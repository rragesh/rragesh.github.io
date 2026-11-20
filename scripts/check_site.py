#!/usr/bin/env python3
"""Check shipped portfolio routes for broken local URLs and removed résumé links."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.urls = []
        self.ids = set()
        self.h1 = 0
        self.errors = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'h1':
            self.h1 += 1
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.errors.append(f"Duplicate ID: {attrs['id']}")
            self.ids.add(attrs['id'])
        if tag == 'img' and 'alt' not in attrs:
            self.errors.append('Image missing alt attribute')
        for name in ('href', 'src'):
            if attrs.get(name):
                self.urls.append(attrs[name])


pages = {}
for path in [ROOT / 'index.html', *sorted((ROOT / 'projects').glob('*.html'))]:
    page = Page(path)
    page.feed(path.read_text())
    pages[path.resolve()] = page

errors = []
for path, page in pages.items():
    if page.h1 != 1:
        page.errors.append(f'Expected one h1, got {page.h1}')
    for url in page.urls:
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc:
            continue
        target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        if not target.is_file():
            page.errors.append(f'Missing local target: {url}')
        elif parsed.fragment and target in pages and parsed.fragment not in pages[target].ids:
            page.errors.append(f'Missing anchor: {url}')
    errors.extend(f'{path.relative_to(ROOT)}: {error}' for error in page.errors)
for path in ROOT.rglob('*.html'):
    if '.git' not in path.parts and 'resume/Ragesh_CV.pdf' in path.read_text(errors='replace'):
        errors.append(f'{path.relative_to(ROOT)} still references the removed résumé')
if (ROOT / 'resume/Ragesh_CV.pdf').exists():
    errors.append('Résumé PDF must not be published')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Checked {len(pages)} pages: local links, anchors, images, headings, and résumé removal passed.')
