import config
import requests
import logging

logger = logging.getLogger(__name__)

headers = {
    'CLASKEY': config.API_KEY
}

def fetch_scraping_list():
    endpoint = f"{config.API_BASE_URL}/alert/list"
    logger.info(f"Fetching latest alerts: GET {endpoint}")
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        logger.info('Fetch successful')
        return response.json().get('data', {})
    logger.error(f"Failed to retrieve data. Status code: {response.status_code}. Message: {response.json().get('message')}", exc_info=True)
    return None

def post_result(post_data):
    endpoint = f"{config.API_BASE_URL}/post"
    logger.info(f"Add Post: POST {endpoint}", extra={'json_data': post_data})
    response = requests.post(endpoint, json=post_data, headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        logger.info(response.json().get('message'))
    else:
        logger.error(f"Failed to create post\nStatus code: {response.status_code}\nMessage: {response.json().get('message')}", exc_info=True)