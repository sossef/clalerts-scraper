from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import random
import re
import config
import logging

logger = logging.getLogger(__name__)

def wait():
    sleep_time = random.randint(10, 30)
    logger.info(f"Sleeping for {sleep_time} seconds before processing...")
    time.sleep(sleep_time)

def scrape_page(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        return wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, config.CSS_SELECTOR_SEARCH_RESULT)))
    except Exception as e:
        logger.error(f"Scraping error occurred: {e}", exc_info=True)
        return None
        #print(driver.page_source)

def extract_date_posted(text):
    current_year = datetime.now().year
    match = re.search(config.DATE_PATTERN, text)
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
        date_obj = datetime(year=current_year, month=month, day=day)
        return date_obj.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return None

def include_result(alert, result): 

    if alert['has_pic'] == 1 and result['has_pic'] != 1:
        return False
    
    # Include all items without price
    if result['price'] is not None:
        if alert['min_price'] is not None and result['price'] < float(alert['min_price']):
            return False
        if alert['max_price'] is not None and result['price'] > float(alert['max_price']):
            return False
        
    keywords = re.split(r',\s*', alert['keywords'])

    return True if any(keyword.lower() in result['web_element'].text.lower() for keyword in keywords) else False

def prepare_post(alert, result):

    web_element, has_pic, price = result['web_element'], result['has_pic'], result['price']

    date_posted = extract_date_posted(web_element.text)

    post_data = {
        'title': web_element.get_attribute('title'),
        'url': web_element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'),
        'has_pic': has_pic,
        'clid': web_element.get_attribute('data-pid'),
        'alert_id': alert['id']
    }

    if price is not None:
        post_data['price'] = price

    if date_posted is not None:
        post_data['date_posted'] = date_posted

    return post_data

def prepare_search_result(result):

    has_pic = 1 if len(result.find_elements(By.CSS_SELECTOR, config.CSS_SELECTOR_PIC)) > 0 else 0

    try:
        price = float(result.find_element(By.CSS_SELECTOR, config.CSS_SELECTOR_PRICE_INFO).text.replace('$', '').replace(',', ''))
    except:
        price = None

    search_result = {
        'web_element': result,
        'has_pic': has_pic,
        'price': price
    }

    return search_result