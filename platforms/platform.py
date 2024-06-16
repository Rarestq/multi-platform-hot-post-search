from abc import ABC, abstractmethod

class Platform(ABC):
    @abstractmethod
    def get_posts(self, keyword):
        """
        Abstract method to be implemented by each platform to fetch posts related to the given keyword.
        """
        pass

    @staticmethod
    def format_post(platform, author, description, metrics, link, created_at):
        """
        Method to format post information, ensuring consistency across different platforms.
        """
        return {
            "platform": platform,
            "author": author,
            "description": description[:100] + "..." if len(description) > 100 else description,
            "metrics": metrics,
            "link": link,
            "created_at": created_at
        }
