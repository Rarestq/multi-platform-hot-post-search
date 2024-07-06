from typing import List
from .config import Config

def get_default_platforms() -> List[str]:
    """
    Get the list of default platforms to search.
    
    Returns:
        List[str]: A list of default platform names.
    """
    return Config.DEFAULT_PLATFORMS

def generate_cache_key(keyword: str, platforms: List[str] = None) -> str:
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
    return f"{keyword}_cross_platforms_{platforms_str}"