from core.posts_search import optimized_search_hot_posts
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    keyword = input("Please enter the keyword you want to search for: ")
    results, timing = optimized_search_hot_posts(keyword, None)
    for post in results:
        print(f"Platform: {post['platform']}")
        print(f"Author: {post['author']}")
        print(f"Title: {post['title']}")
        print(f"Metrics: {post['metrics']}")
        print(f"Link: {post['link']}")
        print(f"Created at: {post['created_at']}")
        print("---")
    print(f"Total search time: {timing['total_time']} ms")

if __name__ == "__main__":
    main()