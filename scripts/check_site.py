#!/usr/bin/env python3
"""Check the built site (Astro output) before publication.

Runs against the build output directory (default: dist/, override with --dist PATH)
so it validates exactly what GitHub Pages will serve: pages, bundled assets,
published HTML files, the sitemap, and robots.txt. Run `npm run build` first.
"""

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'src/data'
BASE = 'https://rragesh.github.io/'
LINKEDIN = 'https://www.linkedin.com/in/ragesh-ramachandran/'
MAIN_PAGES = ('index.html', 'about.html', 'work.html', 'writing.html', 'how-i-work.html')
NAVIGATION = ['/', '/about.html', '/work.html', '/writing.html', '/how-i-work.html', LINKEDIN]
# HTML files that are published but are not portfolio pages.
NON_PAGE_HTML = {
    'google50c6424adfbe2f59.html',
    'google84685ae9ed10fc43.html',
}
PROJECT_LINK = re.compile(r'/projects/[^/]+\.html')


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
        self.assets = []
        self.schemas = []
        self.schema_parts = None
        self.visible = []
        self.in_body = False
        self.hidden_depth = 0
        self.title = []
        self.in_title = False
        self.navigation = []
        self.in_navigation = False
        self.section_count = 0
        self.details_depth = 0
        self.article_count = 0
        self.project_links = []
        self.project_chapters = {}
        self.section_ids = []
        self.section_classes = []
        self.breadcrumb_links = []
        self.return_links = []
        self.in_breadcrumbs = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'nav' and attrs.get('aria-label') == 'Main navigation':
            self.in_navigation = True
        if tag == 'nav' and attrs.get('aria-label') == 'Breadcrumb':
            self.in_breadcrumbs = True
        if tag == 'section':
            self.section_count += 1
            self.section_ids.append(attrs.get('id'))
            self.section_classes.append((attrs.get('class') or '').split())
        if tag == 'details':
            self.details_depth += 1
        if tag == 'article' and 'article-card' in (attrs.get('class') or '').split():
            self.article_count += 1
            if self.details_depth:
                self.errors.append('Medium previews must be visible without opening a disclosure')
        if tag == 'title':
            self.in_title = True
        if tag == 'body':
            self.in_body = True
        if tag in ('script', 'style'):
            self.hidden_depth += 1
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.schema_parts = []
        if tag == 'meta':
            key = attrs.get('name', attrs.get('property', attrs.get('http-equiv', ''))) or ''
            self.meta[key.lower()] = attrs.get('content', '')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs.get('href'))
        if (tag == 'link' and attrs.get('rel') in ('stylesheet', 'modulepreload')) or (tag == 'script' and attrs.get('src')):
            self.assets.append(attrs.get('href') or attrs.get('src'))
        if tag == 'a':
            href = attrs.get('href') or ''
            self.links.append(href)
            if self.in_breadcrumbs:
                self.breadcrumb_links.append(href)
            if self.section_classes and 'continue-reading' in self.section_classes[-1]:
                self.return_links.append(href)
            if self.in_navigation:
                self.navigation.append((href, attrs.get('aria-current')))
            if PROJECT_LINK.fullmatch(urlsplit(href).path) and not urlsplit(href).netloc:
                self.project_links.append(href)
                self.project_chapters[href] = self.section_ids[-1] if self.section_ids else None
                if self.details_depth:
                    self.errors.append('Project links must be visible without opening a disclosure')
            host = urlsplit(href).hostname or ''
            if host == 'instagram.com' or host.endswith('.instagram.com'):
                self.errors.append('Instagram is not an owner profile')
            if href and not href.startswith('#') and urlsplit(href).scheme in ('', 'http', 'https'):
                if attrs.get('target') != '_blank' or 'noopener' not in (attrs.get('rel') or '').split():
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
        if attrs.get('srcset'):
            self.urls.extend(candidate.split()[0] for candidate in attrs['srcset'].split(',') if candidate.strip())

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if self.schema_parts is not None:
            self.schema_parts.append(data)
        elif self.in_body and not self.hidden_depth:
            self.visible.append(data)

    def handle_endtag(self, tag):
        if tag == 'section' and self.section_ids:
            self.section_ids.pop()
            self.section_classes.pop()
        if tag == 'nav':
            self.in_navigation = False
            self.in_breadcrumbs = False
        if tag == 'details':
            self.details_depth = max(0, self.details_depth - 1)
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


def resolve(dist, path, url_path):
    """File a local URL path points to, as GitHub Pages would serve it."""
    if url_path.startswith('/'):
        target = dist / unquote(url_path.lstrip('/'))
    else:
        target = path.parent / unquote(url_path) if url_path else path
    if url_path.endswith('/') or target.is_dir():
        target = target / 'index.html'
    return target.resolve()


def local_url_errors(dist, path, urls, pages):
    errors = []
    for url in urls:
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc:
            continue
        target = resolve(dist, path, parsed.path)
        if not target.is_file() or not target.is_relative_to(dist):
            errors.append(f'Missing local target: {url}')
        elif parsed.fragment and target in pages and parsed.fragment not in pages[target].ids:
            errors.append(f'Missing anchor: {url}')
    return errors


def graph_nodes(page):
    return [node for schema in page.schemas for node in schema.get('@graph', [])]


def check(dist):
    errors = []
    project_index = {project['slug']: project for project in json.loads((DATA / 'projects.json').read_text())}
    pages = {}
    expected_files = [dist / name for name in MAIN_PAGES] + [dist / 'projects' / f'{slug}.html' for slug in project_index]
    for path in [*expected_files, *sorted((dist / 'projects').glob('*.html'))]:
        if path.resolve() in pages:
            continue
        if not path.is_file():
            errors.append(f'Missing built page: {path.relative_to(dist)}')
            continue
        page = Page(path)
        page.feed(path.read_text())
        pages[path.resolve()] = page

    titles = set()
    descriptions = set()
    for path, page in pages.items():
        relative = path.relative_to(dist).as_posix()
        in_projects = path.parent.name == 'projects'
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
        if [href for href, _ in page.navigation] != NAVIGATION:
            page.errors.append('Main navigation must expose Home, My story, Work, Writing, How I work, and LinkedIn contact consistently')
        active = [href for href, current in page.navigation if current]
        expected_active = '/about.html' if in_projects else ('/' if relative == 'index.html' else '/' + relative)
        if active != [expected_active]:
            page.errors.append('Main navigation must identify the current page or parent section')
        expected = BASE if relative == 'index.html' else BASE + relative
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
        for key in ('og:image', 'twitter:image'):
            image = page.meta.get(key, '')
            if image and (not image.startswith(BASE) or not resolve(dist, path, urlsplit(image).path).is_file()):
                page.errors.append(f'Social preview must reference an existing public image: {key}')
        if not any(urlsplit(asset).path.startswith('/_astro/') and asset.endswith('.css') for asset in page.assets):
            page.errors.append('Page must load the bundled stylesheet from /_astro/')
        nodes = graph_nodes(page)
        if in_projects:
            chapter = project_index.get(path.stem, {}).get('storyChapter')
            if chapter not in ('origins', 'control'):
                page.errors.append('Project must identify a supported story chapter')
            elif any(f'/about.html#{chapter}' not in links for links in (page.breadcrumb_links, page.return_links)):
                page.errors.append('Project breadcrumb and closing link must return to its story chapter')
            work = next((node for node in nodes if node.get('@type') == 'CreativeWork'), {})
            if work.get('author', {}).get('@id') != BASE + '#ragesh' or work.get('url') != expected:
                page.errors.append('Project schema must connect the canonical project and its author')
        elif relative in ('about.html', 'how-i-work.html'):
            profile = next((node for node in nodes if node.get('@type') == 'ProfilePage'), {})
            if profile.get('url') != expected or profile.get('mainEntity', {}).get('@id') != BASE + '#ragesh':
                page.errors.append('Personal profile must connect its canonical URL and the Person entity')
        elif relative in ('work.html', 'writing.html'):
            collection = next((node for node in nodes if node.get('@type') == 'CollectionPage'), {})
            if collection.get('url') != expected:
                page.errors.append('Collection page must identify its canonical URL in structured data')
        page.errors.extend(local_url_errors(dist, path, page.urls, pages))
        errors.extend(f'{relative}: {error}' for error in page.errors)

    for path in sorted(dist.rglob('*.html')):
        if 'resume/Ragesh_CV.pdf' in path.read_text():
            errors.append(f'{path.relative_to(dist)} still references the removed résumé')
    if any(dist.rglob('Ragesh_CV.pdf')):
        errors.append('Résumé PDF must not be published')

    def page_at(name):
        return pages.get((dist / name).resolve(), Page(dist / name))

    home = page_at('index.html')
    if home.section_count != 1 or home.article_count:
        errors.append('Homepage must contain only the introductory hero, with content on dedicated pages')
    writing = page_at('writing.html')
    if writing.article_count != len(json.loads((DATA / 'medium-posts.json').read_text())):
        errors.append('Writing page must contain every cached Medium preview')
    work_page = page_at('work.html')
    story_page = page_at('about.html')
    expected_projects = {f'/projects/{slug}.html' for slug in project_index}
    if set(story_page.project_links) != expected_projects or len(story_page.project_links) != len(expected_projects):
        errors.append('My story must expose every project exactly once')
    for slug, project in project_index.items():
        if story_page.project_chapters.get(f'/projects/{slug}.html') != project.get('storyChapter'):
            errors.append(f'Project {slug} must be linked from its declared story chapter')
    if work_page.project_links or '/about.html#origins' not in work_page.links or 'projects' not in work_page.ids:
        errors.append('Work must retain the legacy projects anchor and point readers to My story')

    graph = [node for page in pages.values() for node in graph_nodes(page)]
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
    if not entities.get(BASE + 'work.html#faq', {}).get('mainEntity', []):
        errors.append('Missing structured FAQ')
    for page in pages.values():
        visible = ' '.join(' '.join(page.visible).split())
        for node in graph_nodes(page):
            if node.get('@type') == 'FAQPage':
                for question in node.get('mainEntity', []):
                    for text in (question.get('name', ''), question.get('acceptedAnswer', {}).get('text', '')):
                        if not text or ' '.join(text.split()) not in visible:
                            errors.append(f'FAQ schema must match its page content: {text[:90]}')
            if node.get('@type') == 'Article':
                if node.get('url') not in page.urls or node.get('headline', '') not in visible:
                    errors.append('Structured article must be linked and named on its page')

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

    published = {path.relative_to(dist).as_posix() for path in dist.rglob('*.html')}
    unexpected = published - {path.relative_to(dist).as_posix() for path in pages} - NON_PAGE_HTML
    errors.extend(f'{name}: Unexpected published HTML file (not a canonical portfolio page)' for name in sorted(unexpected))

    stylesheets = sorted(dist.rglob('*.css'))
    if not stylesheets:
        errors.append('Build produced no stylesheet')
    for path in stylesheets:
        urls = [match.strip().strip('\'"') for match in re.findall(r'url\(([^)]+)\)', path.read_text())]
        urls = [url for url in urls if not url.startswith(('data:', '#'))]
        errors.extend(f'{path.relative_to(dist)}: {error}' for error in local_url_errors(dist, path, urls, pages))

    locations = []
    try:
        sitemap = ET.parse(dist / 'sitemap.xml')
        locations = [node.text for node in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    except (OSError, ET.ParseError) as error:
        errors.append(f'Sitemap missing or invalid: {error}')
    expected_locations = {page.canonical[0] for page in pages.values() if len(page.canonical) == 1}
    if set(locations) != expected_locations or len(locations) != len(set(locations)):
        errors.append('Sitemap must list each canonical portfolio page exactly once')
    robots = RobotFileParser()
    robots_path = dist / 'robots.txt'
    robots.parse(robots_path.read_text().splitlines() if robots_path.is_file() else [])
    if robots.site_maps() != [BASE + 'sitemap.xml']:
        errors.append('robots.txt must advertise the canonical sitemap')
    assets = sorted({BASE + urlsplit(asset).path.lstrip('/') for page in pages.values() for asset in page.assets if not urlsplit(asset).netloc})
    for agent in ('Googlebot', 'bingbot', 'OAI-SearchBot', 'Claude-SearchBot', 'PerplexityBot'):
        for url in [*locations, *assets]:
            if not robots.can_fetch(agent, url):
                errors.append(f'{agent} cannot crawl {url}')
    return errors, len(pages)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--dist', type=Path, default=ROOT / 'dist', help='build output directory to check (default: dist/)')
    args = parser.parse_args()
    dist = args.dist.resolve()
    if not (dist / 'index.html').is_file():
        raise SystemExit(f'No built site at {dist}; run `npm run build` first.')
    errors, count = check(dist)
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Checked {count} built pages in {dist}: navigation, links, bundled assets, hero-only home, visible writing/projects, metadata, schema, sitemap, robots, published files, and profile cleanup passed.')


if __name__ == '__main__':
    main()
