import config
import requests

headers = {
    'CLASKEY': config.API_KEY
}

def fetch_scraping_list():
    response = requests.get(f"{config.API_BASE_URL}/alert/list", headers=headers)
    if response.status_code == 200:
        return response.json().get('data', {})
    print(f"Failed to retrieve data\nStatus code: {response.status_code}\nMessage: {response.json().get('message')}")
    return None

def post_result(post_data):
    response = requests.post(f"{config.API_BASE_URL}/post", json=post_data, headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        data = response.json()
        print(f"Post created: {data}")
    else:
        print(f"Failed to create post\nStatus code: {response.status_code}\nMessage: {response.json().get('message')}")