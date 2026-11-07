import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from publish import ArticleText, clusters, similarity, source_quote, verify_claims, looks_hungarian, editorial_sentences, audit_passes, evidence_catalog, resolve_evidence_ids


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

    def test_looser_titles_still_need_two_shared_terms(self):
        now = datetime.now(timezone.utc).isoformat()
        entries = [
            {"source":"A","category":"gaming","original_title":"Nier Automata update inflates PC file size to 366GB","url":"https://a.test/nier","published_at":now},
            {"source":"B","category":"gaming","original_title":"Nier Automata dev working on fix for bloated 366GB PC update","url":"https://b.test/nier","published_at":now},
            {"source":"C","category":"gaming","original_title":"Mass Effect composer releases farewell trailer","url":"https://c.test/mass","published_at":now},
            {"source":"D","category":"gaming","original_title":"Mass Effect truck arrives at EA headquarters","url":"https://d.test/mass","published_at":now},
        ]
        groups = clusters(entries, [])
        self.assertEqual(len(groups), 1)
        self.assertEqual({x["source"] for x in groups[0]}, {"A", "B"})

    def test_political_titles_are_excluded(self):
        now = datetime.now(timezone.utc).isoformat()
        entries = [{"source": name, "category":"bulvar", "original_title":title,
                    "url":f"https://{name.lower()}.test/news", "published_at":now}
                   for name, title in [("A", "Bill Maher reacts to Trump election result"),
                                       ("B", "Trump election result prompts Bill Maher reaction")]]
        self.assertEqual(clusters(entries, []), [])

    def test_retracted_story_is_not_reconsidered(self):
        now = datetime.now(timezone.utc).isoformat()
        urls = [
            "https://www.ign.com/articles/ea-hq-graced-with-save-mass-effect-truck-as-n7-day-looms",
            "https://kotaku.com/save-mass-effect-ea-bioware-redwood-truck-billboard-2000754705",
        ]
        entries = [{"source":source,"category":"gaming","original_title":"Save Mass Effect truck arrives at EA HQ",
                    "url":url,"published_at":now} for source,url in zip(("IGN","Kotaku"),urls)]
        self.assertEqual(clusters(entries, []), [])

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

    def test_hungarian_language_gate(self):
        english = "Warren Spector argued that the executives had made decisions without accountability. "
        hungarian = "A fejlesztők szerint a stúdió új játékot mutatott be, és az első képek már elérhetők. "
        self.assertFalse(looks_hungarian("EA executives criticize closure", english, [english * 5]))
        self.assertTrue(looks_hungarian("Új játékot mutatott be a stúdió", hungarian, [hungarian * 5]))

    def test_audit_must_cover_every_sentence(self):
        draft = {"title":"Rövid cím", "excerpt":"Az adat kb. 50 GB-ról 366 GB-ra nőtt.",
                 "body":["Az első mondat. A második mondat.", "A harmadik mondat."]}
        sentences = editorial_sentences(draft)
        self.assertEqual(len(sentences), 5)
        self.assertIn("kb. 50 GB-ról", sentences[1])
        checks = [{"index":i,"supported":True,"issue":""} for i in range(5)]
        self.assertTrue(audit_passes({"checks":checks}, len(sentences)))
        self.assertFalse(audit_passes({"checks":checks[:-1]}, len(sentences)))
        checks[2]["supported"], checks[2]["issue"] = False, "A szám hibás"
        self.assertFalse(audit_passes({"checks":checks}, len(sentences)))

    def test_evidence_ids_resolve_to_exact_source_passages(self):
        texts = [
            ({"source":"A","url":"https://a.test/story","original_title":"Galaxy Quest gets a new release date"},
             "The studio announced a new release date for Galaxy Quest. Players will receive the update on Friday."),
            ({"source":"B","url":"https://b.test/story","original_title":"New Galaxy Quest date announced"},
             "Galaxy Quest will arrive on Friday, the publisher confirmed.")
        ]
        sources, catalog = evidence_catalog(texts)
        self.assertEqual(len(sources), 2)
        chosen_id = sources[0]["passages"][1]["id"]
        claims = [{"text":"Megjelenés", "evidence":[{"id":chosen_id}]}]
        self.assertTrue(resolve_evidence_ids(claims, catalog))
        self.assertEqual(claims[0]["evidence"][0], catalog[chosen_id])
        self.assertTrue(verify_claims(claims, {item["url"]: item["original_title"] + "\n" + body for item, body in texts}))
        self.assertFalse(resolve_evidence_ids([{"evidence":[{"id":"invented"}]}], catalog))

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
