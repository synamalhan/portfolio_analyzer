import streamlit as st
import pandas as pd

def display_sidebar():
    # Sidebar header
    st.sidebar.header("Portfolio Editor")

    # Initialize the portfolio DataFrame with one empty row (with placeholder values) using pd.concat
    empty_row = pd.DataFrame({"Ticker": [""], "Shares": [0]})
    portfolio = pd.concat([empty_row], ignore_index=True)

    # Use the data editor to allow users to input stock tickers and number of shares
    portfolio = st.sidebar.data_editor(
        portfolio, 
        use_container_width=True,
        column_order=["Ticker", "Shares"], 
        column_config={
            "Ticker": st.column_config.Text("Stock Ticker"),
            "Shares": st.column_config.Number("Number of Shares", min_value=1),
        },
        num_rows="fixed",  # Fixed number of rows, but editable
        key="portfolio_data_editor"
    )

    # Add a submit button to trigger the portfolio analysis
    submit_button = st.sidebar.button("Submit Portfolio")

    return portfolio, submit_button
