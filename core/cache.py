from flask import current_app
from typing import List, Optional, Any
from core.utils import get_default_platforms
import redis
import json
import logging

logger = logging.getLogger(__name__)

# global Redis client
_redis_client = None

def get_redis_client():
    """
    Retrieve or initialize the Redis client.
    
    Returns:
        A Redis client instance.
    """
    global _redis_client
    if _redis_client is None:
        redis_url = current_app.config.get('REDIS_URL', 'redis://localhost:6379/0')
        _redis_client = redis.from_url(redis_url)
    return _redis_client

def generate_cache_key(keyword: str, platforms: Optional[List[str]] = None) -> str:
    """
    Generate a unique cache key based on the search keyword and platforms.
    
    Args:
        keyword (str): The search keyword.
        platforms (List[str], optional): List of platforms to search. Defaults to None.
    
    Returns:
        str: A unique cache key string.
    """
    if platforms is None:
        platforms = get_default_platforms()
    platforms_str = '_'.join(sorted(platforms))
    return f"cache:{keyword}_cross_platforms_{platforms_str}"

def cache_get(key: str) -> Any:
    """
    Retrieve a value from the cache by key.
    
    Args:
        key (str): The cache key.
    
    Returns:
        The cached value or None if the key does not exist.
    """
    try:
        logging.info(f"cache_get for key: {key}")
        redis_client = get_redis_client()
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        current_app.logger.error(f"Error getting cache for key {key}: {e}")
        return None

def cache_set(key: str, value: Any, timeout: Optional[int] = 3600) -> None:
    """
    Set a value in the cache with an optional timeout.
    
    Args:
        key (str): The cache key.
        value: The value to cache.
        timeout (int, optional): The cache timeout in seconds. Defaults to 3600 (1 hour).
    """
    try:
        logging.info(f"Cache set for key: {key}")
        redis_client = get_redis_client()
        redis_client.setex(key, timeout, json.dumps(value))
        logging.info(f"Cache set completed for key: {key}")
    except Exception as e:
        current_app.logger.error(f"Error setting cache for key {key}: {e}")