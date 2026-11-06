import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from publish import ArticleText, clusters, similarity, source_quote, verify_claims


class PublisherSafetyTests(unittest.TestCase):
    def test_only_independent_matching_sources(self):
        now = datetime.now(timezone.utc).isoformat()
        make = lambda source, title, url: {"source": source, "category": "gaming", "original_title": title, "url": url, "published_at": now}
        entries = [make("A", "Studio announces Galaxy Quest release date for PC", "https://a.test/one"),
                   make("B", "Galaxy Quest PC release date announced by studio", "https://b.test/two"),
                   make("A", "Galaxy Quest release date confirmed", "https://a.test/three"),
                   make("C", "Actor dies after hospital stay", "https://c.test/four")]
        groups = clusters(entries, [])
        self.assertEqual(len(groups), 1)
        self.assertEqual({x["source"] for x in groups[0]}, {"A", "B"})

    def test_same_source_is_not_confirmation(self):
        now = datetime.now(timezone.utc).isoformat()
        entries = [{"source":"A","category":"gaming","original_title":"Galaxy Quest release date announced","url":f"https://a.test/{n}","published_at":now} for n in range(2)]
        self.assertEqual(clusters(entries, []), [])

    def test_article_extraction_ignores_navigation(self):
        parser = ArticleText()
        parser.feed('<nav><p>junk</p></nav><article><p>Good text.</p><script>Ignore</script><p>More text.</p></article>')
        self.assertIn("Good text.", "".join(parser.parts))
        self.assertNotIn("junk", "".join(parser.parts))
        self.assertNotIn("Ignore", "".join(parser.parts))

    def test_evidence_recovers_only_close_source_span(self):
        source = "Rockstar shares 38 new screenshots of Grand Theft Auto 6, showing Vice City."
        quote = "Rockstar shares 38 new screenshots of Grand Theft Auto VI"
        self.assertEqual(source_quote(quote, source), "Rockstar shares 38 new screenshots of Grand Theft Auto ")
        self.assertIsNone(source_quote("A completely unrelated game was cancelled yesterday", source))
        claims = [{"evidence": [{"url": "https://example.test/news/", "quote": quote}]}]
        self.assertTrue(verify_claims(claims, {"https://example.test/news": source}))
        self.assertEqual(claims[0]["evidence"][0]["url"], "https://example.test/news")


if __name__ == "__main__":
    unittest.main()
