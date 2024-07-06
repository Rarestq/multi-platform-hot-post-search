import praw
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from .platform import Platform

load_dotenv()

class Reddit(Platform):
    def __init__(self):
        """
        Initialize the Reddit API client.
        """
        REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
        REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
        REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
        
        self.reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                                  client_secret=REDDIT_CLIENT_SECRET,
                                  user_agent=REDDIT_USER_AGENT)

    def get_posts(self, keyword):
        """
        Use the Reddit API to fetch top posts related to the given keyword.
        """
        print(f"Searching Reddit for keyword: {keyword}\n")
        
        # Increase the limit to fetch more posts initially for sorting
        posts = self.reddit.subreddit('all').search(keyword, limit=50)

        # Convert posts to a list and sort them by score in descending order (highest score first)
        sorted_posts = sorted(posts, key=lambda post: (post.score, post.created_utc), reverse=True)

        # Select the top 5 newest posts
        top_posts = sorted_posts[:5]

        return [self.format_post(
            "Reddit",
            post.author.name if post.author else "Unknown",
            post.title,
            post.score,
            f"https://www.reddit.com{post.permalink}",
            created_at=self.format_timestamp(post.created_utc)
        ) for post in top_posts]
        
    def format_timestamp(self, timestamp):
        """
        Format the timestamp from Reddit's UTC format to a readable string.
        """
        utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return utc_time.strftime('%Y-%m-%d %H:%M:%S')
    
    def requires_translation(self):
        return True
