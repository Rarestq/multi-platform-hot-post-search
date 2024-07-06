from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from .platform import Platform

POSTS_LIMIT = 5
V2EX_URL = "https://www.sov2ex.com/"
CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"

class V2EX(Platform):
    def get_posts(self, keyword):
        """
        Fetch top posts related to the given keyword from V2EX using sov2ex.com.
        """
        print(f"Searching V2EX for keyword: {keyword}\n")
        
        params = {
            'q': keyword
        }
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        
        # Set up the WebDriver
        service = Service(CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        url = V2EX_URL + '?' + '&'.join([f"{k}={v}" for k, v in params.items()])
        
        try:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            result_cards = soup.find_all('div', class_='resultcard')
            
            hot_posts = []
            
            for card in result_cards[:POSTS_LIMIT]:
                title_tag = card.find('a', href=True)
                if title_tag:
                    title = title_tag.text.strip()
                    link = title_tag['href']
                    
                    author_tag = card.find('a', href=lambda x: x and '/member/' in x)
                    author = author_tag.text.strip() if author_tag else 'Unknown'
                    
                    date_tag = card.find('span', class_='date')
                    date = date_tag.text.strip() if date_tag else 'Unknown'
                    
                    replies_tag = card.find('span', class_='replies')
                    replies = int(replies_tag.find('span').text.strip()) if replies_tag else 0
                    
                    hot_posts.append({
                        'title': title,
                        'author': author,
                        'date': date,
                        'replies': replies,
                        'link': link
                    })
            
            return [self.format_post(
                "V2EX",
                post['author'],
                post['title'],
                post['replies'],
                post['link'],
                post['date']
            ) for post in hot_posts]

        except Exception as e:
            print(f"Error fetching data from V2EX: {e}")
            return []
        finally:
            driver.quit()
        
    def format_timestamp(self, timestamp):
        return super().format_timestamp(timestamp)
    
    def requires_translation(self):
        return False