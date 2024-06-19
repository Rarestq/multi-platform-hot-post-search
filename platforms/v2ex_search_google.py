from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from .platform import Platform
from datetime import datetime

POSTS_LIMIT = 5
GOOGLE_URL = "https://www.google.com/search"
CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"

class V2EX_GOOGLE(Platform):
    def get_posts(self, keyword):
        """
        Fetch top posts related to the given keyword from V2EX using Google search.
        """
        params = {
            'q': f'site:v2ex.com/t {keyword}'
        }
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        
        # Set up the WebDriver
        service = Service(CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        url = GOOGLE_URL + '?' + '&'.join([f"{k}={v}" for k, v in params.items()])
        
        try:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            search_results = soup.find_all('div', class_='tF2Cxc')
            
            hot_posts = []
            
            for result in search_results[:POSTS_LIMIT]:
                title_tag = result.find('h3')
                if title_tag:
                    title = title_tag.text.strip()
                    link_tag = result.find('a', href=True)
                    link = link_tag['href'] if link_tag else 'Unknown'
                    
                    date_tag = result.find('span', class_='LEwnzc Sqrs4e')
                    date_str = date_tag.text.strip().rstrip(' —') if date_tag else 'Unknown'
                    date = self.format_date(date_str)
                    
                    hot_posts.append({
                        'title': title,
                        'link': link,
                        'date': date
                    })
            
            return [self.format_post(
                "V2EX",
                "Google Search",
                post['title'],
                "#", 
                post['link'],
                post['date']
            ) for post in hot_posts]

        except Exception as e:
            print(f"Error fetching data from Google: {e}")
            return []
        finally:
            driver.quit()
        
    def format_date(self, date_str):
        if date_str == 'Unknown':
            return date_str
        try:
            date_obj = datetime.strptime(date_str, '%Y/%m/%d')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            return 'Unknown'
        
    def format_timestamp(self, timestamp):
        return super().format_timestamp(timestamp)