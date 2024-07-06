import os
from dotenv import set_key
from config import Config

def update_hot_keywords(keywords):
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    
    # update .env file
    set_key(env_path, "HOT_KEYWORDS", ','.join(keywords))
    
    Config.reload()

def get_hot_keywords():
    return Config.HOT_KEYWORDS