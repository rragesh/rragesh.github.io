import importlib.util
from pathlib import Path
import unittest

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


if __name__ == "__main__":
    unittest.main()
