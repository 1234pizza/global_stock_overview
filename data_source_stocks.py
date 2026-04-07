import yfinance as yf
import pandas as pd
from datetime import datetime

class DataSource:
    def __init__(self):
        # Define the tickers for each index
        self.index_config = {
            "SMI": {
                "tickers": [
                    "ABBN.SW", "ALC.SW", "CFR.SW", "GEBN.SW", "GIVN.SW", 
                    "HOLN.SW", "KNIN.SW", "LOGN.SW", "LONN.SW", "NESN.SW", 
                    "NOVN.SW", "PGHN.SW", "ROG.SW", "SCMN.SW", "SIKA.SW", 
                    "SLHN.SW", "SOON.SW", "SREN.SW", "UBSG.SW", "ZURN.SW"
                ],
                "currency": "CHF",
                "suffix": ".SW"
            },
            "DAX": {
                "tickers": [
                    "ADS.DE", "AIR.DE", "ALV.DE", "BAS.DE", "BAYN.DE", "BMW.DE",
                    "CON.DE", "DB1.DE", "DBK.DE", "DHL.DE", "DTE.DE", "EOAN.DE",
                    "IFX.DE", "MBG.DE", "MUV2.DE", "SAP.DE", "SIE.DE", "VOW3.DE"
                ],
                "currency": "EUR",
                "suffix": ".DE"
            },
            "SP500": {
                "tickers": ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "BRK-B", "TSLA", "V", "JPM"],
                "currency": "USD",
                "suffix": ""
            },
            "NASDAQ": {
                "tickers": ["AAPL", "MSFT", "AMZN", "NVDA", "AVGO", "META", "ADBE", "COST", "PEP", "NFLX"],
                "currency": "USD",
                "suffix": ""
            }
        }

    def get_data_for_index(self, index_name):
        """Fetch real-time data for a specific index by name"""
        try:
            if index_name not in self.index_config:
                print(f"Index {index_name} not configured.")
                return pd.DataFrame()

            config = self.index_config[index_name]
            tickers = config["tickers"]
            currency = config["currency"]
            suffix = config["suffix"]

            # Download data (1m interval for 'live' feel)
            data = yf.download(tickers, period="1d", interval="1m", group_by='ticker', progress=False)
            
            stock_list = []
            
            for ticker in tickers:
                # Handle cases where yfinance might return a single-ticker DataFrame differently
                if len(tickers) > 1:
                    ticker_data = data[ticker]
                else:
                    ticker_data = data

                if not ticker_data.empty:
                    last_price = ticker_data['Close'].iloc[-1]
                    
                    stock_list.append({
                        'Ticker': ticker.replace(suffix, ""), 
                        f'Price ({currency})': round(last_price, 2),
                        'Time': datetime.now().strftime("%H:%M:%S")
                    })

            return pd.DataFrame(stock_list)

        except Exception as error:
            print(f"Error fetching {index_name} data: {error}")
            return pd.DataFrame()

# --- Example Usage ---
if __name__ == "__main__":
    source = DataSource()
    # Test with DAX
    dax_table = source.get_data_for_index("DAX")
    print(dax_table)