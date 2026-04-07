import streamlit as st
import time
from datetime import datetime
from data_source_stocks import DataSource 

st.set_page_config(page_title="Global Market Overview", layout="wide")

def color_values(val):
    if isinstance(val, (int, float)):
        if val > 0: return 'color: #00CC00; font-weight: bold;'
        if val < 0: return 'color: #FF4B4B; font-weight: bold;'
    return ''

def main():
    st.title("🌍 Consolidated Global Market Performance")
    st.markdown("Overview: **1-Month** and **5-Day (Weekly)** totals with daily breakdown.")
    
    data_source = DataSource()
    
    # Sidebar
    st.sidebar.header("Controls")
    refresh_rate = st.sidebar.slider("Refresh rate (sec)", 60, 600, 300)
    
    if st.sidebar.button("Clear Cache & Refresh"):
        st.cache_data.clear()
        st.rerun()

    # Fetching
    with st.spinner("Downloading monthly market data..."):
        df = data_source.get_all_stocks_data()

    if df is not None and not df.empty:
        # Search Box
        search = st.text_input("🔍 Search Ticker or Index", "")
        
        if search:
            mask = df['Ticker'].str.contains(search, case=False) | \
                   df['Index'].str.contains(search, case=False)
            df_display = df[mask]
        else:
            df_display = df

        st.caption(f"Last sync: {datetime.now().strftime('%H:%M:%S')} | 5-minute cache active.")

        # Formatting: Color from column index 2 (Total 1M %) onwards
        styled_df = df_display.style.map(color_values, subset=df_display.columns[2:]) \
                                   .format(precision=2, na_rep="-")
        
        st.dataframe(
            styled_df, 
            use_container_width=True, 
            height=800, 
            hide_index=True
        )
            
    else:
        st.error("No data found. Please check your connection or 'Clear Cache'.")

    # Refresh Timer
    time.sleep(refresh_rate)
    st.rerun()

if __name__ == "__main__":
    main()