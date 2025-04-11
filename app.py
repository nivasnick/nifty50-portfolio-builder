import streamlit as st 
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# ----------------------------------------
# Function to fetch CMP (no default fallback)
# ----------------------------------------
def get_cmp(stock_ticker):
    try:
        data = yf.Ticker(stock_ticker)
        cmp = data.info.get('currentPrice')
        if cmp is None:
            cmp = data.info.get('regularMarketPrice')
        if cmp is None:
            hist = data.history(period="1d")
            cmp = hist['Close'].iloc[-1] if not hist.empty else None
        return round(cmp, 2) if cmp else None
    except Exception as e:
        print(f"⚠️ Failed to fetch CMP for {stock_ticker}: {e}")
        return None

# ----------------------------------------
# Initialize session state
# ----------------------------------------
if "custom_tickers" not in st.session_state:
    st.session_state.custom_tickers = []

if "selected_stocks" not in st.session_state:
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

    # Pie Chart for Allocation %
    st.markdown("### 🥧 Allocation Pie Chart")

    fig, ax = plt.subplots()
    ax.pie(
        edited_df["Investment (₹)"],
        labels=edited_df["Stock"],
        autopct="%1.1f%%",
        startangle=90
        )
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig)

    # 📥 CSV Download
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Portfolio CSV", csv, "portfolio.csv", "text/csv")

else:
    st.warning("Please select at least one stock to build your portfolio.")

