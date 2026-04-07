import streamlit as st
import time
from datetime import datetime
from data_source_stocks import DataSource 

st.set_page_config(page_title="Market Overview", layout="wide")

def color_values(val):
    if isinstance(val, (int, float)):
        if val > 0: return 'color: #00CC00; font-weight: bold;'
        if val < 0: return 'color: #FF4B4B; font-weight: bold;'
    return ''

def main():
    st.title("🌍 Global Stock Performance (Consolidated)")
    
    # Initialize outside the loop
    data_source = DataSource()
    
    # Sidebar
    st.sidebar.header("Control Panel")
    refresh_rate = st.sidebar.slider("Auto-Refresh (sec)", 60, 600, 300)
    
    with st.spinner("Syncing with Global Markets..."):
        # Call the new consolidated method
        df = data_source.get_all_stocks_data()

    if df is not None and not df.empty:
        # Search Box
        search = st.text_input("🔍 Search Ticker or Index", "")
        if search:
            mask = df['Ticker'].str.contains(search, case=False) | df['Index'].str.contains(search, case=False)
            df_display = df[mask]
        else:
            df_display = df

        # Styling
        styled_df = df_display.style.map(color_values, subset=df_display.columns[2:]) \
                                   .format(precision=2, na_rep="-")
        
        st.dataframe(styled_df, use_container_width=True, height=800, hide_index=True)
    else:
        st.warning("No data retrieved. Yahoo Finance might be throttled or markets are closed.")

    time.sleep(refresh_rate)
    st.rerun()

if __name__ == "__main__":
    main()