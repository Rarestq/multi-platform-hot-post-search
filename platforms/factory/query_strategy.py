from abc import ABC, abstractmethod

# Define the base class for query strategies
class QueryStrategy(ABC):
    @abstractmethod
    def fetch_posts(self, platform, keyword):
        pass

# Strategy for fetching latest posts
class LatestStrategy(QueryStrategy):
    def fetch_posts(self, platform, keyword):
        return platform.fetch_latest_posts(keyword)

# Strategy for fetching top posts
class TopStrategy(QueryStrategy):
    def fetch_posts(self, platform, keyword):
        return platform.fetch_top_posts(keyword)

# Strategy for fetching hottest posts
class HottestStrategy(QueryStrategy):
    def fetch_posts(self, platform, keyword):
        return platform.fetch_hottest_posts(keyword)