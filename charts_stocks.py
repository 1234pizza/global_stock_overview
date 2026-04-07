import yfinance as yf
import pandas as pd
import streamlit as st

class DataSource:
    def __init__(self):
        self.index_config = {
            "SMI": ["ABBN.SW", "ALC.SW", "CFR.SW", "GEBN.SW", "GIVN.SW", "HOLN.SW", "KNIN.SW", "LOGN.SW", "LONN.SW", "NESN.SW", "NOVN.SW", "PGHN.SW", "ROG.SW", "SCMN.SW", "SIKA.SW", "SLHN.SW", "SOON.SW", "SREN.SW", "UBSG.SW", "ZURN.SW"],
            "DAX": ["ADS.DE", "AIR.DE", "ALV.DE", "BAS.DE", "BAYN.DE", "BMW.DE", "CON.DE", "DB1.DE", "DBK.DE", "DHL.DE", "DTE.DE", "EOAN.DE", "IFX.DE", "MBG.DE", "MUV2.DE", "SAP.DE", "SIE.DE", "VOW3.DE", "BEI.DE", "BNR.DE", "CBK.DE", "1COV.DE", "DTG.DE", "FRE.DE", "FME.DE", "HEI.DE", "HEN3.DE", "HLAG.DE", "MTX.DE", "PUM.DE", "PAH3.DE", "RWE.DE", "SHL.DE", "SY1.DE", "VNA.DE", "ZAL.DE", "MRK.DE", "LIN.DE", "ENR.DE", "QIA.DE"],
            "SP500": ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "BRK-B", "TSLA", "V", "JPM", "UNH", "JNJ", "XOM", "WMT", "MA", "AVGO", "PG", "ORCL", "CVX", "HD"],
            "NASDAQ": ["AAPL", "MSFT", "AMZN", "NVDA", "AVGO", "META", "ADBE", "COST", "PEP", "NFLX", "AMD", "CMCSA", "TMUS", "TXN", "INTC", "AMGN", "HON", "INTU", "QCOM", "SBUX"]
        }

    @st.cache_data(ttl=300)
    def get_all_stocks_data(_self):
        """Combines all indices into one single massive table with total overviews"""
        try:
            all_tickers = []
            ticker_to_index = {} 
            
            for index_name, tickers in _self.index_config.items():
                for t in tickers:
                    if t not in all_tickers:
                        all_tickers.append(t)
                        ticker_to_index[t] = index_name

            # 1. Download 1 month of data to cover the 30-day calculation
            data = yf.download(all_tickers, period="35d", interval="1d", group_by='ticker', progress=False)
            
            combined_results = []
            
            for ticker in all_tickers:
                try:
                    if ticker not in data.columns.get_level_values(0):
                        continue
                        
                    ticker_df = data[ticker].dropna()
                    
                    if not ticker_df.empty and len(ticker_df) > 1:
                        # Individual Daily Changes
                        pct_changes = ticker_df['Close'].pct_change() * 100
                        current_price = ticker_df['Close'].iloc[-1]
                        
                        # --- Total Performance Calculations ---
                        # 7-Day Total (Price today vs Price 7 trading days ago)
                        price_7d_ago = ticker_df['Close'].iloc[-8] if len(ticker_df) >= 8 else ticker_df['Close'].iloc[0]
                        total_7d_pct = ((current_price - price_7d_ago) / price_7d_ago) * 100
                        
                        # 30-Day Total (Price today vs Price at start of data)
                        price_30d_ago = ticker_df['Close'].iloc[0]
                        total_30d_pct = ((current_price - price_30d_ago) / price_30d_ago) * 100

                        display_name = ticker.split('.')[0]
                        
                        # 2. Build the Row
                        row = {
                            'Index': ticker_to_index[ticker],
                            'Ticker': display_name,
                            'Total 30D %': round(total_30d_pct, 2), # Overview 1
                            'Total 7D %': round(total_7d_pct, 2),   # Overview 2
                            'Today %': round(pct_changes.iloc[-1], 2)
                        }
                        
                        # Add individual daily columns (1 to 7)
                        for i in range(1, 8):
                            if len(pct_changes) > i:
                                row[f'Day -{i} (%)'] = round(pct_changes.iloc[-(i+1)], 2)
                        
                        combined_results.append(row)
                except Exception:
                    continue

            return pd.DataFrame(combined_results)
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return pd.DataFrame()