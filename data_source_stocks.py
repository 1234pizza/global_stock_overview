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
    def get_all_stocks_data(_self):
        try:
            all_tickers = []
            ticker_to_index = {}
            for idx, tickers in _self.index_config.items():
                for t in tickers:
                    if t not in all_tickers:
                        all_tickers.append(t)
                        ticker_to_index[t] = idx

            # Download 35 days of data
            data = yf.download(all_tickers, period="35d", interval="1d", group_by='ticker', progress=False)
            
            if data.empty:
                return pd.DataFrame()

            combined_results = []
            for ticker in all_tickers:
                try:
                    # Check if ticker exists in columns
                    if ticker not in data.columns.get_level_values(0):
                        continue
                    
                    df_t = data[ticker].dropna()
                    if len(df_t) < 10: 
                        continue

                    close = df_t['Close']
                    
                    # Calculations
                    today_pct = ((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]) * 100
                    total_7d = ((close.iloc[-1] - close.iloc[-8]) / close.iloc[-8]) * 100
                    total_30d = ((close.iloc[-1] - close.iloc[0]) / close.iloc[0]) * 100

                    row = {
                        'Index': ticker_to_index[ticker],
                        'Ticker': ticker.split('.')[0],
                        'Total 30D %': round(total_30d, 2),
                        'Total 7D %': round(total_7d, 2),
                        'Today %': round(today_pct, 2)
                    }

                    # Add Last 7 Days history
                    for i in range(1, 8):
                        # % change from previous day
                        val = ((close.iloc[-i] - close.iloc[-(i+1)]) / close.iloc[-(i+1)]) * 100
                        row[f'Day -{i} (%)'] = round(val, 2)
                    
                    combined_results.append(row)
                except:
                    continue

            return pd.DataFrame(combined_results)
        except Exception as e:
            st.error(f"Data Source Error: {e}")
            return pd.DataFrame()