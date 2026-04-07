import streamlit as st
import time
from datetime import datetime
from data_source_stocks import DataSource 

# Page Setup
st.set_page_config(page_title="Global Market Overview", layout="wide")

def color_values(val):
    if isinstance(val, (int, float)):
        if val > 0: return 'color: #00CC00; font-weight: bold;'
        if val < 0: return 'color: #FF4B4B; font-weight: bold;'
    return ''

def main():
    st.title("🌍 Consolidated Global Market Performance")
    
    # Init Data
    data_source = DataSource()
    
    # Sidebar
    st.sidebar.header("Controls")
    refresh_rate = st.sidebar.slider("Refresh rate (sec)", 60, 600, 300)
    
    if st.sidebar.button("Clear Cache & Refresh"):
        st.cache_data.clear()
        st.rerun()

    # Fetching
    with st.spinner("Downloading 30-day market data..."):
        df = data_source.get_all_stocks_data()

    # Check if we have data
    if df is not None and not df.empty:
        # Search functionality
        search = st.text_input("🔍 Filter by Ticker or Index Name (e.g. SMI, AAPL, DAX)", "")
        
        if search:
            mask = df['Ticker'].str.contains(search, case=False) | \
                   df['Index'].str.contains(search, case=False)
            df_display = df[mask]
        else:
            df_display = df

        # Last updated info
        st.caption(f"Last sync: {datetime.now().strftime('%H:%M:%S')} | Data cached for 5 min.")

        # Formatting
        # We color columns starting from index 2 (Total 30D %) to the end
        try:
            styled_df = df_display.style.map(color_values, subset=df_display.columns[2:]) \
                                       .format(precision=2, na_rep="-")
            
            st.dataframe(
                styled_df, 
                use_container_width=True, 
                height=800, 
                hide_index=True
            )
        except Exception as e:
            st.error(f"Display Error: {e}")
            st.table(df_display.head(20)) # Fallback to standard table if dataframe fails
            
    else:
        st.error("No data found. Markets may be closed or the API is currently throttled.")
        st.info("Try clicking 'Clear Cache & Refresh' in the sidebar.")

    # Refresh
    time.sleep(refresh_rate)
    st.rerun()

if __name__ == "__main__":
    main()