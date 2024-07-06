from typing import List
from config import Config

def get_default_platforms() -> List[str]:
    """
    Get the list of default platforms to search.
    
    Returns:
        List[str]: A list of default platform names.
    """
    return Config.DEFAULT_PLATFORMS