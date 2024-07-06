import os
import tweepy
from dotenv import load_dotenv
from .platform import Platform 

load_dotenv()

class Twitter(Platform):
    def __init__(self):
        """
        Initialize the Twitter API client with Bearer Token.
        """
        TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
        
        auth = tweepy.OAuth2BearerHandler(bearer_token=TWITTER_BEARER_TOKEN)
        self.api = tweepy.API(auth)

    def get_posts(self, keyword):
        """
        Use the Twitter API to fetch popular tweets related to the given keyword.
        """
        tweets = self.api.search_tweets(q=keyword, result_type='popular', tweet_mode='extended', count=5)
        return [self.format_post(
            "Twitter",
            tweet.user.screen_name,
            tweet.full_text,
            tweet.favorite_count,
            f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}"
        ) for tweet in tweets]
