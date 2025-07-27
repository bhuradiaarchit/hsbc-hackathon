
import requests
import logging

def get_24hr_ticker_update(contract_pair):

    if not contract_pair:
        logging.error("Invalid contract pair. Please enter a valid contract pair (e.g., 'btc', 'eth').")
        return None

    full_url = f"https://api.pi42.com/v1/market/ticker24Hr/{contract_pair}"
    logging.info(f"Constructed URL: {full_url}")

    try:
        response = requests.get(full_url)
        response.raise_for_status()
        logging.info(f"Successfully fetched data for contract pair: {contract_pair}")
        
        response_data = response.json()
        return response_data

    except requests.exceptions.HTTPError as err:
        if err.response:
            logging.error(f"HTTPError for contract pair {contract_pair}: {err.response.text}")
        else:
            logging.error(f"HTTPError: {err}")
    except Exception as e:
        logging.exception(f"An unexpected error occurred for contract pair {contract_pair}: {str(e)}")

    return None

def get_current_price(ticker):

    try:
        data = get_24hr_ticker_update(ticker)
        if data and "data" in data and "c" in data["data"]:
            current_price = float(data["data"]["c"])
            logging.info(f"Current price for {ticker}: {current_price}")
            return current_price
        else:
            logging.warning(f"Price data not found for ticker: {ticker}")
            return None
    except Exception as e:
        logging.exception(f"An error occurred while fetching the current price for {ticker}: {str(e)}")
        return None