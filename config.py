import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the application."""

    # Rate limiting settings
    RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "100 per day, 20 per hour")
    RATELIMIT_STRATEGY = os.getenv("RATELIMIT_STRATEGY", "moving-window")
    CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL", "redis://localhost:6379")

    # Cache settings
    CACHE_TYPE = os.getenv("CACHE_TYPE", "redis")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 600))
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # List of hot keywords for cache preheating
    HOT_KEYWORDS = os.getenv("HOT_KEYWORDS", "AI,Claude,Gemini,ChatGPT,Google").split(',')
    
    @classmethod
    def reload(cls):
        load_dotenv(override=True)
        cls.HOT_KEYWORDS = os.getenv("HOT_KEYWORDS", "AI,Claude,Gemini,ChatGPT,Google").split(',')

    # Performance monitoring flag
    ENABLE_PERFORMANCE_MONITORING = os.getenv("ENABLE_PERFORMANCE_MONITORING", "True").lower() == "true"

    # Logging level
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Debug mode
    DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"
    
    # enable pytest
    TESTING = os.getenv("TESTING", "True").lower() == "true"

    # Default platforms to search
    DEFAULT_PLATFORMS = os.getenv("DEFAULT_PLATFORMS", "reddit,hackernews,github,v2ex,theresanaiforthat").split(',')

    # Add any additional configuration variables here
    
# class ProdConfig: