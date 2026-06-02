#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import requests
import feedparser
from datetime import datetime, timezone
import json

class ProfileBuilder:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.blog_rss_url = "https://pi-dal.com/blog-feed.xml"
        self.books_rss_url = "https://pi-dal.com/books-feed.xml"
        
    def fetch_blog_posts(self, limit=8):
        """Fetch blog posts from RSS feed"""
        try:
            feed = feedparser.parse(self.blog_rss_url)
            posts = []

            entries = feed.entries[:limit] if limit else feed.entries
            for entry in entries:
                # Debug: print available date fields
                published_date = entry.get('published', '')
                if not published_date:
                    # Try other common date fields
                    published_date = entry.get('pubDate', '')
                if not published_date:
                    published_date = entry.get('updated', '')
                    
                
                post = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': published_date,
                    'summary': entry.get('summary', '')[:100] + '...' if entry.get('summary') else ''
                }
                posts.append(post)
            
            return posts
        except Exception as e:
            print(f"Error fetching blog posts: {e}")
            return []

    def fetch_english_titles(self):
        """Fetch English titles from English RSS feed, keyed by slug"""
        try:
            feed = feedparser.parse('https://pi-dal.com/en/feed.xml')
            titles = {}
            for entry in feed.entries:
                # Extract slug from URL (e.g. /en/posts/Slug -> Slug)
                slug = entry.link.rstrip('/').split('/')[-1]
                titles[slug] = entry.title
            return titles
        except Exception as e:
            print(f"Error fetching English titles: {e}")
            return {}
    
    def fetch_reading_posts(self, limit=8):
        """Fetch recent reading posts from books RSS feed"""
        try:
            feed = feedparser.parse(self.books_rss_url)
            posts = []

            for entry in feed.entries[:limit]:
                # Debug: print available date fields
                published_date = entry.get('published', '')
                if not published_date:
                    # Try other common date fields
                    published_date = entry.get('pubDate', '')
                if not published_date:
                    published_date = entry.get('updated', '')
                    
                
                post = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': published_date,
                    'summary': entry.get('summary', '')[:100] + '...' if entry.get('summary') else ''
                }
                posts.append(post)
            
            return posts
        except Exception as e:
            print(f"Error fetching reading posts: {e}")
            return []
    
    
    def generate_blog_section(self, posts):
        """Generate blog posts section"""
        if not posts:
            return "<!-- BLOG-POST-LIST:START -->\n<!-- No recent posts available -->\n<!-- BLOG-POST-LIST:END -->"

        # Fetch English titles for bilingual display
        en_titles = self.fetch_english_titles()
        
        content = "<!-- BLOG-POST-LIST:START -->\n"
        for post in posts:
            # Parse date for better formatting
            try:
                if post['published']:
                    # Try multiple date formats that xlog might use
                    date_str = post['published']
                    # Remove timezone info if present and try parsing
                    date_str = re.sub(r'[+-]\d{2}:?\d{2}$', '', date_str)
                    date_str = date_str.replace('Z', '')
                    
                    # Try different formats
                    for fmt in ['%a, %d %b %Y %H:%M:%S %Z', '%a, %d %b %Y %H:%M:%S GMT', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%a, %d %b %Y %H:%M:%S']:
                        try:
                            pub_date = datetime.strptime(post['published'].strip(), fmt)
                            formatted_date = pub_date.strftime('%Y-%m-%d')
                            break
                        except ValueError as e:
                            continue
                    else:
                        # If all parsing attempts fail, try the original method
                        try:
                            pub_date = datetime.fromisoformat(post['published'].replace('Z', '+00:00'))
                            formatted_date = pub_date.strftime('%Y-%m-%d')
                        except Exception as e:
                            formatted_date = 'Recent'
                else:
                    formatted_date = 'Recent'
            except:
                formatted_date = 'Recent'
            
            # Build title with English translation if available
            # Match by extracting slug from URL
            slug = post['link'].rstrip('/').split('/')[-1]
            en_title = en_titles.get(slug)
            if en_title and en_title != post['title']:
                display_title = f"{post['title']}（{en_title}）"
            else:
                display_title = post['title']
            
            content += f"- [{display_title}]({post['link']}) - {formatted_date}\n"
        
        # Add ellipsis link to see more posts
        content += "- [...](https://pi-dal.com/posts)\n"
        content += "- 语言入口（Locale Links）: [中文（Chinese）](https://pi-dal.com/zh/posts) · [英文（English）](https://pi-dal.com/en/posts) · [日文（Japanese）](https://pi-dal.com/ja/posts)\n"
        content += "<!-- BLOG-POST-LIST:END -->"
        return content
    
    def generate_reading_section(self, posts):
        """Generate reading posts section"""
        if not posts:
            return "<!-- READING-LIST:START -->\n<!-- No recent reading posts available -->\n<!-- READING-LIST:END -->"
        
        content = "<!-- READING-LIST:START -->\n"
        for post in posts:
            # Parse date for better formatting
            try:
                if post['published']:
                    # Try multiple date formats that xlog might use
                    date_str = post['published']
                    # Remove timezone info if present and try parsing
                    date_str = re.sub(r'[+-]\d{2}:?\d{2}$', '', date_str)
                    date_str = date_str.replace('Z', '')
                    
                    # Try different formats
                    for fmt in ['%a, %d %b %Y %H:%M:%S %Z', '%a, %d %b %Y %H:%M:%S GMT', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%a, %d %b %Y %H:%M:%S']:
                        try:
                            pub_date = datetime.strptime(post['published'].strip(), fmt)
                            formatted_date = pub_date.strftime('%Y-%m-%d')
                            break
                        except ValueError as e:
                            continue
                    else:
                        # If all parsing attempts fail, try the original method
                        try:
                            pub_date = datetime.fromisoformat(post['published'].replace('Z', '+00:00'))
                            formatted_date = pub_date.strftime('%Y-%m-%d')
                        except Exception as e:
                            formatted_date = 'Recent'
                else:
                    formatted_date = 'Recent'
            except:
                formatted_date = 'Recent'
            
            content += f"- [{post['title']}]({post['link']}) - {formatted_date}\n"
        
        # Add ellipsis link to see more reading notes
        content += "- [...](https://pi-dal.com/books)\n"
        content += "<!-- READING-LIST:END -->"
        return content
    
    def update_readme(self):
        """Update README.md with dynamic content"""
        readme_path = 'README.md'
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print("README.md not found")
            return
        
        # Fetch data
        blog_posts = self.fetch_blog_posts()
        reading_posts = self.fetch_reading_posts()
        
        # Generate sections
        blog_section = self.generate_blog_section(blog_posts)
        reading_section = self.generate_reading_section(reading_posts)
        
        # Update README content
        # Replace blog posts section
        content = re.sub(
            r'<!-- BLOG-POST-LIST:START -->.*?<!-- BLOG-POST-LIST:END -->',
            blog_section,
            content,
            flags=re.DOTALL
        )
        
        # Replace reading posts section
        content = re.sub(
            r'<!-- READING-LIST:START -->.*?<!-- READING-LIST:END -->',
            reading_section,
            content,
            flags=re.DOTALL
        )
        
        # Write updated content
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("README.md updated successfully!")

if __name__ == "__main__":
    builder = ProfileBuilder()
    builder.update_readme()
