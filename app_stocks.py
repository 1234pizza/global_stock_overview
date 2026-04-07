import streamlit as st
import time
from datetime import datetime
from data_source_stocks import DataSource 

# 1. Page Configuration
st.set_page_config(
    page_title="Global Market Monitor", 
    page_icon="📈", 
    layout="wide"
)

def color_values(val):
    """Applies green for gains and red for losses."""
    if isinstance(val, (int, float)):
        if val > 0:
            return 'color: #00CC00; font-weight: bold;'
        elif val < 0:
            return 'color: #FF4B4B; font-weight: bold;'
    return ''

def main():
    # 2. Header and Title
    st.title("🌍 Global Stock Performance (Consolidated)")
    st.markdown("""
        This view combines **SMI, DAX, S&P 500, and NASDAQ**. 
        Includes **30-Day/7-Day Overviews** and daily percentage changes.
    """)
    
    # 3. Sidebar Controls
    st.sidebar.header("Dashboard Settings")
    refresh_rate = st.sidebar.slider("Auto-Refresh Interval (sec)", 60, 600, 300)
    
    if st.sidebar.button("🔄 Force Refresh Now"):
        st.cache_data.clear()
        st.rerun()

    # Initialize Data Source
    data_source = DataSource()
    
    # 4. Data Fetching
    with st.spinner("Syncing global market data (30-day window)..."):
        df = data_source.get_all_stocks_data()

    # 5. Display Logic
    if df is not None and not df.empty:
        # Status Info
        current_time = datetime.now().strftime("%H:%M:%S")
        st.sidebar.success(f"Last Sync: {current_time}")
        st.sidebar.info("Note: Data is cached for 5 minutes to prevent API throttling.")

        # Search / Filter Bar
        search_query = st.text_input("🔍 Search by Ticker or Index (e.g., 'UBS', 'AAPL', or 'DAX')", "")
        
        if search_query:
            # Filter the dataframe based on Ticker or Index columns
            mask = (df['Ticker'].str.contains(search_query, case=False)) | \
                   (df['Index'].str.contains(search_query, case=False))
            display_df = df[mask]
        else:
            display_df = df

        # 6. Table Styling
        # We start coloring from the 3rd column (index 2) onwards: 
        # (Total 30D, Total 7D, Today, Day -1, etc.)