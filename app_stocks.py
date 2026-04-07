import streamlit as st
import time
from datetime import datetime
from data_source_stocks import DataSource 

st.set_page_config(
    page_title="Global Market Performance", 
    page_icon="📊", 
    layout="wide"
)

def color_values(val):
    if isinstance(val, (int, float)):
        color = 'green' if val > 0 else 'red' if val < 0 else '#cccccc'
        return f'color: {color}; font-weight: bold;'
    return ''

def main():
    st.title("📈 Global Index 7-Day Performance")
    st.markdown("Real-time percentage changes and 7-day history.")
    
    st.sidebar.header("Settings")
    auto_refresh = st.sidebar.checkbox("Enable Auto Refresh", value=True)
    refresh_interval = st.sidebar.slider("Update Every (sec)", 5, 60, 10)

    data_source = DataSource()
    indices = ["SMI", "DAX", "SP500", "NASDAQ"]
    
    current_time = datetime.now().strftime("%H:%M:%S")
    st.info(f"Last data sync: {current_time}")

    for idx_name in indices:
        st.subheader(f"{idx_name} Stocks")
        
        df = data_source.get_data_for_index(idx_name)

        if not df.empty:
            # subset=df.columns[2:] ensures we skip 'Ticker' and 'Name'
            styled_df = df.style.map(color_values, subset=df.columns[2:]) \
                               .format(precision=2, na_rep="-")
            
            st.dataframe(
                styled_df, 
                use_container_width=True, 
                height=450,
                hide_index=True
            )
        else:
            st.warning(f"No data currently available for {idx_name}.")
        
        st.markdown("---")

    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()