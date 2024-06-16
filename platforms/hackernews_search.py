import requests
from datetime import datetime, timezone
from .platform import Platform

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# HACKERNEWS_API_URL_BY_DATE = 'http://hn.algolia.com/api/v1/search_by_date'
HACKERNEWS_API_URL = 'http://hn.algolia.com/api/v1/search'

class HackerNews(Platform):
    def get_posts(self, keyword):
        """
        Use the Hacker News API to fetch top stories related to the given keyword.
        """
        try:
            params = {
                'query': keyword,
                'tags': 'story',
                'hitsPerPage': 50  # Fetching more stories to sort by date later
            }
            print(f"Searching HackerNews for keyword: {keyword}")
            
            response = requests.get(HACKERNEWS_API_URL, params=params, headers=HEADERS)
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            hits = response.json().get('hits', [])
            
            # Sort hits by 'points' and 'created_at' fields in descending order (highest score and newest first)
            sorted_hits = sorted(hits, key=lambda x: (x.get('points', 0), x.get('created_at_i', 0)), reverse=True)

            # Select the top 5 hits after sorting
            top_hits = sorted_hits[:5]

            return [self.format_post(
                "HackerNews",
                hit.get('author', 'Unknown'),
                hit.get('title', 'No Title'),
                hit.get('points', 0),
                hit.get('url', '#'),
                created_at=self.format_timestamp(hit.get('created_at_i', 0))
            ) for hit in top_hits]

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from HackerNews API: {e}")
            return []
        
    def format_timestamp(self, timestamp):
        """
        Format the timestamp from HackerNews's UTC format to a readable string.
        """
        if timestamp == 0:
            return "Unknown"
        utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return utc_time.strftime('%Y-%m-%d %H:%M:%S')
