import yfinance as yf
import pandas as pd
import streamlit as st

class DataSource:
    def __init__(self):
        # Comprehensive lists for all indices
        self.index_config = {
            "SMI": ["ABBN.SW", "ALC.SW", "CFR.SW", "GEBN.SW", "GIVN.SW", "HOLN.SW", "KNIN.SW", "LOGN.SW", "LONN.SW", "NESN.SW", "NOVN.SW", "PGHN.SW", "ROG.SW", "SCMN.SW", "SIKA.SW", "SLHN.SW", "SOON.SW", "SREN.SW", "UBSG.SW", "ZURN.SW"],
            "DAX": ["ADS.DE", "AIR.DE", "ALV.DE", "BAS.DE", "BAYN.DE", "BMW.DE", "CON.DE", "DB1.DE", "DBK.DE", "DHL.DE", "DTE.DE", "EOAN.DE", "IFX.DE", "MBG.DE", "MUV2.DE", "SAP.DE", "SIE.DE", "VOW3.DE", "BEI.DE", "BNR.DE", "CBK.DE", "1COV.DE", "DTG.DE", "FRE.DE", "FME.DE", "HEI.DE", "HEN3.DE", "HLAG.DE", "MTX.DE", "PUM.DE", "PAH3.DE", "RWE.DE", "SHL.DE", "SY1.DE", "VNA.DE", "ZAL.DE", "MRK.DE", "LIN.DE", "ENR.DE", "QIA.DE"],
            "SP500": ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "BRK-B", "TSLA", "V", "JPM", "UNH", "JNJ", "XOM", "WMT", "MA", "AVGO", "PG", "ORCL", "CVX", "HD"], # Add more as needed
            "NASDAQ": ["AAPL", "MSFT", "AMZN", "NVDA", "AVGO", "META", "ADBE", "COST", "PEP", "NFLX", "AMD", "CMCSA", "TMUS", "TXN", "INTC", "AMGN", "HON", "INTU", "QCOM", "SBUX"]
        }

    @st.cache_data(ttl=300)
    def get_all_stocks_data(self):
        """Combines all indices into one single massive table"""
        try:
            # 1. Combine all unique tickers into one list
            all_tickers = []
            ticker_to_index = {} # To keep track of which stock belongs where
            
            for index_name, tickers in self.index_config.items():
                for t in tickers:
                    if t not in all_tickers:
                        all_tickers.append(t)
                        ticker_to_index[t] = index_name

            # 2. Batch Download (One request for EVERYTHING)
            data = yf.download(all_tickers, period="12d", interval="1d", group_by='ticker', progress=False)
            
            combined_results = []
            
            # 3. Process the data
            for ticker in all_tickers:
                try:
                    # Handle single vs multi-ticker dataframe return
                    ticker_df = data[ticker].dropna() if len(all_tickers) > 1 else data.dropna()
                    
                    if not ticker_df.empty and len(ticker_df) > 1:
                        pct_changes = ticker_df['Close'].pct_change() * 100
                        
                        # Clean suffix for display
                        display_name = ticker.split('.')[0]
                        
                        row = {
                            'Index': ticker_to_index[ticker],
                            'Ticker': display_name,
                            'Today %': round(pct_changes.iloc[-1], 2)
                        }
                        
                        # Add last 7 trading days
                        for i in range(1, 8):
                            if len(pct_changes) > i:
                                row[f'Day -{i} (%)'] = round(pct_changes.iloc[-(i+1)], 2)
                        
                        combined_results.append(row)
                except:
                    continue

            return pd.DataFrame(combined_results)
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return pd.DataFrame()