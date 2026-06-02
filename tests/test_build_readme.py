import unittest

from build_readme import ProfileBuilder


class GenerateBlogSectionTests(unittest.TestCase):
    def test_blog_section_includes_chinese_with_english_gloss_locale_entry_links(self):
        builder = ProfileBuilder()

        section = builder.generate_blog_section([
            {
                "title": "Example Post",
                "link": "https://pi-dal.com/posts/example-post",
                "published": "2026-06-02T10:00:00",
                "summary": "example",
            },
        ])

        self.assertIn("- 语言入口（Locale Links）: [中文（Chinese）](https://pi-dal.com/zh/posts) · [英文（English）](https://pi-dal.com/en/posts) · [日文（Japanese）](https://pi-dal.com/ja/posts)", section)


if __name__ == "__main__":
    unittest.main()
