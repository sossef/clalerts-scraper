from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium with Chrome WebDriver
def extract_search_results_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Optional: Run in headless mode

    # Automatically detect and download the correct version of ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Load the webpage
        driver.get(url)

        # Wait until the specific <li> elements with class "search-result" are present
        wait = WebDriverWait(driver, 15)  # Wait for up to 15 seconds
        search_results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.cl-search-result')))

        # Extract and print the results
        for index, result in enumerate(search_results, 1):
            print(f"Result {index}:")
            print(result.text)
            print()

    except Exception as e:
        print(f"Error occurred: {e}")
        # Print the page source to debug if necessary
        print(driver.page_source)

    finally:
        # Close the browser
        driver.quit()

# Example usage
url = 'https://miami.craigslist.org/search/sof'
extract_search_results_selenium(url)
