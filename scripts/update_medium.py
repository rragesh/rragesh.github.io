#!/usr/bin/env python3
"""Embed Medium RSS previews in static HTML; keep last-good content on failure."""

import argparse
from datetime import timezone
from email.utils import parsedate_to_datetime
import hashlib
from io import BytesIO
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
FEED_URL = "https://rragesh.medium.com/feed"
START = "<!-- MEDIUM:START -->"
END = "<!-- MEDIUM:END -->"


class PreviewParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paragraphs = []
        self.current = None
        self.image = ""
        self.ignored = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self.ignored += 1
        if tag == "p":
            self.current = []
        if tag == "img" and not self.image:
            candidate = attrs.get("src", "")
            if urlsplit(candidate).hostname in ("cdn-images-1.medium.com", "miro.medium.com"):
                self.image = candidate

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.ignored = max(0, self.ignored - 1)
        if tag == "p" and self.current is not None:
            self.paragraphs.append("".join(self.current))
            self.current = None

    def handle_data(self, data):
        if not self.ignored and self.current is not None:
            self.current.append(data)


def normalize(text):
    return " ".join(text.split())


def medium_url(value):
    parsed = urlsplit(value)
    host = parsed.hostname or ""
    if parsed.scheme != "https" or not (host == "medium.com" or host.endswith(".medium.com")):
        raise ValueError(f"Not a Medium HTTPS article: {value}")
    return urlunsplit(("https", host, parsed.path, urlencode({
        "utm_source": "rragesh.github.io", "utm_medium": "website", "utm_campaign": "portfolio"
    }), ""))


def parse_feed(content, limit=7):
    root = ET.fromstring(content)
    posts = []
    seen = set()
    for item in root.findall("./channel/item"):
        title = normalize(item.findtext("title", ""))
        if not title:
            continue
        url = medium_url(item.findtext("link", ""))
        if url in seen:
            continue
        seen.add(url)
        published = parsedate_to_datetime(item.findtext("pubDate", ""))
        if published.tzinfo is None:
            published = published.replace(tzinfo=timezone.utc)
        parser = PreviewParser()
        parser.feed(item.findtext("{http://purl.org/rss/1.0/modules/content/}encoded", item.findtext("description", "")))
        paragraphs = [normalize(p) for p in parser.paragraphs if normalize(p)]
        excerpt = next((p for p in paragraphs if len(p) > 85), " ".join(paragraphs))
        if len(excerpt) > 190:
            excerpt = excerpt[:187].rsplit(" ", 1)[0].rstrip(".,;:") + "…"
        tags = [normalize(tag.text or "").replace("-", " ").title() for tag in item.findall("category")]
        names = {"Nvidia": "NVIDIA", "Gpu": "GPU", "Ros2": "ROS 2", "Devops": "DevOps"}
        tags = [names.get(tag, tag) for tag in tags]
        posts.append({
            "title": title, "url": url, "date": published.date().isoformat(),
            "displayDate": published.strftime("%b %d, %Y").replace(" 0", " "),
            "excerpt": excerpt, "topics": list(dict.fromkeys(tags)), "image": parser.image,
        })
    posts.sort(key=lambda post: post["date"], reverse=True)
    if not posts:
        raise ValueError("The feed contained no usable articles; retaining existing previews.")
    return posts[:limit]


def download(url):
    request = Request(url, headers={"User-Agent": "RageshPortfolio/1.0 (+https://rragesh.github.io/)"})
    with urlopen(request, timeout=30) as response:
        return response.read(12_000_001)


def cache_image(url):
    """Use a same-origin thumbnail; avoid tracking pixels and browser feed services."""
    if not url:
        return ""
    url = re.sub(r"/max/\d+/", "/max/800/", url)
    name = hashlib.sha256(url.encode()).hexdigest()[:16]
    directory = ROOT / "img" / "medium"
    directory.mkdir(parents=True, exist_ok=True)
    existing = list(directory.glob(name + ".webp"))
    if existing:
        return existing[0].relative_to(ROOT).as_posix()
    try:
        data = download(url)
        if len(data) > 12_000_000:
            raise ValueError("Article image exceeded size limit")
        with Image.open(BytesIO(data)) as original:
            image = ImageOps.exif_transpose(original).convert("RGB")
            image.thumbnail((800, 600))
            metadata = Image.Exif()
            metadata[270] = f"Source: {url}. Published by Ragesh Ramachandran on Medium."
            path = directory / (name + ".webp")
            image.save(path, format="WEBP", quality=82, exif=metadata)
        return path.relative_to(ROOT).as_posix()
    except Exception as error:
        print(f"Thumbnail unavailable; using text-only preview: {error}", file=sys.stderr)
        return ""


def render_posts(posts):
    cards = []
    for post in posts:
        image = f'<img class="article-cover" src="{escape(post["localImage"], quote=True)}" width="800" height="450" loading="lazy" alt="">' if post.get("localImage") else ""
        topics = escape(json.dumps(post["topics"]), quote=True)
        url = escape(post["url"], quote=True)
        cards.append(f'''<article class="article-card" data-topics="{topics}">
            {image}
            <div class="article-meta"><time datetime="{post['date']}">{post['displayDate']}</time><span>On Medium</span></div>
            <h3><a href="{url}" target="_blank" rel="noopener">{escape(post['title'])}</a></h3>
            <p>{escape(post['excerpt'])}</p>
            <a class="text-link" href="{url}" target="_blank" rel="noopener" aria-label="Read on Medium: {escape(post['title'], quote=True)}">Read on Medium <span class="arrow diagonal" aria-hidden="true"></span></a>
          </article>''')
    return "\n          ".join(cards)


def replace_previews(document, markup):
    if document.count(START) != 1 or document.count(END) != 1:
        raise ValueError("Expected exactly one Medium preview region")
    before, rest = document.split(START)
    _, after = rest.split(END)
    return before + START + "\n          " + markup + "\n          " + END + after


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("--feed-file", type=Path, help="Use a local RSS file instead of the network")
    options = args.parse_args()
    try:
        # Parse fully before touching the homepage so malformed feeds never erase it.
        feed = options.feed_file.read_bytes() if options.feed_file else download(FEED_URL)
        posts = parse_feed(feed)
        document = (ROOT / "index.html").read_text()
        replace_previews(document, "")
        for post in posts:
            post["localImage"] = cache_image(post["image"])
        rendered = replace_previews(document, render_posts(posts))
        (ROOT / "data").mkdir(exist_ok=True)
        (ROOT / "data/medium-posts.json").write_text(json.dumps(posts, ensure_ascii=False, indent=2) + "\n")
        (ROOT / "index.html").write_text(rendered)
        print(f"Embedded {len(posts)} Medium article previews.")
    except Exception as error:
        print(f"Medium refresh failed; existing homepage retained: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
