import requests
from bs4 import BeautifulSoup
from .platform import Platform

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

POSTS_LIMIT=5

THERESANAIFORTHAT_URL="https://theresanaiforthat.com/requests"

class TheresAnAIForThat(Platform):
    def get_posts(self, keyword):
        """
        Fetch top posts related to the given keyword from theresanaiforthat.com.
        """
        try:
            response = requests.get(THERESANAIFORTHAT_URL, headers=HEADERS)
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            posts = soup.find_all('div', class_='row request')
            
            hot_posts = []
            
            for post in posts:
                title_tag = post.find('a', class_='request_title')
                if title_tag and keyword.lower() in title_tag.text.lower():
                    title = title_tag.text
                    link = title_tag['href']
                    vote_tag = post.find('div', class_='votes_count')
                    vote = int(vote_tag.text) if vote_tag else 0
                    user_tag = post.find('a', class_='comment_user_name')
                    user_name = user_tag.text if user_tag else 'Unknown'
                    launch_date_tag = post.find('span', class_='launch_date_top')
                    launch_date = launch_date_tag.text.strip() if launch_date_tag else 'Unknown'
                    
                    hot_posts.append({
                        'title': title,
                        'link': link,
                        'vote': vote,
                        'user_name': user_name,
                        'launch_date': launch_date
                    })
            
            # Sort posts by vote count in descending order
            hot_posts.sort(key=lambda x: x['vote'], reverse=True)
            
            return [self.format_post(
                "TheresAnAIForThat",
                post['user_name'],
                post['title'],
                post['vote'],
                post['link'],
                post['launch_date']
            ) for post in hot_posts[:POSTS_LIMIT]]

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from TheresAnAIForThat: {e}")
            return []
        
    def format_timestamp(self, timestamp):
        return super().format_timestamp(timestamp)