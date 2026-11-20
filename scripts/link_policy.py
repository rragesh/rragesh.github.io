#!/usr/bin/env python3
"""Apply the owner's new-tab preference without changing same-page navigation."""

from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlsplit


def open_in_new_tabs(source):
    offsets = [0]
    for line in source.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))
    edits = []

    class Links(HTMLParser):
        def handle_starttag(self, tag, attributes):
            attrs = dict(attributes)
            href = attrs.get("href", "")
            if tag != "a" or not href or href.startswith("#"):
                return
            if urlsplit(href).scheme not in ("", "http", "https"):
                return
            raw = self.get_starttag_text()
            rel = set((attrs.get("rel") or "").split())
            rel.discard("opener")
            rel.add("noopener")
            clean = re.sub(r'''\s+(?:target|rel)\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+)''', "", raw, flags=re.I)
            replacement = clean[:-1] + f' target="_blank" rel="{" ".join(sorted(rel))}">'
            line, column = self.getpos()
            start = offsets[line - 1] + column
            edits.append((start, start + len(raw), replacement))

    Links().feed(source)
    for start, end, replacement in reversed(edits):
        source = source[:start] + replacement + source[end:]
    return source


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    for path in [*root.glob("*.html"), *(root / "projects").glob("*.html")]:
        source = path.read_bytes().decode("utf-8")
        updated = open_in_new_tabs(source)
        if source != updated:
            path.write_bytes(updated.encode("utf-8"))
            print(f"Updated links: {path.relative_to(root)}")
