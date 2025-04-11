import streamlit as st
import requests
import pandas as pd

import matplotlib.pyplot as plt
from collections import defaultdict

import yfinance as yf
import matplotlib.pyplot as plt


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
=======
    st.session_state.selected_stocks = ["Reliance", "TCS", "Infosys"]

# ----------------------------------------
# NIFTY 50 stock tickers (Yahoo Finance format)
# ----------------------------------------
nifty_50_stocks = {
    "Reliance": "RELIANCE.NS", "TCS": "TCS.NS", "Infosys": "INFY.NS", "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS", "Kotak Bank": "KOTAKBANK.NS", "L&T": "LT.NS", "Axis Bank": "AXISBANK.NS",
    "HUL": "HINDUNILVR.NS", "Bajaj Finance": "BAJFINANCE.NS", "SBI": "SBIN.NS", "Maruti": "MARUTI.NS",
    "ITC": "ITC.NS", "Wipro": "WIPRO.NS", "Power Grid": "POWERGRID.NS", "Asian Paints": "ASIANPAINT.NS",
    "NTPC": "NTPC.NS", "Titan": "TITAN.NS", "UltraTech": "ULTRACEMCO.NS", "Bharti Airtel": "BHARTIARTL.NS",
    "Nestle India": "NESTLEIND.NS", "Dr Reddy": "DRREDDY.NS", "HCL Tech": "HCLTECH.NS", "JSW Steel": "JSWSTEEL.NS",
    "Sun Pharma": "SUNPHARMA.NS", "Tata Steel": "TATASTEEL.NS", "Grasim": "GRASIM.NS", "Bajaj Auto": "BAJAJ-AUTO.NS",
    "HDFC Life": "HDFCLIFE.NS", "Tech Mahindra": "TECHM.NS", "IndusInd Bank": "INDUSINDBK.NS",
    "Adani Ports": "ADANIPORTS.NS", "Eicher Motors": "EICHERMOT.NS", "Divi's Labs": "DIVISLAB.NS",
    "Cipla": "CIPLA.NS", "Bajaj Finserv": "BAJAJFINSV.NS", "Tata Motors": "TATAMOTORS.NS",
    "Apollo Hospitals": "APOLLOHOSP.NS", "Coal India": "COALINDIA.NS", "BPCL": "BPCL.NS", "Britannia": "BRITANNIA.NS",
    "ONGC": "ONGC.NS", "Hindalco": "HINDALCO.NS", "Hero MotoCorp": "HEROMOTOCO.NS", "Mahindra & Mahindra": "M&M.NS",
    "SBI Life": "SBILIFE.NS", "Tata Consumer": "TATACONSUM.NS", "UPL": "UPL.NS", "Shree Cements": "SHREECEM.NS",
    "Infratel": "INFRATEL.NS"
}

# ----------------------------------------
# Streamlit App
# ----------------------------------------
st.set_page_config(page_title="NIFTY 50 Portfolio Builder", layout="wide")
st.title("📈 NIFTY 50 Portfolio Builder")

investment_amount = st.number_input("💰 Enter total investment amount (INR)", min_value=1000, step=500)

# ----------------------
# Add user input for custom stock ticker
# ----------------------
custom_ticker = st.text_input("🔎 Add a custom stock ticker (e.g., DMART.NS, IRCTC.NS):")
if custom_ticker:
    custom_name = custom_ticker.upper()
    if custom_name not in nifty_50_stocks:
        nifty_50_stocks[custom_name] = custom_name
        if custom_name not in st.session_state.custom_tickers:
            st.session_state.custom_tickers.append(custom_name)

# ----------------------
# Multi-select list for all stocks
# ----------------------
all_stock_options = list(nifty_50_stocks.keys())
selected = st.multiselect(
    "Choose stocks (NIFTY 50 + custom)",
    options=all_stock_options,
    default=st.session_state.selected_stocks
)
st.session_state.selected_stocks = selected
selected_stocks = selected

# ----------------------
# Allocation logic with editable table
# ----------------------
if selected_stocks:
    per_stock_invest = investment_amount / len(selected_stocks)
    total_allocated = 0
    data = []

    for stock in selected_stocks:
        ticker = nifty_50_stocks.get(stock, stock)
        cmp = get_cmp(ticker)
        if cmp:
            quantity = int(per_stock_invest // cmp)
            investment = round(cmp * quantity, 2)
            allocation = round((investment / investment_amount) * 100, 2)
            data.append({
                "Stock": stock,
                "Ticker": ticker,
                "CMP (₹)": cmp,
                "Quantity": quantity,
                "Investment (₹)": investment,
                "Allocation %": allocation
            })

    df = pd.DataFrame(data)

    st.markdown("### ✏️ Edit Portfolio Table Below")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        disabled=["Stock", "Ticker"],
        key="editable_table"
    )

    # Dynamically recalculate investment values
    edited_df["Investment (₹)"] = edited_df["CMP (₹)"] * edited_df["Quantity"]
    total_allocated = edited_df["Investment (₹)"].sum()
    edited_df["Allocation %"] = round((edited_df["Investment (₹)"] / investment_amount) * 100, 2)

    st.markdown("### 📊 Portfolio Summary")
    st.dataframe(edited_df, use_container_width=True)

    st.success(f"✅ Total Investment Allocated: ₹{round(total_allocated, 2)} out of ₹{investment_amount}")
    
    # ➕ Show Remaining Unallocated Amount
    remaining_amount = round(investment_amount - total_allocated, 2)
    st.info(f"💡 Remaining Unallocated Amount: ₹{remaining_amount}")

   


    # 📥 CSV Download
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Portfolio CSV", csv, "portfolio.csv", "text/csv")


else:
    st.info("Start building your portfolio by searching and adding stocks.")
