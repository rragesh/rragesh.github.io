#!/usr/bin/env python3
"""Check portfolio pages, assets, and compatibility redirects before publication."""

from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://rragesh.github.io/'
REDIRECTS = {
    'about.html': 'index.html#about',
    'blog-home.html': 'index.html#writing',
    'blog-single.html': 'index.html#writing',
    'contact.html': 'index.html#contact',
    'elements.html': 'index.html#home',
    'portfolio.html': 'index.html#work',
    'portfolio-details.html': 'index.html#work',
    'services.html': 'index.html#expertise',
}


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.urls = []
        self.links = []
        self.ids = set()
        self.h1 = 0
        self.errors = []
        self.meta = {}
        self.canonical = []
        self.schemas = []
        self.schema_parts = None
        self.visible = []
        self.in_body = False
        self.hidden_depth = 0
        self.title = []
        self.in_title = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'title':
            self.in_title = True
        if tag == 'body':
            self.in_body = True
        if tag in ('script', 'style'):
            self.hidden_depth += 1
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.schema_parts = []
        if tag == 'meta':
            key = attrs.get('name', attrs.get('property', attrs.get('http-equiv', '')))
            self.meta[key.lower()] = attrs.get('content', '')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs.get('href'))
        if tag == 'a':
            href = attrs.get('href', '')
            self.links.append(href)
            host = urlsplit(href).hostname or ''
            if host == 'instagram.com' or host.endswith('.instagram.com'):
                self.errors.append('Instagram is not an owner profile')
            if href and not href.startswith('#') and urlsplit(href).scheme in ('', 'http', 'https'):
                if attrs.get('target') != '_blank' or 'noopener' not in attrs.get('rel', '').split():
                    self.errors.append(f'Destination link must open safely in a new tab: {href}')
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

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if self.schema_parts is not None:
            self.schema_parts.append(data)
        elif self.in_body and not self.hidden_depth:
            self.visible.append(data)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag == 'script' and self.schema_parts is not None:
            try:
                self.schemas.append(json.loads(''.join(self.schema_parts)))
            except json.JSONDecodeError as error:
                self.errors.append(f'Invalid JSON-LD: {error}')
            self.schema_parts = None
        if tag in ('script', 'style'):
            self.hidden_depth = max(0, self.hidden_depth - 1)
        if tag == 'body':
            self.in_body = False


def local_url_errors(path, urls, pages):
    errors = []
    for url in urls:
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc:
            continue
        if parsed.path.startswith('/'):
            target = (ROOT / unquote(parsed.path.lstrip('/'))).resolve()
        else:
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        if not target.is_file():
            errors.append(f'Missing local target: {url}')
        elif parsed.fragment and target in pages and parsed.fragment not in pages[target].ids:
            errors.append(f'Missing anchor: {url}')
    return errors


pages = {}
for path in [ROOT / 'index.html', *sorted((ROOT / 'projects').glob('*.html'))]:
    page = Page(path)
    page.feed(path.read_text())
    pages[path.resolve()] = page

errors = []
titles = set()
descriptions = set()
for path, page in pages.items():
    title = ''.join(page.title).strip()
    if not title or title in titles:
        page.errors.append('Each canonical page needs a unique title')
    titles.add(title)
    description = page.meta.get('description', '')
    if description in descriptions:
        page.errors.append('Each canonical page needs a unique description')
    descriptions.add(description)
    if page.h1 != 1:
        page.errors.append(f'Expected one h1, got {page.h1}')
    expected = BASE if path.name == 'index.html' else BASE + path.relative_to(ROOT).as_posix()
    if page.canonical != [expected]:
        page.errors.append(f'Expected one canonical URL: {expected}')
    if not page.meta.get('description'):
        page.errors.append('Missing meta description')
    if 'noindex' in page.meta.get('robots', ''):
        page.errors.append('A published portfolio page must be indexable')
    for key in ('og:title', 'og:description', 'og:url', 'og:image', 'og:image:alt', 'twitter:card'):
        if not page.meta.get(key):
            page.errors.append(f'Missing search/social metadata: {key}')
    if page.meta.get('og:url') != expected:
        page.errors.append('Social URL must match the canonical URL')
    image = page.meta.get('og:image', '')
    if not image.startswith(BASE) or not (ROOT / unquote(urlsplit(image).path.lstrip('/'))).is_file():
        page.errors.append('Social preview must reference an existing public image')
    if path.parent.name == 'projects':
        nodes = [node for schema in page.schemas for node in schema.get('@graph', [])]
        work = next((node for node in nodes if node.get('@type') == 'CreativeWork'), {})
        if work.get('author', {}).get('@id') != BASE + '#ragesh' or work.get('url') != expected:
            page.errors.append('Project schema must connect the canonical project and its author')
    page.errors.extend(local_url_errors(path, page.urls, pages))
    errors.extend(f'{path.relative_to(ROOT)}: {error}' for error in page.errors)
for path in [*ROOT.glob('*.html'), *sorted((ROOT / 'projects').glob('*.html'))]:
    if 'resume/Ragesh_CV.pdf' in path.read_text():
        errors.append(f'{path.relative_to(ROOT)} still references the removed résumé')
if (ROOT / 'resume/Ragesh_CV.pdf').exists():
    errors.append('Résumé PDF must not be published')

home = pages[(ROOT / 'index.html').resolve()]
graph = [node for schema in home.schemas for node in schema.get('@graph', [])]
entities = {node.get('@id'): node for node in graph if node.get('@id')}
person_id = BASE + '#ragesh'
person = entities.get(person_id, {})
if person.get('@type') != 'Person' or person.get('name') != 'Ragesh Ramachandran':
    errors.append('Homepage must identify Ragesh with a stable Person entity')
if entities.get(BASE + '#profile', {}).get('mainEntity', {}).get('@id') != person_id:
    errors.append('ProfilePage must reference the Person entity')
if entities.get(BASE + '#robotics-deployment', {}).get('provider', {}).get('@id') != person_id:
    errors.append('Deployment service must reference the Person provider')
if entities.get(BASE + '#robotair', {}).get('founder', {}).get('@id') != person_id:
    errors.append('Robotair must reference Ragesh as its founder')
visible = ' '.join(' '.join(home.visible).split())
questions = entities.get(BASE + '#faq', {}).get('mainEntity', [])
if not questions:
    errors.append('Missing structured FAQ')
for question in questions:
    for text in (question.get('name', ''), question.get('acceptedAnswer', {}).get('text', '')):
        if not text or ' '.join(text.split()) not in visible:
            errors.append(f'FAQ schema must match visible content: {text[:90]}')
for node in graph:
    if node.get('@type') == 'Article':
        if node.get('url') not in home.urls or node.get('headline', '') not in visible:
            errors.append('Structured article must be linked and named in visible content')

def check_references(value):
    if isinstance(value, dict):
        if set(value) == {'@id'} and value['@id'] not in entities:
            errors.append(f'Unresolved structured-data entity: {value["@id"]}')
        for child in value.values():
            check_references(child)
    elif isinstance(value, list):
        for child in value:
            check_references(child)
check_references(graph)

for name, destination in REDIRECTS.items():
    path = ROOT / name
    redirect = Page(path)
    redirect.feed(path.read_text())
    if 'noindex' not in redirect.meta.get('robots', ''):
        redirect.errors.append('Compatibility redirect must not be indexed')
    if redirect.meta.get('refresh') != f'0;url={destination}':
        redirect.errors.append(f'Expected an immediate redirect to {destination}')
    if redirect.canonical != [BASE]:
        redirect.errors.append('Compatibility redirect must use the homepage canonical')
    if destination not in redirect.links:
        redirect.errors.append('Compatibility redirect needs a fallback link to its destination')
    redirect.errors.extend(local_url_errors(path, [*redirect.urls, destination], pages))
    errors.extend(f'{name}: {error}' for error in redirect.errors)

for path in (ROOT / 'css').rglob('*.css'):
    urls = [match.strip().strip('\'"') for match in re.findall(r'url\(([^)]+)\)', path.read_text())]
    errors.extend(f'{path.relative_to(ROOT)}: {error}' for error in local_url_errors(path, urls, pages))

sitemap = ET.parse(ROOT / 'sitemap.xml')
locations = [node.text for node in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
expected_locations = {page.canonical[0] for page in pages.values() if len(page.canonical) == 1}
if set(locations) != expected_locations or len(locations) != len(set(locations)):
    errors.append('Sitemap must list each canonical portfolio page exactly once')
robots = RobotFileParser()
robots.parse((ROOT / 'robots.txt').read_text().splitlines())
if robots.site_maps() != [BASE + 'sitemap.xml']:
    errors.append('robots.txt must advertise the canonical sitemap')
for agent in ('Googlebot', 'bingbot', 'OAI-SearchBot', 'Claude-SearchBot', 'PerplexityBot'):
    for url in [*locations, BASE + 'css/site.css', BASE + 'js/site.js', *[BASE + name for name in REDIRECTS]]:
        if not robots.can_fetch(agent, url):
            errors.append(f'{agent} cannot crawl {url}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Checked {len(pages)} pages and {len(REDIRECTS)} redirects: links, stylesheet assets, new-tab behavior, headings, metadata, schema/visible FAQ parity, sitemap, redirects, and profile cleanup passed.')
