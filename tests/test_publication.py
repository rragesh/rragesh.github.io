import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('publication', Path(__file__).parents[1] / 'scripts/check_live.py')
publication = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publication)
BASE = publication.CANONICAL


def page(canonical=BASE):
    graph = {'@graph': [
        {'@type': 'ProfilePage'},
        {'@type': 'Person', '@id': BASE + '#ragesh'}
    ]}
    return f'<link rel="canonical" href="{canonical}"><meta name="description" content="Robotics deployment"><meta property="og:url" content="{canonical}"><script type="application/ld+json">{json.dumps(graph)}</script>'


class PublicationTests(unittest.TestCase):
    def test_detects_old_site_even_when_http_succeeds(self):
        errors = publication.validate_html('<h1>Ragesh Ramachandran</h1>', BASE)
        self.assertTrue(any('old site' in error for error in errors))

    def test_accepts_published_profile(self):
        self.assertEqual(publication.validate_html(page(), BASE), [])

    def test_rejects_header_and_html_indexing_blocks(self):
        for document, header in ((page(), 'noindex'), (page() + '<meta name="robots" content="none">', ''), (page(), 'nosnippet')):
            with self.subTest(header=header):
                self.assertTrue(any('blocked' in error for error in publication.validate_html(document, BASE, header)))

    def test_rejects_wrong_domain_canonical(self):
        errors = publication.validate_html(page('https://example.com/'), BASE)
        self.assertIn('canonical URL missing or incorrect', errors)


if __name__ == '__main__':
    unittest.main()
