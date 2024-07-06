import concurrent.futures
import time
import logging
from core.translator import Translator
from core.platforms.reddit_search import Reddit
from core.platforms.hackernews_search import HackerNews
from core.platforms.github_repos_search import GitHub
from core.platforms.theresanaiforthat_search import TheresAnAIForThat
from core.platforms.v2ex_search import V2EX

logger = logging.getLogger(__name__)

class PostSearcher:
    def __init__(self):
        self.platforms = [Reddit(), HackerNews(), GitHub(), TheresAnAIForThat(), V2EX()]
        self.translator = Translator()

    def search_posts(self, keyword: str, platforms=None):
        if platforms:
            self.platforms = [p for p in self.platforms if p.__class__.__name__.lower() in platforms]

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
        
def search_hot_posts(keyword, platforms=None):
    searcher = PostSearcher()
    
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
    searcher = PostSearcher()
    
    start_time = time.time()
    all_posts = searcher.search_posts(keyword, platforms)
    end_time = time.time()
    total_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds

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