import yfinance as yf
import pandas as pd

class DataSource:
    def __init__(self):
        self.index_config = {
            "SMI": {"tickers": ["ABBN.SW", "ALC.SW", "CFR.SW", "GEBN.SW", "GIVN.SW", "HOLN.SW", "KNIN.SW", "LOGN.SW", "LONN.SW", "NESN.SW", "NOVN.SW", "PGHN.SW", "ROG.SW", "SCMN.SW", "SIKA.SW", "SLHN.SW", "SOON.SW", "SREN.SW", "UBSG.SW", "ZURN.SW"], "suffix": ".SW"},
            "DAX": {"tickers": ["ADS.DE", "AIR.DE", "ALV.DE", "BAS.DE", "BAYN.DE", "BMW.DE", "CON.DE", "DB1.DE", "DBK.DE", "DHL.DE", "DTE.DE", "EOAN.DE", "IFX.DE", "MBG.DE", "MUV2.DE", "SAP.DE", "SIE.DE", "VOW3.DE"], "suffix": ".DE"},
            "SP500": {"tickers": ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "BRK-B", "TSLA", "V", "JPM"], "suffix": ""},
            "NASDAQ": {"tickers": ["AAPL", "MSFT", "AMZN", "NVDA", "AVGO", "META", "ADBE", "COST", "PEP", "NFLX"], "suffix": ""}
        }

    def get_data_for_index(self, index_name):
        try:
            config = self.index_config[index_name]
            tickers = config["tickers"]
            
            # Fetch data
            data = yf.download(tickers, period="12d", interval="1d", group_by='ticker', progress=False)
            
            combined_results = []
            for ticker in tickers:
                # Get the Ticker Object to pull the company name
                t_obj = yf.Ticker(ticker)
                # Fallback to ticker symbol if name is not found
                company_name = t_obj.info.get('longName', ticker)
                
                hist = data[ticker]['Close'].dropna()
                
                if len(hist) > 1:
                    pct_changes = hist.pct_change() * 100
                    
                    stock_row = {
                        'Ticker': ticker.replace(config["suffix"], ""),
                        'Name': company_name,  # <--- Added Name
                        'Today %': round(pct_changes.iloc[-1], 2)
                    }
                    
                    for i in range(1, 8):
                        if len(pct_changes) > i:
                            val = pct_changes.iloc[-(i+1)]
                            stock_row[f'Day -{i} (%)'] = round(val, 2)
                    
                    combined_results.append(stock_row)
            
            return pd.DataFrame(combined_results)
        except Exception as e:
            print(f"Error: {e}")
            return pd.DataFrame()