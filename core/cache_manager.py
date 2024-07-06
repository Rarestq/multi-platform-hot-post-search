from flask_caching import Cache
from flask_apscheduler import APScheduler
from .config import Config
from .main import optimized_search_hot_posts
from .utils import generate_cache_key, get_default_platforms

cache = Cache()
scheduler = APScheduler()

@scheduler.task('cron', id='cache_preheating', minute='*/30')
def preheating_task():
    """
    Scheduled task to preheat the cache for hot keywords every 30 minutes.
    This helps in reducing response time for frequently searched keywords.
    """
    default_platforms = get_default_platforms()
    for keyword in Config.HOT_KEYWORDS:
        cache_key = generate_cache_key(keyword, default_platforms)
        if not cache.get(cache_key):
            # If the keyword is not in cache, perform a search and cache the results
            results, search_times = optimized_search_hot_posts(keyword, default_platforms)
            response = {
                "results": results,
                "search_times": search_times
            }
            cache.set(cache_key, response)