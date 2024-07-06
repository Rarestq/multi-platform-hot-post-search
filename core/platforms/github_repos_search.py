import requests
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from .platform import Platform

load_dotenv()

class GitHub(Platform):
    def __init__(self):
        """
        Initialize the GitHub API client.
        """
        self.github_token = os.getenv('GITHUB_API_TOKEN')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            "Authorization": f"token {self.github_token}",
            'Accept': 'application/vnd.github.v3+json'
        }

    def get_posts(self, keyword):
        """
        Use the GitHub API to fetch top repositories related to the given keyword.
        """
        print(f"Searching GitHub for keyword: {keyword}\n")
        
        # see: https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28#search-repositories
        # or REST API end points for search: https://docs.github.com/en/rest/search?apiVersion=2022-11-28
        url = "https://api.github.com/search/repositories"
        params = {
            "q": f"{keyword} in:name,description,topics,readme",
            "sort": "stars",
            "order": "desc",
            "per_page": 5
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return []
        
        repositories = response.json().get("items", [])
        
        return [self.format_post(
            "GitHub",
            repo['owner']['login'],
            repo['name'],
            repo['stargazers_count'],
            repo['html_url'],
            created_at=self.format_timestamp(repo['created_at'])
        ) for repo in repositories]

    def format_timestamp(self, timestamp):
        """
        Format the timestamp from GitHub's UTC format to a readable string.
        """
        utc_time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        return utc_time.strftime('%Y-%m-%d %H:%M:%S')
    
    def requires_translation(self):
        return False