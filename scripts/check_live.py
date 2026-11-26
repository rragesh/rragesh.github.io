#!/usr/bin/env python3
"""Verify publication over HTTP. This checks availability, not search-engine indexing."""

import argparse
from html.parser import HTMLParser
import json
import re
from urllib.error import URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

CANONICAL = 'https://rragesh.github.io/'


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}
        self.canonicals = []
        self.schemas = []
        self.parts = None

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'meta':
            self.meta[attrs.get('name', attrs.get('property', ''))] = attrs.get('content', '')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs.get('href'))
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.parts = []

    def handle_data(self, data):
        if self.parts is not None:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.parts is not None:
            self.schemas.append(json.loads(''.join(self.parts)))
            self.parts = None


def validate_html(document, canonical, header_robots=''):
    page = Metadata()
    page.feed(document)
    errors = []
    if page.canonicals != [canonical]:
        errors.append('canonical URL missing or incorrect')
    directives = set(re.split(r'[\s,]+', (page.meta.get('robots', '') + ' ' + header_robots).lower()))
    if directives & {'noindex', 'none', 'nosnippet'}:
        errors.append('page is blocked from indexing or search snippets')
    if not page.meta.get('description') or page.meta.get('og:url') != canonical:
        errors.append('search metadata is missing or stale')
    nodes = [node for schema in page.schemas for node in schema.get('@graph', [])]
    if canonical in (CANONICAL, CANONICAL + 'about.html', CANONICAL + 'how-i-work.html'):
        expected_type = 'ProfilePage'
    elif canonical in (CANONICAL + 'work.html', CANONICAL + 'writing.html'):
        expected_type = 'CollectionPage'
    else:
        expected_type = 'CreativeWork'
    if not any(node.get('@type') == expected_type for node in nodes):
        errors.append(f'{expected_type} structured data not published; the old site may still be live')
    if not any(node.get('@type') == 'Person' and node.get('@id') == CANONICAL + '#ragesh' for node in nodes):
        errors.append('Ragesh author identity is missing')
    return errors


def fetch(url):
    request = Request(url, headers={'User-Agent': 'PortfolioPublicationCheck/1.0'})
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise ValueError(f'HTTP {response.status}: {url}')
        return response.read().decode('utf-8'), response.headers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default=CANONICAL, help='HTTP origin to check; canonicals must still use the production domain')
    args = parser.parse_args()
    base = args.base_url.rstrip('/') + '/'
    try:
        # Fail early and clearly when the fork changes have not been published.
        homepage, headers = fetch(base)
        errors = validate_html(homepage, CANONICAL, headers.get('X-Robots-Tag', ''))
        if errors:
            raise ValueError('Homepage: ' + '; '.join(errors))
        robots_text, _ = fetch(urljoin(base, 'robots.txt'))
        robots = RobotFileParser()
        robots.parse(robots_text.splitlines())
        if robots.site_maps() != [CANONICAL + 'sitemap.xml']:
            raise ValueError('robots.txt does not advertise the canonical sitemap')
        sitemap_text, _ = fetch(urljoin(base, 'sitemap.xml'))
        urls = [node.text for node in ET.fromstring(sitemap_text).findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        if CANONICAL not in urls or len(urls) != len(set(urls)):
            raise ValueError('Sitemap must include the homepage and contain no duplicates')
        for canonical in urls:
            if not canonical.startswith(CANONICAL):
                raise ValueError(f'Unexpected sitemap domain: {canonical}')
            for agent in ('Googlebot', 'bingbot', 'OAI-SearchBot', 'Claude-SearchBot', 'PerplexityBot'):
                if not robots.can_fetch(agent, canonical):
                    raise ValueError(f'{agent} blocked from {canonical}')
            if canonical == CANONICAL:
                continue
            document, headers = fetch(urljoin(base, urlsplit(canonical).path.lstrip('/')))
            errors = validate_html(document, canonical, headers.get('X-Robots-Tag', ''))
            if errors:
                raise ValueError(canonical + ': ' + '; '.join(errors))
        print(f'Publication verified: {len(urls)} canonical pages, structured identities, sitemap, and crawler access. Search-engine indexing is not measured by this check.')
        return 0
    except (URLError, ValueError, ET.ParseError) as error:
        print(f'Publication check failed: {error}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
