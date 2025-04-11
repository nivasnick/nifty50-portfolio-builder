import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Constants
API_KEY = "your_api_key_here"  # Replace with your actual API Key from financialmodelingprep.com
SEARCH_API = "https://financialmodelingprep.com/api/v3/search"
PROFILE_API = "https://financialmodelingprep.com/api/v3/profile"

st.set_page_config(page_title="NIFTY50 Portfolio Builder", layout="wide")
st.title("📊 NIFTY50 Portfolio Builder with Industry Allocation")

# Initialize session state
if "selected_stocks" not in st.session_state:
    st.session_state.selected_stocks = []

if "stock_industries" not in st.session_state:
    st.session_state.stock_industries = {}

# Search and select stock
st.subheader("🔍 Search and Add Stocks to Portfolio")
query = st.text_input("Type stock name or symbol (e.g. INFY, TCS)")

if query:
    response = requests.get(f"{SEARCH_API}?query={query}&limit=10&exchange=NS&apikey={API_KEY}")
    if response.status_code == 200:
        suggestions = response.json()
        stock_options = [f"{item['symbol']} - {item['name']}" for item in suggestions if 'symbol' in item and 'name' in item]

        if stock_options:
            selected_stock = st.selectbox("Select a stock to add to portfolio:", stock_options)
            if st.button("Add to Portfolio"):
                symbol = selected_stock.split(" - ")[0]
                if symbol not in st.session_state.selected_stocks:
                    st.session_state.selected_stocks.append(symbol)

                    # Fetch industry
                    profile_resp = requests.get(f"{PROFILE_API}/{symbol}?apikey={API_KEY}")
                    if profile_resp.status_code == 200:
                        profile_data = profile_resp.json()
                        if profile_data:
                            industry = profile_data[0].get("industry", "Unknown")
                            st.session_state.stock_industries[symbol] = industry
                    st.success(f"✅ {symbol} added to portfolio!")
                else:
                    st.info(f"ℹ️ {symbol} is already in your portfolio.")
        else:
            st.warning("No matching stocks found.")
    else:
        st.error("Failed to fetch data. Check your API key or internet connection.")

# Display selected stocks
if st.session_state.selected_stocks:
    st.subheader("📦 Selected Stocks")
    for stock in st.session_state.selected_stocks:
        industry = st.session_state.stock_industries.get(stock, "Unknown")
        st.write(f"- **{stock}** ({industry})")

    # Group by industry for pie chart
    industry_alloc = defaultdict(int)
    for symbol in st.session_state.selected_stocks:
        industry = st.session_state.stock_industries.get(symbol, "Unknown")
        industry_alloc[industry] += 1

    # Plot Pie Chart
    st.subheader("📈 Industry Allocation")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(industry_alloc.values(), labels=industry_alloc.keys(), autopct='%1.1f%%', startangle=140, textprops={'fontsize': 10})
    ax.axis('equal')
    st.pyplot(fig)
else:
    st.info("Start building your portfolio by searching and adding stocks.")
