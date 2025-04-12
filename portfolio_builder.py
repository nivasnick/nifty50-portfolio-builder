import streamlit as st
import pandas as pd

# Set page title
st.title("Build Portfolio from Any NSE Stock")

# Header
st.header("Create Your Custom NSE Portfolio")

# Search box
st.subheader("Search Stocks")
search_query = st.text_input(
    "Type to search stocks (e.g., Reliance, HDFC)",
    placeholder="Enter stock name or symbol"
)

# Multi-select list for stocks
st.subheader("Select Stocks for Your Portfolio")
# Placeholder stock list (to be replaced with dataset later)
placeholder_stocks = ["RELIANCE.NS", "HDFCBANK.NS", "TCS.NS", "INFY.NS"]
selected_stocks = st.multiselect(
    "Select up to 10 stocks",
    options=placeholder_stocks,
    default=[],
    help="Choose stocks to include in your portfolio (max 10)"
)

# Numeric input for investment amount
st.subheader("Investment Details")
investment_amount = st.number_input(
    "Total Investment Amount (INR)",
    min_value=1000.0,
    max_value=10000000.0,
    value=100000.0,
    step=1000.0,
    help="Enter the total amount you want to invest"
)

# Table for selected stocks
st.subheader("Your Portfolio")
# Create dummy data for the table
if selected_stocks:
    dummy_data = {
        "Symbol": selected_stocks,
        "Company_Name": [f"{s.replace('.NS', '')} Ltd" for s in selected_stocks],
        "Current_Price": [3000.0, 1800.0, 4000.0, 1700.0][:len(selected_stocks)],
        "Quantity": [0] * len(selected_stocks),
        "Allocation (%)": [0.0] * len(selected_stocks)
    }
    portfolio_df = pd.DataFrame(dummy_data)
    st.dataframe(portfolio_df, use_container_width=True)
else:
    st.write("No stocks selected. Please choose stocks above.")

# Editable cells for quantity and allocation
if selected_stocks:
    st.markdown("**Edit Quantity or Allocation below for each stock**")
    for stock in selected_stocks:
        col1, col2 = st.columns(2)
        with col1:
            st.number_input(
                f"Quantity for {stock}",
                min_value=0,
                value=0,
                step=1,
                key=f"qty_{stock}"
            )
        with col2:
            st.number_input(
                f"Allocation (%) for {stock}",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=1.0,
                key=f"alloc_{stock}"
            )

# Split Investment button and split type
st.subheader("Finalize Portfolio")
col_button, col_select = st.columns([1, 2])
with col_button:
    st.button("Split Investment", help="Click to split your investment")
with col_select:
    st.selectbox(
        "Split Type",
        options=["Equal", "Custom"],
        index=0,
        help="Choose how to split your investment"
    )
