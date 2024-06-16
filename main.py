from platforms.reddit_search import Reddit
from platforms.hackernews_search import HackerNews
from dotenv import load_dotenv

load_dotenv()

class PostSearcher:
    def __init__(self):
        """
        Initialize PostSearcher with an empty list of platforms.
        """
        self.platforms = []

    def register_platform(self, platform):
        """
        Register a platform by adding it to the list of platforms.
        """
        self.platforms.append(platform)

    def search(self, keyword):
        """
        Search for posts related to the given keyword across all registered platforms, 
        and return the top five posts sorted by metrics.
        """
        all_posts = []
        for platform in self.platforms:
            all_posts.extend(platform.get_posts(keyword))
        return all_posts

def main():
    """
    Main function to interact with the user, register platforms, perform search, 
    and print the results.
    """
    keyword = input("Please enter the keyword you want to search for: ")

    # Create PostSearcher object and register platforms
    searcher = PostSearcher()
    searcher.register_platform(Reddit())
    searcher.register_platform(HackerNews())

    # Search for the keyword and get the top posts
    top_posts = searcher.search(keyword)

    # Print the results
    for post in top_posts:
        print(f"Platform: {post['platform']}")
        print(f"Author: {post['author']}")
        print(f"Description: {post['description']}")
        print(f"Metrics: {post['metrics']}")
        print(f"Link: {post['link']}")
        print(f"Created_at: {post['created_at']}")
        print("---")

if __name__ == "__main__":
    main()