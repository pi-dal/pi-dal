import unittest

from build_readme import ProfileBuilder


class GenerateBlogSectionTests(unittest.TestCase):
    def test_blog_section_formats_each_post_with_merged_rss_title(self):
        """
        RSS feed now returns merged titles: "中文标题（English Title）"
        The blog section should use the RSS title directly.
        """
        builder = ProfileBuilder()

        section = builder.generate_blog_section([
            {
                "title": "2023年物竞外出培训—杭州行（2023 Physics Olympiad Training Trip — Hangzhou）",
                "link": "https://pi-dal.com/zh/posts/2023-Hangzhou-Travelling",
                "published": "2026-06-02T10:00:00",
                "summary": "example",
            },
        ])

        self.assertIn(
            "- [2023年物竞外出培训—杭州行（2023 Physics Olympiad Training Trip — Hangzhou）](https://pi-dal.com/zh/posts/2023-Hangzhou-Travelling) - 2026-06-02",
            section,
        )
        self.assertNotIn("语言入口（Locale Links）", section)

    def test_blog_section_deduplicates_by_link(self):
        """
        When upstream RSS feed returns duplicate entries (same link),
        only the first occurrence should appear in the output.
        """
        builder = ProfileBuilder()

        section = builder.generate_blog_section([
            {
                "title": "知流",
                "link": "https://pi-dal.com/zh/posts/knowledge-flow",
                "published": "2026-06-08T00:00:00",
                "summary": "test",
            },
            {
                "title": "知流",
                "link": "https://pi-dal.com/zh/posts/knowledge-flow",
                "published": "2026-06-08T00:00:00",
                "summary": "test",
            },
        ])

        # knowledge-flow should appear exactly once
        count = section.count("zh/posts/knowledge-flow")
        self.assertEqual(count, 1, f"Expected 1 occurrence of link, got {count}")


if __name__ == "__main__":
    unittest.main()
