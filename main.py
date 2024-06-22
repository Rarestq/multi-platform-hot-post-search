from platforms.reddit_search import Reddit
from platforms.hackernews_search import HackerNews
from platforms.github_repos_search import GitHub
from platforms.theresanaiforthat_search import TheresAnAIForThat
from platforms.v2ex_search import V2EX
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate
import re
# from emails.email_notifier import EmailNotifier
# from apscheduler.schedulers.background import BackgroundScheduler
# import atexit

load_dotenv()

class PostSearcher:
    def __init__(self):
        """
        Initialize PostSearcher with an empty list of platforms and translator.
        """
        self.platforms = []
        self.translator = translate.Client()

    def register_platform(self, platform):
        """
        Register a platform by adding it to the list of platforms.
        """
        self.platforms.append(platform)
        
    def translate_keyword(self, keyword):
        """
        Translate the keyword to English if it is not in English.
        """
        try:
            if self.is_english(keyword):
                return keyword  # Keyword only contains English letters
            else:
                # Translate the keyword to English
                translation = self.translator.translate(keyword, target_language='en')
                return translation['translatedText']
        except Exception as e:
            print(f"Error detecting or translating language: {e}")
            return keyword  # In case of an error, return the original keyword
        
    def is_english(self, keyword):
        """
        Check if the keyword is an English word or phrase.
        """
        return re.match(r'^[a-zA-Z\s]+$', keyword) is not None


    def search(self, keyword):
        """
        Search for posts related to the given keyword across all registered platforms, 
        and return the top five posts sorted by metrics.
        """
        all_posts = []
        for platform in self.platforms:
            if platform.requires_translation():
                translated_keyword = self.translate_keyword(keyword)
                all_posts.extend(platform.get_posts(translated_keyword))
            else:
                all_posts.extend(platform.get_posts(keyword))
        return all_posts

def main():
    """
    Main function to interact with the user, register platforms, perform search, 
    and print the results.
    """
    keyword = input("Please enter the keyword you want to search for: ")
    # user_email = input("Please enter your email to receive notifications: ")

    # Create PostSearcher object and register platforms
    searcher = PostSearcher()
    searcher.register_platform(Reddit())
    searcher.register_platform(HackerNews())
    searcher.register_platform(GitHub())
    searcher.register_platform(TheresAnAIForThat())
    searcher.register_platform(V2EX())

    # Search for the keyword and get the top posts
    top_posts = searcher.search(keyword)

    # Print the results
    for post in top_posts:
        print(f"Platform: {post['platform']}")
        print(f"Author: {post['author']}")
        print(f"Title: {post['title']}")
        print(f"Metrics: {post['metrics']}")
        print(f"Link: {post['link']}")
        print(f"Post: {post['created_at']}")
        print("---")
        
    # # Set up scheduler to run the email notification task every day at 8 PM
    # scheduler = BackgroundScheduler()
    # # scheduler.add_job(main, 'cron', hour=20, minute=0)
    
    # # Note：Test to run the email notification task every 5 minute
    # scheduler.add_job(main, 'interval', minutes=5)
    # scheduler.start()

    # # Shut down the scheduler when exiting the app
    # atexit.register(lambda: scheduler.shutdown())

    # # Send email notification
    # if top_posts:
    #     body = "\n".join([f"Platform: {post['platform']}\nAuthor: {post['author']}\nTitle: {post['title']}\nMetrics: {post['metrics']}\nLink: {post['link']}\nPost: {post['created_at']}\n---" for post in top_posts])
    #     email_notifier = EmailNotifier()
    #     email_notifier.add_recipient(user_email)
    #     email_notifier.send_email(f"Keyword: {keyword} - Hottest Posts", body)

if __name__ == "__main__":
    main()