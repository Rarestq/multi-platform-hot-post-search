from platforms.reddit_search import Reddit
from platforms.hackernews_search import HackerNews
from platforms.github_repos_search import GitHub
from platforms.theresanaiforthat_search import TheresAnAIForThat
from platforms.v2ex_search import V2EX
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate
import re
import concurrent.futures
import time

load_dotenv()

class PostSearcher:
    def __init__(self):
        """
        Initialize PostSearcher with an empty list of platforms and translator.
        """
        self.platforms = []
        self.translator = translate.Client()

    def register_platform(self, platform):
        """
        Register a platform by adding it to the list of platforms.
        """
        self.platforms.append(platform)
        
    def translate_keyword(self, keyword):
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
        except Exception as e:
            print(f"Error detecting or translating language: {e}")
            return keyword  # In case of an error, return the original keyword
        
    def is_english(self, keyword):
        """
        Check if the keyword is an English word or phrase.
        """
        return re.match(r'^[a-zA-Z\s]+$', keyword) is not None


    def search(self, keyword):
        """
        Search for posts related to the given keyword across all registered platforms, 
        and return the top five posts sorted by metrics.
        """
        all_posts = []
        for platform in self.platforms:
            if platform.requires_translation():
                translated_keyword = self.translate_keyword(keyword)
                all_posts.extend(platform.get_posts(translated_keyword))
            else:
                all_posts.extend(platform.get_posts(keyword))
        return all_posts

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
    
    top_posts = searcher.search(keyword)
    
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
    
    return formatted_posts

def optimized_search_hot_posts(keyword, platforms):
    searcher = initialize_searcher()

    if platforms:
        searcher.platforms = [p for p in searcher.platforms if p.__class__.__name__.lower() in platforms]

    all_posts = []
    search_times = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_platform = {}
        for platform in searcher.platforms:
            if platform.requires_translation():
                translated_keyword = searcher.translate_keyword(keyword)
                future = executor.submit(platform.get_posts, translated_keyword)
            else:
                future = executor.submit(platform.get_posts, keyword)
            future_to_platform[future] = platform

        for future in concurrent.futures.as_completed(future_to_platform):
            platform = future_to_platform[future]
            start_time = time.perf_counter()
            try:
                posts = future.result()
                all_posts.extend(posts)
            except Exception as exc:
                print(f'{platform.__class__.__name__} generated an exception: {exc}')
            end_time = time.perf_counter()
            search_times[platform.__class__.__name__] = round((end_time - start_time) * 1000, 2)  # transfer to milliseconds

    # Format the results
    formatted_posts = []
    for post in all_posts:
        formatted_post = {
            "platform": post['platform'],
            "author": post['author'],
            "title": post['title'],
            "metrics": post['metrics'],
            "link": post['link'],
            "created_at": post['created_at']
        }
        formatted_posts.append(formatted_post)

    return formatted_posts, search_times

# This part is optional, you can keep it for local testing
if __name__ == "__main__":
    keyword = input("Please enter the keyword you want to search for: ")
    results = search_hot_posts(keyword)
    for post in results:
        print(f"Platform: {post['platform']}")
        print(f"Author: {post['author']}")
        print(f"Title: {post['title']}")
        print(f"Metrics: {post['metrics']}")
        print(f"Link: {post['link']}")
        print(f"Post: {post['created_at']}")
        print("---")