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
    
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
        logger.info('Fetch successful')
        return response.json().get('data', {})
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to retrieve data. Exception: {str(e)}", exc_info=True)
        return None

def post_result(post_data):
    endpoint = f"{config.API_BASE_URL}/post"
    logger.info(f"Add Post: POST {endpoint}", extra={'json_data': post_data})

    try:
        response = requests.post(endpoint, json=post_data, headers=headers)
        response.raise_for_status()
        logger.info(response.json().get('message'))
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to create post\nStatus code: {response.status_code}\nMessage: {response.json().get('message')}", exc_info=True)
