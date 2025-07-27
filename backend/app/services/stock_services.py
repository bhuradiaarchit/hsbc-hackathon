

import pandas as pd
from fyers_apiv3 import fyersModel
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import pytz

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


load_dotenv()

class FyersAPI():

    def __init__(self):
        client_id = os.getenv('FYERS_CLIENT_ID')
        access_token = os.getenv('FYERS_ACCESS_TOKEN')
        self.fyers = fyersModel.FyersModel(token=access_token,
                                                   is_async=False,
                                                   client_id=client_id,
                                                   log_path="")
    
    
    def epoch_values_for_fyers(self, timestamp):
        ist = pytz.timezone("Asia/Kolkata")

        try:
            naive_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # Fallback to date only if time is missing
            naive_dt = datetime.strptime(timestamp, "%Y-%m-%d")
            naive_dt = naive_dt.replace(hour=0, minute=0, second=0)

        aware_ist_dt = ist.localize(naive_dt)
        utc_dt = aware_ist_dt.astimezone(pytz.utc)
        epoch_time = int(utc_dt.timestamp())

        return epoch_time
    
    def get_symbol_data(self, symbol, start_date, end_date, res):
        
        start_date = self.epoch_values_for_fyers(start_date)
        end_date = self.epoch_values_for_fyers(end_date)

        try:
            data = {"symbol": symbol,
                    "resolution":res,
                    "date_format":"0",
                    "range_from":start_date,
                    "range_to":end_date,
                    "cont_flag":"1"}
            
            logger.info(data)
            
            data_candles = (self.fyers.history(data)).get('candles')
            columns = ["epoch", "open", "high", "low", "close", "volume"]
            df = pd.DataFrame(data_candles, columns=columns)
            df["date"] = pd.to_datetime(df["epoch"], unit='s', utc=True).dt.tz_convert("Asia/Kolkata")
            df = df[["date", "open", "high", "low", "close", "volume"]]

            return df
        except Exception as e:
            logger.error(f"Extracting Data from FYERS gave an error: {e}")
            raise
    
    def get_ltp(self, symbol):
        data = {"symbols": symbol}
        response = self.fyers.quotes(data = data)
        print(response)
        ltp = response['d'][0]['v']['lp']
        return float(ltp) if ltp is not None else None


if __name__ == "__main__":
    fyers_client = FyersAPI()
    df = fyers_client.get_symbol_data("BSE:SENSEX25JUL81200CE", "2025-06-11 14:00:00", "2025-07-30 14:00:00", "1")
    print(df)
