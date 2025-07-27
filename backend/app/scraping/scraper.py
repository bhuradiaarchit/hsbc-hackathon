import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

NSE_URL = "https://www.nseindia.com/market-data/large-deals"

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

def get_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    time.sleep(20000)
    return driver

def download_csv():
    driver = get_driver()
    driver.get(NSE_URL)
    time.sleep(5) 
    try:
        csv_button = driver.find_element(By.XPATH, "//a[contains(@href, '.csv')]")
        csv_url = csv_button.get_attribute("href")

        if csv_url:
            logger.info(f"Downloading CSV from {csv_url}")
            response = requests.get(csv_url, timeout=10)
            if response.status_code == 200:
                csv_path = "nse_large_deals.csv"
                with open(csv_path, "wb") as file:
                    file.write(response.content)
                logger.info("CSV Downloaded Successfully!")
                return csv_path
            else:
                logger.error(f"❌ Failed to download CSV. Status Code: {response.status_code}")
                return None
        else:
            logger.error("CSV link not found!")
            return None

    except Exception as e:
        logger.error(f"❌ Error while downloading CSV: {e}")
        return None

    finally:
        driver.quit()
