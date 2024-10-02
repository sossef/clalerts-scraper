from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import log
import logging

logger = logging.getLogger(__name__)

import clscraper, api

scraping_list = api.fetch_scraping_list()

if scraping_list:

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) as driver:

        for url, alerts in scraping_list.items():

            logger.info(f"Fetching page from: {url}")

            clscraper.wait()

            search_results = clscraper.scrape_page(driver, url)
            
            if search_results:

                for alert in alerts:

                    logger.info(f"Processing Alert ID: {alert['id']}. Name: '{alert['name']}'. Keywords: '{alert['keywords']}'. has_pic: {alert['has_pic']}. Price: [{alert['min_price']} - {alert['max_price']}]")
                    
                    for index, result in enumerate(search_results, 1):

                        search_result = clscraper.prepare_search_result(result)
                        
                        if clscraper.include_result(alert, search_result):  

                            api.post_result(clscraper.prepare_post(alert, search_result))

else:
    logger.info('No alerts to process.')            

                        


    
