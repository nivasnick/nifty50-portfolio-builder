import streamlit as st
import requests
import pandas as pd
import yfinance as yf

# Constants
API_KEY = "your_api_key_here"  # Replace with your actual API Key from financialmodelingprep.com
SEARCH_API = "https://financialmodelingprep.com/api/v3/search"

# NIFTY 50 stock tickers (Yahoo Finance format)
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

# Helper function to get current market price
def get_cmp(ticker):
    try:
        stock = yf.Ticker(ticker)
        return round(stock.history(period="1d")["Close"].iloc[-1], 2)
    except:
        return None

# Set page config
st.set_page_config(page_title="NIFTY50 Portfolio Builder", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    .stButton>button {background-color: #007bff; color: white; border-radius: 5px;}
    .stButton>button:hover {background-color: #0056b3;}
    .stTextInput>label {font-size: 1.1rem; font-weight: bold;}
    .stNumberInput>label {font-size: 1.1rem; font-weight: bold;}
    .stSelectbox>label {font-size: 1.1rem; font-weight: bold;}
    .stMultiSelect>label {font-size: 1.1rem; font-weight: bold;}
    .sidebar .sidebar-content {background-color: #ffffff;}
    .stAlert {border-radius: 5px;}
    </style>
""", unsafe_allow_html=True)

# Sidebar for portfolio controls
with st.sidebar:
    st.header("Portfolio Controls")
    investment_amount = st.number_input("💰 Investment Amount (INR)", min_value=1000, step=500, value=10000)
    if st.button("🗑️ Clear Portfolio"):
        st.session_state.selected_stocks = []
        st.session_state.custom_tickers = []
        st.rerun()

# Initialize session state
if "selected_stocks" not in st.session_state:
    st.session_state.selected_stocks = []
if "custom_tickers" not in st.session_state:
    st.session_state.custom_tickers = []

# Main title
st.title("📊 NIFTY50 Portfolio Builder")
st.markdown("Build your portfolio with NIFTY50 stocks and customize your investments.")

# Two-column layout
col1, col2 = st.columns([2, 1])

with col1:
    # Stock selection section
    st.subheader("🔍 Add Stocks to Portfolio")
    query = st.text_input("Search stock name or symbol (e.g., INFY, TCS)", placeholder="Type to search...")
    
    if query:
        with st.spinner("Searching stocks..."):
            response = requests.get(f"{SEARCH_API}?query={query}&limit=10&exchange=NS&apikey={API_KEY}")
            if response.status_code == 200:
                suggestions = response.json()
                stock_options = [f"{item['symbol']} - {item['name']}" for item in suggestions if 'symbol' in item and 'name' in item]
                
                if stock_options:
                    selected_stock = st.selectbox("Select a stock:", stock_options, key="stock_select")
                    if st.button("➕ Add Stock"):
                        symbol = selected_stock.split(" - ")[0]
                        if symbol not in st.session_state.selected_stocks:
                            st.session_state.selected_stocks.append(symbol)
                            st.success(f"✅ {symbol} added to portfolio!")
                        else:
                            st.info(f"ℹ️ {symbol} is already in your portfolio.")
                else:
                    st.warning("⚠️ No matching stocks found.")
            else:
                st.error("❌ Failed to fetch data. Check your API key or connection.")

    # Custom ticker input
    custom_ticker = st.text_input("🔎 Add Custom Ticker (e.g., DMART.NS)", placeholder="Enter ticker...")
    if custom_ticker:
        custom_name = custom_ticker.upper()
        if custom_name not in nifty_50_stocks:
            nifty_50_stocks[custom_name] = custom_name
            if custom_name not in st.session_state.custom_tickers:
                st.session_state.custom_tickers.append(custom_name)
                st.success(f"✅ Custom ticker {custom_name} added!")

with col2:
    # Selected stocks display
    if st.session_state.selected_stocks:
        st.subheader("📋 Your Portfolio")
        for stock in st.session_state.selected_stocks:
            if st.button(f"🗑️ Remove {stock}", key=f"remove_{stock}"):
                st.session_state.selected_stocks.remove(stock)
                st.rerun()
            st.markdown(f"**{stock}**")

# Portfolio allocation and summary
if st.session_state.selected_stocks:
    st.subheader("📊 Portfolio Allocation")
    per_stock_invest = investment_amount / len(st.session_state.selected_stocks)
    data = []

    for stock in st.session_state.selected_stocks:
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
    
    # Editable table
    st.markdown("### ✏️ Edit Your Portfolio")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        disabled=["Stock", "Ticker", "CMP (₹)", "Investment (₹)", "Allocation %"],
        column_config={
            "Quantity": st.column_config.NumberColumn(min_value=0, step=1)
        },
        key="portfolio_table"
    )

    # Recalculate investment values
    edited_df["Investment (₹)"] = edited_df["CMP (₹)"] * edited_df["Quantity"]
    total_allocated = edited_df["Investment (₹)"].sum()
    edited_df["Allocation %"] = round((edited_df["Investment (₹)"] / total_allocated) * 100, 2) if total_allocated > 0 else 0

    # Display summary
    st.markdown("### 📈 Portfolio Summary")
    st.dataframe(edited_df.style.format({
        "CMP (₹)": "₹{:.2f}",
        "Investment (₹)": "₹{:.2f}",
        "Allocation %": "{:.2f}%"
    }), use_container_width=True)

    # Allocation feedback
    remaining_amount = investment_amount - total_allocated
    st.success(f"✅ Total Allocated: ₹{round(total_allocated, 2)}")
    if remaining_amount > 0:
        st.info(f"💡 Unallocated Amount: ₹{round(remaining_amount, 2)}")
    elif remaining_amount < 0:
        st.warning(f"⚠️ Over-allocated by: ₹{-round(remaining_amount, 2)}")

    # CSV download
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Portfolio as CSV", csv, "portfolio.csv", "text/csv")
else:
    st.info("👉 Start by searching and adding stocks to build your portfolio!")
