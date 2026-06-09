import unittest

from build_readme import ProfileBuilder

class GenerateBlogSectionTests(unittest.TestCase):
    def test_blog_section_formats_each_post_with_merged_rss_title(self):
        """
        When both zh and en entries exist with same link, produce
        "中文标题（English Title）" bilingual title.
        """
        builder = ProfileBuilder()

        section = builder.generate_blog_section([
            {
                "title": "知流（The Knowledge Flow）",
                "link": "https://pi-dal.com/zh/posts/knowledge-flow",
                "published": "2026-06-08T00:00:00",
                "display_title": "知流（The Knowledge Flow）",
            },
        ])

        self.assertIn(
            "- [知流（The Knowledge Flow）](https://pi-dal.com/zh/posts/knowledge-flow) - 2026-06-08",
            section,
        )

    def test_dedup_and_merge_normalizes_locale_links(self):
        """
        _dedup_and_merge should normalize locale prefixes in links
        so that /zh/posts/x and /en/posts/x match as the same entry.
        """
        builder = ProfileBuilder()

        zh_entries = [
            {
                "title": "知流",
                "link": "https://pi-dal.com/zh/posts/knowledge-flow",
                "published": "2026-06-08T00:00:00",
            },
            # Duplicate with same zh link
            {
                "title": "知流",
                "link": "https://pi-dal.com/zh/posts/knowledge-flow",
                "published": "2026-06-08T00:00:00",
            },
        ]
        en_entries = [
            {
                "title": "The Knowledge Flow",
                "link": "https://pi-dal.com/en/posts/knowledge-flow",
                "published": "2026-06-08T00:00:00",
            },
        ]

        merged = builder._dedup_and_merge(zh_entries, en_entries, limit=10)

        # Should deduplicate to 1 entry and produce bilingual title
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["display_title"], "知流（The Knowledge Flow）")

    def test_dedup_and_merge_produces_bilingual_titles(self):
        """
        _dedup_and_merge should pair zh and en entries by link
        and produce "中文标题（English Title）" format.
        """
        builder = ProfileBuilder()

        zh_entries = [
            {
                "title": "知流",
                "link": "https://pi-dal.com/zh/posts/knowledge-flow",
                "published": "2026-06-08T00:00:00",
            },
            {
                "title": "2023年物竞外出培训—杭州行",
                "link": "https://pi-dal.com/zh/posts/2023-Hangzhou-Travelling",
                "published": "2023-07-27T00:00:00",
            },
        ]
        en_entries = [
            {
                "title": "The Knowledge Flow",
                "link": "https://pi-dal.com/en/posts/knowledge-flow",
                "published": "2026-06-08T00:00:00",
            },
            {
                "title": "2023 Physics Camp in Hangzhou",
                "link": "https://pi-dal.com/en/posts/2023-Hangzhou-Travelling",
                "published": "2023-07-27T00:00:00",
            },
        ]

        merged = builder._dedup_and_merge(zh_entries, en_entries, limit=10)

        self.assertIn("display_title", merged[0])
        self.assertEqual(merged[0]["display_title"], "知流（The Knowledge Flow）")
        self.assertEqual(merged[1]["display_title"], "2023年物竞外出培训—杭州行（2023 Physics Camp in Hangzhou）")
        self.assertEqual(len(merged), 2)

if __name__ == "__main__":
    unittest.main()
