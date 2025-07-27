import os
import requests
import time
from dotenv import load_dotenv
import logging
from data_to_postgres import DataToPostgres

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

load_dotenv()

csv_url = os.getenv('CSV_URL')
csv_file_path = os.getenv('CSV_FILE_PATH')

def download_csv():
    try:
        logger.info("Downloading NSE Large Deals CSV file...")
        response = requests.get(csv_url, timeout=15)

        if response.status_code == 200:
            with open(csv_file_path, "wb") as file:
                file.write(response.content)
            logger.info(f"CSV downloaded successfully: {csv_file_path}")
            return True
        else:
            logger.error(f"Failed to download CSV. Status Code: {response.status_code}")
            return False
    except requests.RequestException as e:
        logger.error(f"Error downloading CSV: {e}")
        return False

if __name__ == "__main__":
    if download_csv():
        logger.info("Storing CSV data into database...")
        client = DataToPostgres()
        client.execution_flow()
    else:
        logger.error("Skipping database insertion due to CSV download failure.")

    
