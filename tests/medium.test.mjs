import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { mkdir, mkdtemp, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { after, describe, test } from "node:test";
import sharp from "sharp";
import * as medium from "../scripts/update-medium.mjs";

const feed = ({ link = "https://rragesh.medium.com/story", title = "A &amp; B", body = "A robotics article.", image = "" } = {}) =>
  `<rss xmlns:content="http://purl.org/rss/1.0/modules/content/"><channel><item>
      <title>${title}</title><link>${link}</link><pubDate>Thu, 28 May 2026 06:51:00 GMT</pubDate>
      <category>robotics</category><content:encoded><![CDATA[${image}<p>${body}</p>]]></content:encoded>
      </item></channel></rss>`;

const scratch = process.env.PANE_SCRATCH_DIR ?? (await import("node:os")).tmpdir();
const temporaryRoots = [];
async function temporaryRoot() {
  await mkdir(scratch, { recursive: true });
  const root = await mkdtemp(join(scratch, "medium-test-"));
  temporaryRoots.push(root);
  return root;
}
after(() => Promise.all(temporaryRoots.map((root) => rm(root, { recursive: true, force: true }))));

const quiet = { log() {}, warn() {} };
const offline = async (url) => {
  throw new Error(`unexpected network access: ${url}`);
};

describe("parseFeed", () => {
  test("RSS becomes plain-text, accessible preview data", () => {
    const [post] = medium.parseFeed(feed({ body: "Useful &amp; practical <script>bad()</script> ideas." }));
    assert.equal(post.date, "2026-05-28");
    assert.equal(post.displayDate, "May 28, 2026");
    assert.deepEqual(post.topics, ["Robotics"]);
    // Entities are decoded to plain text; Astro escapes it when the card renders.
    assert.equal(post.title, "A & B");
    assert.equal(post.excerpt, "Useful & practical ideas.");
    assert.ok(!post.excerpt.includes("bad()"));
    assert.ok(post.url.includes("utm_source=rragesh.github.io"));
  });

  test("rejects non-Medium and script links", () => {
    for (const link of ["javascript:alert(1)", "https://medium.com.evil.test/story", "http://medium.com/story"]) {
      assert.throws(() => medium.parseFeed(feed({ link })), Error, link);
    }
  });

  test("empty and malformed feeds fail", () => {
    for (const content of ["<rss><channel/></rss>", "not xml", feed().slice(0, 200)]) {
      assert.throws(() => medium.parseFeed(content), Error, content);
    }
  });

  test("dedupes, sorts newest first and limits the list", () => {
    const item = (slug, date) => `<item><title>${slug}</title><link>https://rragesh.medium.com/${slug}?source=rss</link>
      <pubDate>${date}</pubDate><description><![CDATA[<p>Body</p>]]></description></item>`;
    const items = [item("old", "Mon, 04 May 2026 10:00:00 GMT"), item("new", "Thu, 07 May 2026 10:00:00 GMT"), item("old", "Mon, 04 May 2026 10:00:00 GMT")];
    for (let day = 10; day < 20; day += 1) items.push(item(`extra-${day}`, `${day} Apr 2026 08:00:00 +0000`));
    const posts = medium.parseFeed(`<rss><channel>${items.join("")}</channel></rss>`);
    assert.equal(posts.length, 7);
    assert.deepEqual(posts.slice(0, 3).map((post) => post.title), ["new", "old", "extra-19"]);
    assert.equal(posts[0].displayDate, "May 7, 2026");
    assert.equal(posts[0].url, "https://rragesh.medium.com/new?utm_source=rragesh.github.io&utm_medium=website&utm_campaign=portfolio");
  });

  test("normalises topic names", () => {
    assert.deepEqual(["nvidia", "gpu", "ros2", "devops", "fleet-management", "3d-printing"].map(medium.topicName), [
      "NVIDIA", "GPU", "ROS 2", "DevOps", "Fleet Management", "3D Printing",
    ]);
  });

  test("excerpt uses the first substantial paragraph and truncates at 190 characters", () => {
    const short = "Short intro.";
    const long = "Robots ".repeat(40).trim() + ".";
    const excerpt = medium.excerptFrom([short, long]);
    assert.ok(excerpt.length <= 190);
    assert.ok(excerpt.endsWith("Robots…"));
    assert.equal(medium.excerptFrom(["One.", "Two."]), "One. Two.");
  });
});

describe("parsePreview", () => {
  test("ignores tracking pixels", () => {
    const { image } = medium.parsePreview('<img src="https://medium.com/_/stat?event=view"><img src="https://cdn-images-1.medium.com/max/800/cover.png">');
    assert.equal(image, "https://cdn-images-1.medium.com/max/800/cover.png");
  });
});

describe("main", () => {
  test("refresh writes only the cached posts and thumbnails, and failures change nothing", async () => {
    const root = await temporaryRoot();
    await mkdir(join(root, "src/pages"), { recursive: true });
    await writeFile(join(root, "src/pages/index.astro"), "<h1>Hero only</h1>");
    const rss = join(root, "feed.xml");
    const cover = "https://cdn-images-1.medium.com/max/1024/1*cover.png";
    await writeFile(rss, feed({ image: `<img src="https://medium.com/_/stat?event=view"><img src="${cover}">` }));
    const png = await sharp({ create: { width: 1600, height: 900, channels: 4, background: "#3a7" } }).png().toBuffer();
    const requested = [];
    const fetchBytes = async (url) => {
      requested.push(url);
      return png;
    };

    assert.equal(await medium.main(["--feed-file", rss], { root, fetchBytes, ...quiet }), 0);
    assert.equal(await readFile(join(root, "src/pages/index.astro"), "utf8"), "<h1>Hero only</h1>");
    const posts = JSON.parse(await readFile(join(root, medium.POSTS_FILE), "utf8"));
    assert.equal(posts.length, 1);
    assert.equal(posts[0].title, "A & B");
    const { file } = medium.thumbnailName(cover);
    assert.deepEqual(requested, [cover.replace("/max/1024/", "/max/800/")]);
    assert.equal(posts[0].localImage, `medium/${file}`);
    const metadata = await sharp(join(root, medium.IMAGE_DIR, file)).metadata();
    assert.deepEqual([metadata.format, metadata.width, metadata.height], ["webp", 800, 450]);

    // Cached thumbnails are reused without downloading again.
    assert.equal(await medium.main(["--feed-file", rss], { root, fetchBytes: offline, ...quiet }), 0);

    const lastGood = await readFile(join(root, medium.POSTS_FILE), "utf8");
    const lastImages = await readdir(join(root, medium.IMAGE_DIR));
    for (const content of ["<rss><channel/></rss>", "not xml", feed({ link: "https://example.com/x" })]) {
      await writeFile(rss, content);
      assert.equal(await medium.main(["--feed-file", rss], { root, fetchBytes: offline, ...quiet }), 1);
      assert.equal(await readFile(join(root, medium.POSTS_FILE), "utf8"), lastGood);
      assert.deepEqual(await readdir(join(root, medium.IMAGE_DIR)), lastImages);
    }
    assert.equal(await medium.main(["--feed-file", join(root, "missing.xml")], { root, ...quiet }), 1);
  });

  test("an unavailable thumbnail degrades to a text-only card", async () => {
    const root = await temporaryRoot();
    const rss = join(root, "feed.xml");
    await writeFile(rss, feed({ image: '<img src="https://miro.medium.com/max/1400/broken.png">' }));
    assert.equal(await medium.main(["--feed-file", rss], { root, fetchBytes: offline, ...quiet }), 0);
    const [post] = JSON.parse(await readFile(join(root, medium.POSTS_FILE), "utf8"));
    assert.equal(post.localImage, "");
    assert.ok(!existsSync(join(root, medium.IMAGE_DIR)) || (await readdir(join(root, medium.IMAGE_DIR))).length === 0);
  });
});

describe("cached data", () => {
  test("every cached post resolves to a thumbnail in src/assets", async () => {
    const posts = JSON.parse(await readFile(new URL("../src/data/medium-posts.json", import.meta.url), "utf8"));
    assert.ok(posts.length > 0 && posts.length <= 7);
    for (const post of posts) {
      assert.match(post.url, /^https:\/\/([a-z0-9-]+\.)?medium\.com\//);
      if (post.localImage) assert.ok(existsSync(new URL(`../src/assets/${post.localImage}`, import.meta.url)), post.localImage);
    }
  });

  test("the card renders feed text through Astro's escaping (no set:html)", async () => {
    const card = await readFile(new URL("../src/components/writing/ArticleCard.astro", import.meta.url), "utf8");
    assert.ok(!/set:html|set:text/.test(card));
  });
});
