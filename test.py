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

apiBaseUrl = 'http://localhost:8000/api'

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

response = requests.get(f"{apiBaseUrl}/alert/list")

if response.status_code == 200:
    # Parse JSON response data
    scraping_list = response.json()['data']
    
    for url, alerts in scraping_list.items():

        print(f"URL: {url}")
        
        try:
            driver.get(url)
            wait = WebDriverWait(driver, 15)
            search_results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.cl-search-result')))

            for alert in alerts:

                print(f"KEYWORDS: {alert['keywords']}")

                keywords = re.split(r',\s*', alert['keywords'])
                
                for index, result in enumerate(search_results, 1):

                    if any(keyword.lower() in result.text.lower() for keyword in keywords):

                        title = result.get_attribute('title')
                        url = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                        has_pic = 1 if len(result.find_elements(By.CSS_SELECTOR, 'img')) > 0 else 0

                        try:
                            price = result.find_element(By.CSS_SELECTOR, 'span.priceinfo').text.replace('$', '').replace(',', '')
                        except:
                            price = None

                        clid = result.get_attribute('data-pid')
                        alert_id = alert['id']

                        pattern = r'\b(0?[1-9]|1[0-2])/([1-9]|[12][0-9]|3[01])\b'
                        current_year = datetime.now().year
                        match = re.search(pattern, result.text)
                        if match:
                            month = int(match.group(1))
                            day = int(match.group(2))
                            date_obj = datetime(year=current_year, month=month, day=day)
                            date_posted = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            date_posted = None

                        post_data = {
                            'title': title,
                            'url': url,
                            'has_pic': has_pic,
                            'clid': clid,
                            'alert_id': alert_id
                        }

                        if price is not None:
                            post_data['price'] = price

                        if date_posted is not None:
                            post_data['date_posted'] = date_posted

                        post_response = requests.post(f"{apiBaseUrl}/post", json=post_data)
                        if post_response.status_code == 200 or post_response.status_code == 201:
                            data = post_response.json()
                            print(f"Post created: {data}")
                        else:
                            print(f"Failed to create post. Status code: {post_response.status_code}")
                            print(post_response)

        except Exception as e:
            print(f"Error occurred: {e}")
            #print(driver.page_source)

        finally:
            driver.quit()

        sleep_time = random.randint(1, 10)
        print(f"Sleeping for {sleep_time} seconds before processing the next URL...")
        time.sleep(sleep_time)
        
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
