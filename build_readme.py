#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import feedparser
from datetime import datetime

class ProfileBuilder:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        # Main (Chinese) feeds
        self.blog_rss_url = "https://pi-dal.com/blog-feed.xml"
        self.books_rss_url = "https://pi-dal.com/books-feed.xml"
        # English feeds for bilingual title pairing
        self.blog_en_rss_url = "https://pi-dal.com/en/blog-feed.xml"
        self.books_en_rss_url = "https://pi-dal.com/en/books-feed.xml"

    def _parse_date(self, published_str):
        """Try multiple date formats and return YYYY-MM-DD or 'Recent'."""
        if not published_str:
            return 'Recent'
        date_str = re.sub(r'[+-]\d{2}:?\d{2}$', '', published_str)
        date_str = date_str.replace('Z', '')
        for fmt in ['%a, %d %b %Y %H:%M:%S %Z', '%a, %d %b %Y %H:%M:%S GMT',
                     '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%a, %d %b %Y %H:%M:%S']:
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00')).strftime('%Y-%m-%d')
        except Exception:
            return 'Recent'

    def _fetch_feed(self, url, limit=8):
        """Fetch and parse an RSS feed, returning list of {title, link, published}."""
        try:
            feed = feedparser.parse(url)
            entries = feed.entries[:limit] if limit else feed.entries
            posts = []
            for entry in entries:
                published = entry.get('published', '') or entry.get('pubDate', '') or entry.get('updated', '')
                posts.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': published,
                })
            return posts
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return []

    @staticmethod
    def _normalize_link(link):
        """Strip locale prefix from a URL for cross-locale matching."""
        return re.sub(r'/(zh|en|ja)/', '/', link)

    def _build_title_map(self, entries):
        """Build a dict mapping normalized link → title from a list of entries."""
        result = {}
        for e in entries:
            key = self._normalize_link(e['link'])
            result[key] = e['title']
        return result

    def _dedup_and_merge(self, zh_entries, en_entries, limit=8):
        """
        Merge zh and en entries by normalized link. Produce bilingual titles
        "中文标题（English Title）" when EN title exists and differs.
        Deduplicate by canonical link (first-seen order preserved).
        """
        en_titles = self._build_title_map(en_entries)
        seen = set()
        result = []
        for entry in zh_entries:
            link = entry.get('link', '')
            key = self._normalize_link(link)
            if key in seen or not link:
                continue
            seen.add(key)
            en_title = en_titles.get(key)
            zh_title = entry['title']
            if en_title and en_title != zh_title and re.search(r'[a-zA-Z]', en_title):
                display_title = f"{zh_title}（{en_title}）"
            else:
                display_title = zh_title
            entry['display_title'] = display_title
            result.append(entry)
            if len(result) >= limit:
                break
        return result

    def fetch_blog_posts(self, limit=8):
        """Fetch Chinese blog posts, paired with English titles."""
        zh = self._fetch_feed(self.blog_rss_url, limit * 2)
        en = self._fetch_feed(self.blog_en_rss_url, limit * 2)
        return self._dedup_and_merge(zh, en, limit)

    def fetch_reading_posts(self, limit=8):
        """Fetch Chinese reading notes, paired with English titles."""
        zh = self._fetch_feed(self.books_rss_url, limit * 2)
        en = self._fetch_feed(self.books_en_rss_url, limit * 2)
        return self._dedup_and_merge(zh, en, limit)

    def generate_blog_section(self, posts):
        if not posts:
            return "<!-- BLOG-POST-LIST:START -->\n<!-- No recent posts available -->\n<!-- BLOG-POST-LIST:END -->"
        content = "<!-- BLOG-POST-LIST:START -->\n"
        for post in posts:
            formatted_date = self._parse_date(post.get('published'))
            content += f"- [{post['display_title']}]({post['link']}) - {formatted_date}\n"
        content += "- [...](https://pi-dal.com/zh/posts)\n"
        content += "<!-- BLOG-POST-LIST:END -->"
        return content

    def generate_reading_section(self, posts):
        if not posts:
            return "<!-- READING-LIST:START -->\n<!-- No recent reading posts available -->\n<!-- READING-LIST:END -->"
        content = "<!-- READING-LIST:START -->\n"
        for post in posts:
            formatted_date = self._parse_date(post.get('published'))
            content += f"- [{post['display_title']}]({post['link']}) - {formatted_date}\n"
        content += "- [...](https://pi-dal.com/zh/books)\n"
        content += "<!-- READING-LIST:END -->"
        return content

    def update_readme(self):
        readme_path = 'README.md'
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print("README.md not found")
            return

        blog_posts = self.fetch_blog_posts()
        reading_posts = self.fetch_reading_posts()

        blog_section = self.generate_blog_section(blog_posts)
        reading_section = self.generate_reading_section(reading_posts)

        content = re.sub(
            r'<!-- BLOG-POST-LIST:START -->.*?<!-- BLOG-POST-LIST:END -->',
            blog_section, content, flags=re.DOTALL)
        content = re.sub(
            r'<!-- READING-LIST:START -->.*?<!-- READING-LIST:END -->',
            reading_section, content, flags=re.DOTALL)

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("README.md updated successfully!")

if __name__ == "__main__":
    ProfileBuilder().update_readme()
