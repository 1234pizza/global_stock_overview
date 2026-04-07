import streamlit as st
import time
from datetime import datetime
from data_source_stocks import DataSource  # Ensure this file contains the class you provided

# 1. Page Configuration
st.set_page_config(
    page_title="Global Market Performance", 
    page_icon="📊", 
    layout="wide"
)

def color_values(val):
    """Applies green color to positive values and red to negative."""
    if isinstance(val, (int, float)):
        color = 'green' if val > 0 else 'red' if val < 0 else 'grey'
        return f'color: {color}; font-weight: bold;'
    return ''

def main():
    # 2. Header and Title
    st.title("📈 Global Index 7-Day Performance")
    st.markdown("Daily percentage changes for the current session and the last 7 trading days.")
    
    # 3. Sidebar Controls
    st.sidebar.header("Settings")
    auto_refresh = st.sidebar.checkbox("Enable Auto Refresh", value=True)
    refresh_interval = st.sidebar.slider("Update Every (sec)", 5, 60, 10)

    # 4. Initialize Data Source
    data_source = DataSource()
    
    # List of indices we want to display
    indices = ["SMI", "DAX", "SP500", "NASDAQ"]
    
    # Show Last Update Time
    current_time = datetime.now().strftime("%H:%M:%S")
    st.info(f"Last data sync: {current_time}")

    # 5. Display Loop for each Index
    for idx_name in indices:
        st.subheader(f"{idx_name} Stocks - Performance History")
        
        # Get data from your DataSource class
        df = data_source.get_data_for_index(idx_name)

        if not df.empty:
            # Apply color coding to all columns except 'Ticker'
            # We use .style to make it look professional
            styled_df = df.style.applymap(color_values, subset=df.columns[1:]) \
                               .format(precision=2, na_rep="-")
            
            # Display the table
            st.dataframe(
                styled_df, 
                use_container_width=True, 
                height=450,
                hide_index=True
            )
        else:
            st.warning(f"No data currently available for {idx_name}.")
        
        st.markdown("---")

    # 6. Auto-Refresh Logic
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()