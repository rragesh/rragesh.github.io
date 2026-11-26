import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import build_pages

spec = importlib.util.spec_from_file_location("medium", Path(__file__).parents[1] / "scripts/update_medium.py")
medium = importlib.util.module_from_spec(spec)
spec.loader.exec_module(medium)


def feed(link="https://rragesh.medium.com/story", title="A &amp; B", body="A robotics article."):
    return f'''<rss xmlns:content="http://purl.org/rss/1.0/modules/content/"><channel><item>
      <title>{title}</title><link>{link}</link><pubDate>Thu, 28 May 2026 06:51:00 GMT</pubDate>
      <category>robotics</category><content:encoded><![CDATA[<p>{body}</p>]]></content:encoded>
      </item></channel></rss>'''


class MediumTests(unittest.TestCase):
    def test_rss_becomes_escaped_accessible_previews(self):
        posts = medium.parse_feed(feed(body='Useful &amp; practical <script>bad()</script> ideas.'))
        self.assertEqual(posts[0]["date"], "2026-05-28")
        self.assertEqual(posts[0]["topics"], ["Robotics"])
        self.assertNotIn("bad()", posts[0]["excerpt"])
        rendered = medium.render_posts(posts)
        self.assertIn("A &amp; B", rendered)
        self.assertIn("utm_source=rragesh.github.io", rendered)
        self.assertNotIn("<script>", rendered)

    def test_rejects_non_medium_and_script_links(self):
        for link in ("javascript:alert(1)", "https://medium.com.evil.test/story", "http://medium.com/story"):
            with self.subTest(link=link), self.assertRaises(ValueError):
                medium.parse_feed(feed(link=link))

    def test_empty_and_malformed_feeds_fail_without_rendering(self):
        for content in ("<rss><channel/></rss>", "not xml"):
            with self.subTest(content=content), self.assertRaises(Exception):
                medium.parse_feed(content)

    def test_only_preview_region_changes(self):
        document = "before" + medium.START + "old" + medium.END + "after"
        result = medium.replace_previews(document, "new")
        self.assertTrue(result.startswith("before" + medium.START))
        self.assertTrue(result.endswith(medium.END + "after"))
        self.assertNotIn("old", result)
        with self.assertRaises(ValueError):
            medium.replace_previews("no markers", "new")

    def test_ignores_tracking_pixels(self):
        parser = medium.PreviewParser()
        parser.feed('<img src="https://medium.com/_/stat?event=view"><img src="https://cdn-images-1.medium.com/max/800/cover.png">')
        self.assertEqual(parser.image, "https://cdn-images-1.medium.com/max/800/cover.png")

    def test_refresh_updates_writing_without_reintroducing_articles_on_home(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('PANE_SCRATCH_DIR')) as directory:
            root = Path(directory)
            (root / 'data/pages').mkdir(parents=True)
            (root / 'index.html').write_text('<h1>Hero only</h1>')
            source = root / 'data/pages/writing.html'
            source.write_text('Writing intro' + medium.START + 'old' + medium.END + 'Contact links')
            manifest = root / 'data/pages.json'
            manifest.write_text(json.dumps([{
                'key': 'writing', 'file': 'writing.html', 'title': 'Writing',
                'description': 'Notes', 'bodyClass': 'content-page',
                'image': 'img/speaker.jpg', 'imageAlt': 'Speaker', 'graph': [],
            }]))
            rss = root / 'feed.xml'
            rss.write_text(feed())
            with patch.object(medium, 'ROOT', root), patch.object(build_pages, 'MANIFEST', manifest), patch.object(sys, 'argv', ['update_medium.py', '--feed-file', str(rss)]), patch('builtins.print'):
                self.assertEqual(medium.main(), 0)
                self.assertEqual((root / 'index.html').read_text(), '<h1>Hero only</h1>')
                self.assertIn('A &amp; B', source.read_text())
                output = (root / 'writing.html').read_text()
                self.assertIn('Writing intro', output)
                self.assertIn('Contact links', output)
                self.assertIn('Read on Medium', output)
                self.assertEqual(len(json.loads((root / 'data/medium-posts.json').read_text())), 1)
                last_source = source.read_text()
                rss.write_text('<rss><channel/></rss>')
                self.assertEqual(medium.main(), 1)
                self.assertEqual((root / 'writing.html').read_text(), output)
                self.assertEqual(source.read_text(), last_source)


if __name__ == "__main__":
    unittest.main()
