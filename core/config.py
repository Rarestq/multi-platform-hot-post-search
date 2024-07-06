import os

class Config:
    """Configuration settings for the application."""

    # Rate limiting settings
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', "100 per day, 20 per hour")

    # Cache settings
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 600))

    # List of hot keywords for cache preheating
    HOT_KEYWORDS = os.getenv('HOT_KEYWORDS', 'AI,Claude,Gemini').split(',')

    # Performance monitoring flag
    ENABLE_PERFORMANCE_MONITORING = os.getenv('ENABLE_PERFORMANCE_MONITORING', 'True').lower() == 'true'

    # Logging level
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Default platforms to search
    DEFAULT_PLATFORMS = os.getenv('DEFAULT_PLATFORMS', 'reddit,hackernews,github,v2ex,theresanaiforthat').split(',')

    # Add any additional configuration variables here