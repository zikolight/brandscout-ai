import requests
from bs4 import BeautifulSoup
import json
import time

class RedditScraper:
    """Scrape Reddit without API - uses public JSON endpoints"""
    
    def __init__(self):
        self.base_url = "https://www.reddit.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_subreddit(self, subreddit_name, query, limit=50):
        """
        Search a subreddit without API key
        Uses Reddit's public JSON endpoint
        """
        try:
            # Reddit provides JSON at .json endpoint
            url = f"{self.base_url}/r/{subreddit_name}/search.json"
            params = {
                'q': query,
                'restrict_sr': 'on',
                'sort': 'relevance',
                'limit': min(limit, 100),
                't': 'year'  # time filter: year
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            posts = []
            
            for post in data['data']['children']:
                post_data = post['data']
                
                # Get top comments
                comments = self._get_comments(subreddit_name, post_data['id'])
                
                posts.append({
                    'title': post_data.get('title', ''),
                    'body': post_data.get('selftext', ''),
                    'score': post_data.get('score', 0),
                    'comments': comments,
                    'url': f"{self.base_url}{post_data.get('permalink', '')}"
                })
                
                # Be nice to Reddit servers
                time.sleep(1)
            
            return posts
            
        except Exception as e:
            print(f"Error scraping Reddit: {e}")
            return []
    
    def _get_comments(self, subreddit, post_id, limit=5):
        """Get top comments from a post"""
        try:
            url = f"{self.base_url}/r/{subreddit}/comments/{post_id}.json"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            comments = []
            
            # Comments are in second element of response
            if len(data) > 1 and 'data' in data[1]:
                comment_data = data[1]['data']['children']
                
                for comment in comment_data[:limit]:
                    if comment['kind'] == 't1':  # t1 = comment
                        body = comment['data'].get('body', '')
                        if body and body != '[deleted]' and body != '[removed]':
                            comments.append(body)
            
            return comments
            
        except Exception as e:
            print(f"Error getting comments: {e}")
            return []
    
    def get_hot_posts(self, subreddit_name, limit=25):
        """Get hot posts from a subreddit"""
        try:
            url = f"{self.base_url}/r/{subreddit_name}/hot.json"
            params = {'limit': min(limit, 100)}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            posts = []
            
            for post in data['data']['children']:
                post_data = post['data']
                posts.append({
                    'title': post_data.get('title', ''),
                    'body': post_data.get('selftext', ''),
                    'score': post_data.get('score', 0),
                    'url': f"{self.base_url}{post_data.get('permalink', '')}"
                })
            
            return posts
            
        except Exception as e:
            print(f"Error getting hot posts: {e}")
            return []
