import requests
import os

class PerplexityClient:
    def __init__(self):
        self.api_key = os.getenv('PERPLEXITY_API_KEY')
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY not found")
        
        self.url = 'https://api.perplexity.ai/chat/completions'
    
    def search(self, query):
        """Standard search"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'sonar',
            'messages': [
                {
                    'role': 'system',
                    'content': 'Be precise and concise. Cite sources.'
                },
                {
                    'role': 'user',
                    'content': query
                }
            ]
        }
        
        try:
            response = requests.post(self.url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"
    
    def search_reddit(self, subreddit, topic, num_examples=10):
        """
        Search Reddit via Perplexity
        Perplexity can access Reddit without API keys!
        """
        query = f"""
        Search Reddit's r/{subreddit} for discussions about {topic}.
        
        Find {num_examples} real user comments or posts that mention:
        - Frustrations
        - Problems they're facing
        - What they wish existed
        - Complaints about current solutions
        
        For each, provide:
        1. The actual quote (verbatim if possible)
        2. The main frustration
        3. Context
        
        Format as a list with quotes.
        """
        
        return self.search(query)
    
    def find_pain_points(self, category, keywords):
        """
        Use Perplexity to find pain points across Reddit
        """
        query = f"""
        Search Reddit for people discussing problems with {category}.
        
        Keywords to search: {keywords}
        
        Find 10 examples of people expressing:
        - Frustration with current products
        - Unmet needs
        - Desired features that don't exist
        - Complaints
        
        Return actual user quotes and the subreddit they're from.
        """
        
        return self.search(query)
