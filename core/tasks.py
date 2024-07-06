from core.utils import get_default_platforms
from core.cache import generate_cache_key, cache_get, cache_set
from core.performance import performance_monitor
from core.posts_search import optimized_search_hot_posts
from flask_apscheduler import APScheduler
from apscheduler.jobstores.base import ConflictingIdError
from concurrent.futures import ThreadPoolExecutor
import logging
import datetime
import time

thread_pool = ThreadPoolExecutor(max_workers=5)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

scheduler = APScheduler()

def init_scheduler(app):
    scheduler.init_app(app)
    scheduler.start()

def register_cache_preheat(app):
    logger.info("Registering cache preheat task...")
    
    @performance_monitor
    def trigger_cache_preheat():
        """Preheat cache for hot keywords every 30 minutes"""
        logger.info(f"Starting cache preheating. HOT_KEYWORDS: {app.config['HOT_KEYWORDS']}")
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
                logger.info(f"Preheated cache for keyword: {keyword}")
            
        logger.info("Cache preheating completed. All keywords processed.")
        
    def async_trigger_cache_preheat():
        with app.app_context():
            trigger_cache_preheat()
    
    try:
        # try to add a cron job  
        scheduler.add_job(
            id='cache_preheating',
            func=async_trigger_cache_preheat,
            trigger='cron',
            minute='*/30'
        )
    except ConflictingIdError:
        # if job exsits already, then refresh it
        scheduler.reschedule_job('cache_preheating', trigger='cron', minute='*/30')

    def immediate_execution():
        try:
            job_id = f'immediate_cache_preheating_{int(time.time())}'
            scheduler.add_job(
                func=async_trigger_cache_preheat,
                trigger='date',
                run_date=datetime.now(),
                id=job_id
            )
            logger.info(f"Immediate cache preheating job added with id: {job_id}")
        except ConflictingIdError:
            # if conflicts(extremely unlikely)， executing job directly
            logger.warning("Conflict occurred when adding immediate job, executing directly")
            async_trigger_cache_preheat()

    # execute job immediately in thread pool
    thread_pool.submit(immediate_execution)
    
    logger.info("Cache preheat task registered and immediate execution started in background.")
    
def shutdown_scheduler_and_thread_pool(app):
    @app.teardown_appcontext
    def shutdown(error=None):
        if scheduler.running:
            scheduler.shutdown()
        thread_pool.shutdown(wait=False)
        logger.info("Scheduler and thread pool shut down.")