from google.cloud import translate_v2 as translate
import re
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

class Translator:
    def __init__(self):
        """
        Initialize Translator with a translate client.
        """
        self.translator = translate.Client()
        
    @lru_cache(maxsize=100)
    def translate_keyword(self, keyword: str) -> str:
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
        except translate.exceptions.GoogleCloudError as e:
            logger.error(f"Error translating keyword: {e}")
            return keyword  # In case of an error, return the original keyword
        
    @staticmethod
    def is_english(keyword: str) -> bool:
        """
        [simple] Check if the keyword is an English word or phrase.
        """
        return re.match(r'^[a-zA-Z\s]+$', keyword.replace(' ', '')) is not None