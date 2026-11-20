import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('link_policy', Path(__file__).parents[1] / 'scripts/link_policy.py')
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


class LinkPolicyTests(unittest.TestCase):
    def test_external_and_project_links_open_safely(self):
        for href in ('https://robotair.io/', 'projects/recharge.html'):
            with self.subTest(href=href):
                result = policy.open_in_new_tabs(f'<a href="{href}" target="_self" rel="opener nofollow">Read</a>')
                self.assertIn('target="_blank"', result)
                self.assertIn('rel="nofollow noopener"', result)
                self.assertNotIn('rel="opener', result)

    def test_section_navigation_and_script_text_are_unchanged(self):
        source = '''<a href="#writing">Writing</a><script>const text = '<a href="https://example.com">';</script>'''
        self.assertEqual(policy.open_in_new_tabs(source), source)

    def test_is_idempotent_and_preserves_surrounding_html(self):
        source = '<p>A &amp; B</p>\r\n<a\n href="https://robotair.io/">Robotair</a>'
        once = policy.open_in_new_tabs(source)
        self.assertEqual(policy.open_in_new_tabs(once), once)
        self.assertTrue(once.startswith('<p>A &amp; B</p>\r\n'))


if __name__ == '__main__':
    unittest.main()
