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


if __name__ == "__main__":
    unittest.main()
