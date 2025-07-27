
import requests
import logging
import pandas as pd
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    
def get_ohlc_for_symbol(symbol):

    data = get_24hr_ticker_update(symbol)['data']
    symbol_open = float(data['o'])
    symbol_high = float(data['h'])
    symbol_low = float(data['l'])
    symbol_close = float(data['c'])

    return (symbol_open, symbol_high, symbol_low, symbol_close)


def get_kline_data(pair, interval = "1m", limit = 1):
    try:
        params = {
            'pair': pair,
            'interval': interval,
            'limit': limit
        }

        headers = {
            'Content-Type': 'application/json'
        }

        
        kline_url = "https://api.pi42.com/v1/market/klines"

        for attempt in range(3):
            try:
                response = requests.post(kline_url, json=params, headers=headers)
                response.raise_for_status() # Raises an error for 4xx/5xx responses
                response_data = response.json()
                break  

            except requests.exceptions.RequestException:
                print(f"Retrying... ({attempt + 1})")
                time.sleep(10)  
        
        return response_data

    except ValueError:
        print("Please enter valid inputs for pair, interval.")
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err.response.text if err.response else err}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


def make_init_data(contract_pair, time = "1m"):
    
    try:
        logger.info(f"Fetching kline data for contract pair: {contract_pair}")
        info = get_kline_data(contract_pair, interval=time, limit=2000)
        
        data = []

        for i in info:
            high = float(i['high'])
            low = float(i['low'])
            close = float(i['close'])
            open = float(i['open'])
            
            timestamp = pd.to_datetime(int(i['startTime']), unit='ms')
            
            data.append({'date': timestamp, 'high': high, 'low': low, 'close': close, 'open': open})
        
        # Create the DataFrame
        df = pd.DataFrame(data)
        #df.set_index('Timestamp')
        #df.index = pd.to_datetime(df.index)
        
        logger.info("DataFrame created successfully.")
        return df
    
    except Exception as e:
        logger.error(f"Error while making initial data: {e}")
        raise


if __name__ == "__main__":

    print(get_current_price("BTCUSDT"))
    print(make_init_data("BTCUSDT", "1m"))