import yfinance as yf
import pandas as pd
import streamlit as st

class DataSource:
    def __init__(self):
        # Comprehensive lists
        self.index_config = {
            "SMI": ["ABBN.SW", "ALC.SW", "CFR.SW", "GEBN.SW", "GIVN.SW", "HOLN.SW", "KNIN.SW", "LOGN.SW", "LONN.SW", "NESN.SW", "NOVN.SW", "PGHN.SW", "ROG.SW", "SCMN.SW", "SIKA.SW", "SLHN.SW", "SOON.SW", "SREN.SW", "UBSG.SW", "ZURN.SW"],
            "DAX": ["ADS.DE", "AIR.DE", "ALV.DE", "BAS.DE", "BAYN.DE", "BMW.DE", "CON.DE", "DB1.DE", "DBK.DE", "DHL.DE", "DTE.DE", "EOAN.DE", "IFX.DE", "MBG.DE", "MUV2.DE", "SAP.DE", "SIE.DE", "VOW3.DE", "BEI.DE", "BNR.DE", "CBK.DE", "1COV.DE", "DTG.DE", "FRE.DE", "FME.DE", "HEI.DE", "HEN3.DE", "HLAG.DE", "MTX.DE", "PUM.DE", "PAH3.DE", "RWE.DE", "SHL.DE", "SY1.DE", "VNA.DE", "ZAL.DE", "MRK.DE", "LIN.DE", "ENR.DE", "QIA.DE"],
            "SP500": ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "BRK-B", "TSLA", "V", "JPM", "UNH", "JNJ", "XOM", "WMT", "MA", "AVGO", "PG", "ORCL", "CVX", "HD"],
            "NASDAQ": ["AAPL", "MSFT", "AMZN", "NVDA", "AVGO", "META", "ADBE", "COST", "PEP", "NFLX", "AMD", "CMCSA", "TMUS", "TXN", "INTC", "AMGN", "HON", "INTU", "QCOM", "SBUX"]
        }

    @st.cache_data(ttl=300)
    def get_all_stocks_data(_self): # Added underscore to avoid streamlit hashing issues
        try:
            all_tickers = []
            ticker_to_index = {}
            
            for index_name, tickers in _self.index_config.items():
                for t in tickers:
                    if t not in all_tickers:
                        all_tickers.append(t)
                        ticker_to_index[t] = index_name

            # Download data
            data = yf.download(all_tickers, period="15d", interval="1d", group_by='ticker', progress=False)
            
            if data.empty:
                return pd.DataFrame()

            combined_results = []
            
            for ticker in all_tickers:
                try:
                    # SECURE ACCESS: Check if ticker exists in the columns before trying to slice
                    if ticker not in data.columns.get_level_values(0):
                        continue
                        
                    ticker_df = data[ticker].dropna()
                    
                    if not ticker_df.empty and len(ticker_df) > 1:
                        pct_changes = ticker_df['Close'].pct_change() * 100
                        
                        display_name = ticker.split('.')[0]
                        
                        row = {
                            'Index': ticker_to_index[ticker],
                            'Ticker': display_name,
                            'Today %': round(pct_changes.iloc[-1], 2)
                        }
                        
                        # Get 7 history days
                        for i in range(1, 8):
                            if len(pct_changes) > i:
                                row[f'Day -{i} (%)'] = round(pct_changes.iloc[-(i+1)], 2)
                        
                        combined_results.append(row)
                except Exception:
                    continue # Skip individual errors to keep the app running

            return pd.DataFrame(combined_results)
        except Exception as e:
            # This helps debug without crashing the whole app
            st.error(f"Data Fetching Error: {str(e)}")
            return pd.DataFrame()