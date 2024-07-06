from .platforms.reddit_search import Reddit
from .platforms.hackernews_search import HackerNews
from .platforms.github_repos_search import GitHub
from .platforms.theresanaiforthat_search import TheresAnAIForThat
from .platforms.v2ex_search import V2EX
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate
import re
import concurrent.futures
import time
import logging
from functools import lru_cache

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Translator:
    def __init__(self):
        """
        Initialize Translator with a translate client.
        """
        self.translator = translate.Client()
        
    @lru_cache(maxsize=100)
    def translate_keyword(self, keyword: str) -> str:
        """
        Translate the keyword to English if it is not in English.
        """
        try:
            if self.is_english(keyword):
                return keyword  # Keyword only contains English letters
            else:
                # Translate the keyword to English
                translation = self.translator.translate(keyword, target_language='en')
                return translation['translatedText']
        except translate.exceptions.GoogleCloudError as e:
            logger.error(f"Error translating keyword: {e}")
            return keyword  # In case of an error, return the original keyword
        
    @staticmethod
    def is_english(keyword: str) -> bool:
        """
        [simple] Check if the keyword is an English word or phrase.
        """
        return re.match(r'^[a-zA-Z\s]+$', keyword.replace(' ', '')) is not None
    
class PostSearcher:
    def __init__(self):
        self.platforms = []
        self.translator = Translator()

    def register_platform(self, platform):
        self.platforms.append(platform)

    def search(self, keyword: str):
        all_posts = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.platforms)) as executor:
            future_to_platform = {executor.submit(self.search_platform, platform, keyword): platform for platform in self.platforms}
            for future in concurrent.futures.as_completed(future_to_platform):
                platform = future_to_platform[future]
                try:
                    posts = future.result()
                    all_posts.extend(posts)
                except Exception as exc:
                    logger.error(f'{platform.__class__.__name__} generated an exception: {exc}')
        return all_posts

    def search_platform(self, platform, keyword: str):
        if platform.requires_translation():
            translated_keyword = self.translator.translate_keyword(keyword)
            return platform.get_posts(translated_keyword)
        else:
            return platform.get_posts(keyword)

def initialize_searcher():
    searcher = PostSearcher()
    searcher.register_platform(Reddit())
    searcher.register_platform(HackerNews())
    searcher.register_platform(GitHub())
    searcher.register_platform(TheresAnAIForThat())
    searcher.register_platform(V2EX())
    
    return searcher

def search_hot_posts(keyword, platforms=None):
    searcher = initialize_searcher()
    
    if platforms:
        searcher.platforms = [p for p in searcher.platforms if p.__class__.__name__.lower() in platforms]
    
    start_time = time.time()
    top_posts = searcher.search_platform(keyword)
    end_time = time.time()
    total_time = round((end_time - start_time) * 1000, 2)
    
    formatted_posts = []
    for post in top_posts:
        formatted_post = {
            "platform": post['platform'],
            "author": post['author'],
            "title": post['title'],
            "metrics": post['metrics'],
            "link": post['link'],
            "created_at": post['created_at']
        }
        formatted_posts.append(formatted_post)
    
    return formatted_posts, {"total_time": total_time}

def optimized_search_hot_posts(keyword: str, platforms: list):
    """
    Perform an optimized search for hot posts across specified platforms.

    Args:
        keyword (str): The search keyword.
        platforms (list): List of platforms to search.

    Returns:
        tuple: A tuple containing formatted posts and search timing information.
    """
    # Initialize the searcher with specified platforms
    searcher = initialize_searcher()
    
    if platforms:
        searcher.platforms = [p for p in searcher.platforms if p.__class__.__name__.lower() in platforms]

    # Perform the search and measure the time taken
    start_time = time.time()
    all_posts = searcher.search(keyword)
    end_time = time.time()
    total_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds

    # Format the search results
    formatted_posts = [
        {
            "platform": post['platform'],
            "author": post['author'],
            "title": post['title'],
            "metrics": post['metrics'],
            "link": post['link'],
            "created_at": post['created_at']
        } for post in all_posts
    ]

    return formatted_posts, {"total_time": total_time}

# This part is optional, you can keep it for local testing
if __name__ == "__main__":
    keyword = input("Please enter the keyword you want to search for: ")
    results, timing = optimized_search_hot_posts(keyword, None)
    for post in results:
        print(f"Platform: {post['platform']}")
        print(f"Author: {post['author']}")
        print(f"Title: {post['title']}")
        print(f"Metrics: {post['metrics']}")
        print(f"Link: {post['link']}")
        print(f"Post: {post['created_at']}")
        print("---")
    print(f"Total search time: {timing['total_time']} ms")