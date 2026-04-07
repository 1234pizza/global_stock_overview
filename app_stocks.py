import streamlit as st  # Web app framework
import time  # For creating delays
from datetime import datetime  # For working with time
from data_source_stocks import DataSource  # Our data getting class
from charts_stocks import ChartCreator  # Our chart creating class

# Configure our web page
st.set_page_config(
    page_title="Global Market Dashboard", 
    page_icon="📈", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

def main():
    """Main function that runs our Multi-Index dashboard"""

    # 1. Page Setup
    st.title("🌍 Global Market Indices Live")
    st.markdown("Real-time tracking of SMI, DAX, S&P 500, and NASDAQ 100.")
    st.markdown("---")

    # 2. Sidebar Controls
    st.sidebar.header("Dashboard Settings")
    auto_refresh = st.sidebar.checkbox(
        "Enable Auto Refresh",
        value=True,
        help="Automatically update stock data every few seconds"
    )

    refresh_interval = st.sidebar.slider(
        "Update Every (seconds)",
        min_value=5,
        max_value=60,
        value=10
    )

    # 3. Initialize Classes
    data_source = DataSource()
    chart_creator = ChartCreator()

    # 4. Content Containers
    status_container = st.empty()
    
    # We create a dictionary of containers for each index
    indices = {
        "SMI": {"title": "🇨🇭 Swiss Market Index (SMI)", "icon": "CHF"},
        "DAX": {"title": "🇩🇪 German Stock Index (DAX)", "icon": "EUR"},
        "SP500": {"title": "🇺🇸 S&P 500", "icon": "USD"},
        "NASDAQ": {"title": "🇺🇸 NASDAQ 100", "icon": "USD"}
    }
    
    # Pre-create UI containers to prevent jumping
    containers = {key: st.container() for key in indices.keys()}

    update_count = 0

    # 5. The Live Update Loop
    while True:
        update_count += 1
        current_time = datetime.now().strftime("%H:%M:%S")
        status_container.info(f"Last updated: {current_time} (Update #{update_count})")

        # Loop through each index and update its specific section
        for key, info in indices.items():
            with containers[key]:
                st.header(info["title"])
                
                # Logic assumes your data_source can take an index name
                # If your methods are hardcoded for SMI, you'll need to update data_source.py
                data = data_source.get_data_for_index(key) 

                if not data.empty:
                    # Create metrics and charts specifically for this index
                    chart_creator.create_summary_metrics(data)
                    
                    st.subheader(f"{key} Performance ({info['icon']})")
                    fig = chart_creator.create_index_chart(data, key)
                    st.plotly_chart(fig, use_container_width=True, key=f"{key}_chart_{update_count}")
                    
                    with st.expander(f"View {key} Raw Data"):
                        st.dataframe(data, use_container_width=True)
                else:
                    st.warning(f"Waiting for {key} data...")
                
                st.markdown("---")

        # 6. Loop Logic
        if not auto_refresh:
            break
            
        time.sleep(refresh_interval)
        if auto_refresh:
            st.rerun()

if __name__ == "__main__":
    main()