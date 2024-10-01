from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import random
import re
from datetime import datetime

API_BASE_URL = 'http://localhost:8000/api'
CSS_SELECTOR_SEARCH_RESULT = 'li.cl-search-result'
CSS_SELECTOR_PIC = 'img'
CSS_SELECTOR_PRICE_INFO = 'span.priceinfo'
DATE_PATTERN = r'\b(0?[1-9]|1[0-2])/([1-9]|[12][0-9]|3[01])\b'

def fetch_scraping_list():
    response = requests.get(f"{API_BASE_URL}/alert/list")
    if response.status_code == 200:
        return response.json().get('data', {})
    print(f"Failed to retrieve data. Status code: {response.status_code}")
    return None


def scrape_page(url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        return wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, CSS_SELECTOR_SEARCH_RESULT)))
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
        #print(driver.page_source)

def extract_date_posted(text):
    current_year = datetime.now().year
    match = re.search(DATE_PATTERN, text)
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
        date_obj = datetime(year=current_year, month=month, day=day)
        return date_obj.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return None

def post_result(post_data):
    post_response = requests.post(f"{API_BASE_URL}/post", json=post_data)
    if post_response.status_code == 200 or post_response.status_code == 201:
        data = post_response.json()
        print(f"Post created: {data}")
    else:
        print(f"Failed to create post. Status code: {post_response.status_code}")
        print(post_response)

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

    has_pic = 1 if len(result.find_elements(By.CSS_SELECTOR, CSS_SELECTOR_PIC)) > 0 else 0

    try:
        price = float(result.find_element(By.CSS_SELECTOR, CSS_SELECTOR_PRICE_INFO).text.replace('$', '').replace(',', ''))
    except:
        price = None

    search_result = {
        'web_element': result,
        'has_pic': has_pic,
        'price': price
    }

    return search_result


scraping_list = fetch_scraping_list()

if scraping_list:

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) as driver:

        for url, alerts in scraping_list.items():

            print(f"URL: {url}")

            sleep_time = random.randint(1, 10)
            print(f"Sleeping for {sleep_time} seconds before processing the next URL...")
            time.sleep(sleep_time)

            search_results = scrape_page(url)
            
            if search_results:

                for alert in alerts:

                    print(f"KEYWORDS: {alert['keywords']}")

                    keywords = re.split(r',\s*', alert['keywords'])
                    
                    for index, result in enumerate(search_results, 1):

                        search_result = prepare_search_result(result)
                        
                        if include_result(alert, search_result):  

                            post_result(prepare_post(alert, search_result))

            

                        


    
