

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
        naive_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        ist = pytz.timezone("Asia/Kolkata")
        aware_ist_dt = ist.localize(naive_dt)
        utc_dt = aware_ist_dt.astimezone(pytz.utc)
        epoch_time = int(utc_dt.timestamp())

        return epoch_time
    
    def get_symbol_data(self, symbol, start_date, end_date, res):
        
        try:
            data = {"symbol": symbol,
                    "resolution":res,
                    "date_format":"0",
                    "range_from":start_date,
                    "range_to":end_date,
                    "cont_flag":"1"}
            
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
    #df = fyers_client.get_symbol_data("NSE:NIFTY25MAY25000CE", "2025-05-20", "2025-05-22")
    #print(df)

    res = fyers_client.get_ltp("NSE:NIFTY25JUNFUT")
    print(res)
