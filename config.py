from dotenv import load_dotenv
import os

load_dotenv()

API_BASE_URL = os.getenv('API_BASE_URL')
API_KEY = os.getenv('API_KEY')

CSS_SELECTOR_SEARCH_RESULT = 'li.cl-search-result'
CSS_SELECTOR_PIC = 'img'
CSS_SELECTOR_PRICE_INFO = 'span.priceinfo'
DATE_PATTERN = r'\b(0?[1-9]|1[0-2])/([1-9]|[12][0-9]|3[01])\b'