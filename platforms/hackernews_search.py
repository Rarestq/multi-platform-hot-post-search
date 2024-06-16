import requests
from datetime import datetime
from .platform import Platform


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

HACKERNEWS_API_URL = 'https://hn.algolia.com/api/v1/search'

class HackerNews(Platform):
    def get_posts(self, keyword):
        """
        Use the Hacker News API to fetch top stories related to the given keyword.
        """
        try:
            params = {
                'query': keyword,
                'hitsPerPage': 5  # Fetching top 5 stories
            }
            print(f"Searching HackerNews for keyword: {keyword}")
            response = requests.get(HACKERNEWS_API_URL, params=params, headers=HEADERS)
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            hits = response.json().get('hits', [])

            return [self.format_post(
                "HackerNews",
                hit.get('author', 'Unknown'),
                hit.get('title', 'No Title'),
                hit.get('points', 0),
                hit.get('url', '#'),
                created_at=self.format_timestamp(hit.get('created_at'))
            ) for hit in hits]

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from HackerNews API: {e}")
            return []
        
    def format_timestamp(self, created_at):
        """
        Format the timestamp from HackerNews time format to a readable string.
        """
        created_at_datetime = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
        return created_at_datetime.strftime("%Y-%m-%d %H:%M:%S")