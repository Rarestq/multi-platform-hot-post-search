from core.utils import get_default_platforms
from core.cache import generate_cache_key, cache_get, cache_set
from core.performance import performance_monitor
from core.posts_search import optimized_search_hot_posts
import logging

logger = logging.getLogger(__name__)

def register_cache_preheat(app):
    
    @app.apscheduler.task('cron', id='cache_preheating', minute='*/30')
    @performance_monitor
    def trigger_cache_preheat():
        """Preheat cache for hot keywords every 30 minutes"""
        logger.info("Starting cache preheating...")
        default_platforms = get_default_platforms()
        for keyword in app.config['HOT_KEYWORDS']:
            cache_key = generate_cache_key(keyword, default_platforms)
            if not cache_get(cache_key):
                results, search_times = optimized_search_hot_posts(keyword, default_platforms)
                response = {
                    "results": results,
                    "search_times": search_times
                }
                cache_set(cache_key, response)
                app.logger.info(f"Preheated cache for keyword: {keyword}")
            
        app.logger.info("Cache preheating completed")