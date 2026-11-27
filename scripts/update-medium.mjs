#!/usr/bin/env node
// Refresh the Writing page's cached Medium previews; keep last-good content on failure.
//
// Success: writes src/data/medium-posts.json and caches thumbnails in src/assets/medium/, exit 0.
// Failure: prints the reason, leaves every file untouched, exit 1.

import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import { mkdir, readFile, rename, rm, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";
import { Parser } from "htmlparser2";
import sharp from "sharp";

export const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
export const FEED_URL = "https://rragesh.medium.com/feed";
export const POSTS_FILE = "src/data/medium-posts.json";
export const IMAGE_DIR = "src/assets/medium";
const MAX_BYTES = 12_000_000;
const USER_AGENT = "RageshPortfolio/1.0 (+https://rragesh.github.io/)";
const IMAGE_HOSTS = new Set(["cdn-images-1.medium.com", "miro.medium.com"]);
const TOPIC_NAMES = { Nvidia: "NVIDIA", Gpu: "GPU", Ros2: "ROS 2", Devops: "DevOps" };
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export function normalize(text) {
  return text.replace(/\s+/g, " ").trim();
}

/** Canonical HTTPS Medium article URL with the portfolio's UTM parameters; throws otherwise. */
export function mediumUrl(value) {
  let url;
  try {
    url = new URL(value);
  } catch {
    throw new Error(`Not a Medium HTTPS article: ${value}`);
  }
  const host = url.hostname;
  if (url.protocol !== "https:" || !(host === "medium.com" || host.endsWith(".medium.com"))) {
    throw new Error(`Not a Medium HTTPS article: ${value}`);
  }
  return `https://${host}${url.pathname}?utm_source=rragesh.github.io&utm_medium=website&utm_campaign=portfolio`;
}

/** Paragraph text and the first Medium-CDN image of an article body (tracking pixels are skipped). */
export function parsePreview(html) {
  const paragraphs = [];
  let current = null;
  let image = "";
  let ignored = 0;
  const parser = new Parser(
    {
      onopentag(name, attrs) {
        if (name === "script" || name === "style") ignored += 1;
        if (name === "p") current = [];
        if (name === "img" && !image) {
          let host = "";
          try {
            host = new URL(attrs.src ?? "").hostname;
          } catch {}
          if (IMAGE_HOSTS.has(host)) image = attrs.src;
        }
      },
      onclosetag(name) {
        if (name === "script" || name === "style") ignored = Math.max(0, ignored - 1);
        if (name === "p" && current !== null) {
          paragraphs.push(current.join(""));
          current = null;
        }
      },
      ontext(text) {
        if (!ignored && current !== null) current.push(text);
      },
    },
    { decodeEntities: true },
  );
  parser.end(html);
  return { paragraphs, image };
}

/** Strict-enough XML reader: a single element tree, failing on unclosed or stray content. */
function parseXml(content) {
  const source = typeof content === "string" ? content : Buffer.from(content).toString("utf8");
  const document = { name: "#document", children: [], text: "" };
  const stack = [document];
  const fail = (reason) => {
    throw new Error(`Malformed feed: ${reason}`);
  };
  const parser = new Parser(
    {
      onopentag(name) {
        const parent = stack.at(-1);
        if (parent === document && document.children.length) fail("multiple root elements");
        const element = { name, children: [], text: "" };
        parent.children.push(element);
        stack.push(element);
      },
      onclosetag(name, isImplied) {
        // htmlparser2 reports self-closing tags (`<channel/>`) as implied too; anything else is malformed.
        const selfClosing = isImplied && source.slice(parser.startIndex, parser.endIndex + 1).endsWith("/>");
        if ((isImplied && !selfClosing) || stack.length < 2 || stack.at(-1).name !== name) fail(`unclosed or mismatched <${name}>`);
        stack.pop();
      },
      ontext(text) {
        if (stack.length === 1) {
          if (text.trim()) fail("text outside the root element");
          return;
        }
        stack.at(-1).text += text;
      },
      onerror(error) {
        fail(error.message);
      },
    },
    { xmlMode: true, decodeEntities: true },
  );
  parser.end(source);
  if (stack.length !== 1) fail("unexpected end of document");
  if (document.children.length !== 1) fail("no root element");
  return document.children[0];
}

const child = (element, name) => element.children.find((node) => node.name === name);
const childText = (element, name, fallback = "") => child(element, name)?.text ?? fallback;

/** Parse an RFC 2822 date, keeping the calendar date of the feed's own offset (like Python's parsedate). */
export function parseDate(value) {
  const match = /^\s*(?:[A-Za-z]{3},\s*)?(\d{1,2})\s+([A-Za-z]{3})\s+(\d{2}|\d{4})\s+(\d{1,2}):(\d{2})(?::(\d{2}))?(?:\s+\S+)?\s*$/.exec(value);
  const month = match ? MONTHS.findIndex((name) => name.toLowerCase() === match[2].toLowerCase()) : -1;
  if (!match || month < 0) throw new Error(`Invalid publication date: ${value}`);
  let year = Number(match[3]);
  if (match[3].length === 2) year += year < 50 ? 2000 : 1900;
  const day = Number(match[1]);
  const check = new Date(Date.UTC(year, month, day));
  if (check.getUTCMonth() !== month || check.getUTCDate() !== day || Number(match[4]) > 23 || Number(match[5]) > 59) {
    throw new Error(`Invalid publication date: ${value}`);
  }
  return {
    date: `${String(year).padStart(4, "0")}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`,
    displayDate: `${MONTHS[month]} ${day}, ${year}`,
  };
}

export function excerptFrom(paragraphs) {
  const cleaned = paragraphs.map(normalize).filter(Boolean);
  let excerpt = cleaned.find((paragraph) => [...paragraph].length > 85) ?? cleaned.join(" ");
  const chars = [...excerpt];
  if (chars.length > 190) {
    const cut = chars.slice(0, 187).join("");
    const space = cut.lastIndexOf(" ");
    excerpt = (space >= 0 ? cut.slice(0, space) : cut).replace(/[.,;:]+$/, "") + "…";
  }
  return excerpt;
}

/** Same casing as Python's str.title(): capitalise each run of letters. */
const titleCase = (text) => text.replace(/\p{L}+/gu, (word) => word[0].toUpperCase() + word.slice(1).toLowerCase());

export function topicName(tag) {
  const name = titleCase(normalize(tag).replaceAll("-", " "));
  return TOPIC_NAMES[name] ?? name;
}

/** Parse a Medium RSS feed into preview records (newest first, deduplicated, at most `limit`). */
export function parseFeed(content, limit = 7) {
  const root = parseXml(content);
  const channel = child(root, "channel");
  const items = channel ? channel.children.filter((node) => node.name === "item") : [];
  const posts = [];
  const seen = new Set();
  for (const item of items) {
    const title = normalize(childText(item, "title"));
    if (!title) continue;
    const url = mediumUrl(childText(item, "link"));
    if (seen.has(url)) continue;
    seen.add(url);
    const { date, displayDate } = parseDate(childText(item, "pubDate"));
    const preview = parsePreview(childText(item, "content:encoded", childText(item, "description")));
    const topics = item.children.filter((node) => node.name === "category").map((node) => topicName(node.text));
    posts.push({
      title,
      url,
      date,
      displayDate,
      excerpt: excerptFrom(preview.paragraphs),
      topics: [...new Set(topics)],
      image: preview.image,
    });
  }
  posts.sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0));
  if (!posts.length) throw new Error("The feed contained no usable articles; retaining existing previews.");
  return posts.slice(0, limit);
}

/** Fetch a URL with a timeout and a hard size limit. */
export async function download(url) {
  const response = await fetch(url, {
    headers: { "User-Agent": USER_AGENT },
    signal: AbortSignal.timeout(30_000),
  });
  if (!response.ok) throw new Error(`HTTP ${response.status} for ${url}`);
  const chunks = [];
  let size = 0;
  for await (const chunk of response.body) {
    size += chunk.length;
    if (size > MAX_BYTES) throw new Error(`Response exceeded size limit: ${url}`);
    chunks.push(chunk);
  }
  return Buffer.concat(chunks);
}

/** Normalised thumbnail URL and its cache file name. */
export function thumbnailName(url) {
  const normalized = url.replace(/\/max\/\d+\//, "/max/800/");
  return { url: normalized, file: createHash("sha256").update(normalized).digest("hex").slice(0, 16) + ".webp" };
}

/**
 * Prepare a same-origin thumbnail (no tracking pixels or feed services in the browser).
 * Returns the asset-relative path, plus encoded bytes when the file is not cached yet.
 * A failed download degrades to a text-only card, as before.
 */
export async function prepareImage(imageUrl, { root = ROOT, fetchBytes = download, log = console.error } = {}) {
  if (!imageUrl) return { localImage: "" };
  const { url, file } = thumbnailName(imageUrl);
  const localImage = `medium/${file}`;
  if (existsSync(join(root, IMAGE_DIR, file))) return { localImage };
  try {
    const data = await fetchBytes(url);
    if (data.length > MAX_BYTES) throw new Error("Article image exceeded size limit");
    const bytes = await sharp(data)
      .rotate()
      .removeAlpha()
      .toColourspace("srgb")
      .resize(800, 600, { fit: "inside", withoutEnlargement: true })
      .withExif({ IFD0: { ImageDescription: `Source: ${url}. Published by Ragesh Ramachandran on Medium.` } })
      .webp({ quality: 82 })
      .toBuffer();
    return { localImage, file, bytes };
  } catch (error) {
    log(`Thumbnail unavailable; using text-only preview: ${error.message}`);
    return { localImage: "" };
  }
}

export async function main(argv = process.argv.slice(2), { root = ROOT, fetchBytes = download, log = console.log, warn = console.error } = {}) {
  const created = [];
  try {
    const { values } = parseArgs({ args: argv, options: { "feed-file": { type: "string" } } });
    // Parse and prepare everything in memory first so a bad feed never touches the repo.
    const feed = values["feed-file"] ? await readFile(values["feed-file"]) : await fetchBytes(FEED_URL);
    const posts = parseFeed(feed);
    const images = [];
    for (const post of posts) {
      const prepared = await prepareImage(post.image, { root, fetchBytes, log: warn });
      post.localImage = prepared.localImage;
      if (prepared.bytes && !images.some((image) => image.file === prepared.file)) images.push(prepared);
    }

    const directory = join(root, IMAGE_DIR);
    await mkdir(directory, { recursive: true });
    for (const { file, bytes } of images) {
      const target = join(directory, file);
      await writeFile(target, bytes, { flag: "wx" });
      created.push(target);
    }
    const postsFile = join(root, POSTS_FILE);
    const temporary = `${postsFile}.tmp-${process.pid}`;
    created.push(temporary);
    await mkdir(dirname(postsFile), { recursive: true });
    await writeFile(temporary, JSON.stringify(posts, null, 2) + "\n");
    await rename(temporary, postsFile);
    log(`Cached ${posts.length} Medium article previews.`);
    return 0;
  } catch (error) {
    await Promise.all(created.map((path) => rm(path, { force: true })));
    warn(`Medium refresh failed: ${error.message}`);
    return 1;
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = await main();
}
