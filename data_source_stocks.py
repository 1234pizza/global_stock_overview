import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime

class DataSource:
    def __init__(self):
        # Comprehensive lists for SMI and DAX 40
        self.index_config = {
            "SMI": {
                "tickers": [
                    "ABBN.SW", "ALC.SW", "CFR.SW", "GEBN.SW", "GIVN.SW", 
                    "HOLN.SW", "KNIN.SW", "LOGN.SW", "LONN.SW", "NESN.SW", 
                    "NOVN.SW", "PGHN.SW", "ROG.SW", "SCMN.SW", "SIKA.SW", 
                    "SLHN.SW", "SOON.SW", "SREN.SW", "UBSG.SW", "ZURN.SW"
                ],
                "suffix": ".SW"
            },
            "DAX": {
                "tickers": [
                    "ADS.DE", "AIR.DE", "ALV.DE", "BAS.DE", "BAYN.DE", "BMW.DE",
                    "CON.DE", "DB1.DE", "DBK.DE", "DHL.DE", "DTE.DE", "EOAN.DE",
                    "IFX.DE", "MBG.DE", "MUV2.DE", "SAP.DE", "SIE.DE", "VOW3.DE",
                    "BEI.DE", "BNR.DE", "CBK.DE", "1COV.DE", "DTG.DE", "FRE.DE",
                    "FME.DE", "HEI.DE", "HEN3.DE", "HLAG.DE", "MTX.DE", "PUM.DE", 
                    "PAH3.DE", "RWE.DE", "SHL.DE", "SY1.DE", "VNA.DE", "ZAL.DE",
                    "MRK.DE", "LIN.DE", "ENR.DE", "QIA.DE"
                ],
                "suffix": ".DE"
            },
            "SP500": {
                # Top 50 of S&P 500 (Add remaining tickers to this list as needed)
                "tickers": [
                    "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", "BRK-B", "TSLA", "V", 
                    "UNH", "JNJ", "XOM", "JPM", "WMT", "MA", "AVGO", "PG", "ORCL", "CVX",
                    "HD", "LLY", "ABBV", "MRK", "COST", "PEP", "ADBE", "KO", "BAC", "TMO",
                    "CSCO", "AVGO", "CRM", "ACN", "ABT", "LIN", "MCD", "DIS", "WFC", "DHR",
                    "PM", "TXN", "INTU", "VZ", "NEE", "AMGN", "RTX", "HON", "LOW", "UNP"
                ],
                "suffix": ""
            },
            "NASDAQ": {
                # Top 50 of NASDAQ 100
                "tickers": [
                    "AAPL", "MSFT", "AMZN", "NVDA", "AVGO", "META", "ADBE", "COST", "PEP", "NFLX", 
                    "AMD", "CMCSA", "TMUS", "TXN", "INTC", "AMGN", "HON", "INTU", "QCOM", "SBUX",
                    "ISRG", "MDLZ", "GILD", "BKNG", "AMAT", "VRTX", "ADI", "ADP", "PANW", "REGN",
                    "PYPL", "MU", "LRCX", "MELI", "MNST", "CSX", "ORLY", "SNPS", "CDNS", "MAR",
                    "KLAC", "CTAS", "ASML", "FTNT", "KDP", "CHTR", "ADSK", "AEP", "PAYX", "DXCM"
                ],
                "suffix": ""
            }
        }

    @st.cache_data(ttl=300) # Cache data for 5 minutes to prevent IP blocks
    def get_data_for_index(_self, index_name):
        """Fetch all stocks for an index with 7-day history"""
        try:
            if index_name not in _self.index_config:
                return pd.DataFrame()

            config = _self.index_config[index_name]
            tickers = config["tickers"]
            suffix = config["suffix"]

            # Download 12 days to ensure we get 8 trading sessions (Today + 7 Hist)
            # Fetching all tickers in ONE call is the most efficient way
            data = yf.download(tickers, period="12d", interval="1d", group_by='ticker', progress=False)
            
            stock_list = []
            
            for ticker in tickers:
                try:
                    # Accessing multi-index dataframe correctly
                    if len(tickers) > 1:
                        ticker_df = data[ticker].dropna()
                    else:
                        ticker_df = data.dropna()

                    if not ticker_df.empty and len(ticker_df) > 1:
                        # Calculate daily percentage change
                        pct_changes = ticker_df['Close'].pct_change() * 100
                        
                        row = {
                            'Ticker': ticker.replace(suffix, ""),
                            'Today %': round(pct_changes.iloc[-1], 2)
                        }

                        # Add Last 7 Days
                        for i in range(1, 8):
                            if len(pct_changes) > i:
                                val = pct_changes.iloc[-(i+1)]
                                row[f'Day -{i} (%)'] = round(val, 2)
                        
                        stock_list.append(row)
                except KeyError:
                    continue # Skip tickers that failed to download

            df = pd.DataFrame(stock_list)
            return df.sort_values('Ticker') if not df.empty else df

        except Exception as error:
            print(f"Error: {error}")
            return pd.DataFrame()