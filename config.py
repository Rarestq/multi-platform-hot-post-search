import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the application."""

    # Rate limiting settings
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', "100 per day, 20 per hour")

    # Cache settings
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 600))

    # List of hot keywords for cache preheating
    HOT_KEYWORDS = os.getenv('HOT_KEYWORDS', 'AI,Claude,Gemini').split(',')
    
    @classmethod
    def reload(cls):
        load_dotenv(override=True)
        cls.HOT_KEYWORDS = os.getenv('HOT_KEYWORDS', 'AI,Claude,Gemini').split(',')

    # Performance monitoring flag
    ENABLE_PERFORMANCE_MONITORING = os.getenv('ENABLE_PERFORMANCE_MONITORING', 'True').lower() == 'true'

    # Logging level
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Debug mode
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'False')
    
    # enable pytest
    TESTING = os.getenv('TESTING', 'True')

    # Default platforms to search
    DEFAULT_PLATFORMS = os.getenv('DEFAULT_PLATFORMS', 'reddit,hackernews,github,v2ex,theresanaiforthat').split(',')
    
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Add any additional configuration variables here
    
# class ProdConfig: