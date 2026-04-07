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
    st.title("🌍 Consolidated Global Stock Performance")
    st.markdown("All stocks from SMI, DAX, S&P 500, and NASDAQ in a single view.")
    
    data_source = DataSource()
    
    # Sidebar Info
    st.sidebar.header("Status")
    refresh_rate = st.sidebar.slider("Refresh Interval (sec)", 60, 600, 300)
    current_time = datetime.now().strftime("%H:%M:%S")
    st.sidebar.write(f"**Last Sync:** {current_time}")

    # Fetch Consolidated Data
    with st.spinner("Downloading all market data..."):
        df = data_source.get_all_stocks_data()

    if not df.empty:
        # Search/Filter functionality (very useful for one big list)
        search_query = st.text_input("🔍 Search for a Ticker or Index (e.g., 'SMI' or 'AAPL')")
        if search_query:
            df = df[df.apply(lambda row: search_query.upper() in row.astype(str).get('Ticker', '').upper() or 
                                        search_query.upper() in row.astype(str).get('Index', '').upper(), axis=1)]

        # Apply styling to all percentage columns (Today % and Day -1 to -7)
        # These start from the 3rd column (index 2) onwards
        styled_df = df.style.map(color_values, subset=df.columns[2:]) \
                           .format(precision=2, na_rep="-")
        
        st.dataframe(
            styled_df, 
            use_container_width=True, 
            height=800, # Taller height for the big list
            hide_index=True
        )
    else:
        st.error("Could not retrieve data. Please check your connection.")

    # Refresh timer
    time.sleep(refresh_rate)
    st.rerun()

if __name__ == "__main__":
    main()