import tweepy
import os
from dotenv import load_dotenv
from .platform import Platform

load_dotenv()

class Twitter(Platform):
    def __init__(self):
        """
        Initialize the Twitter API client.
        """
        TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
        TWITTER_API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
        TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
        TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def get_posts(self, keyword):
        """
        Use the Twitter API to fetch popular tweets related to the given keyword.
        """
        tweets = self.api.search_tweets(q=keyword, result_type='popular', count=5)
        return [self.format_post(
            "Twitter",
            tweet.user.screen_name,
            tweet.text,
            tweet.favorite_count,
            f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
        ) for tweet in tweets]
