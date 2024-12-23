import streamlit as st
import pandas as pd
import yfinance as yf

# Function to display the sidebar and handle portfolio input
def display_sidebar():
    # Sidebar header
    st.sidebar.title("Portfolio Editor")

    with st.sidebar.popover("How This Tool Works"):
        st.write("""
            This tool allows you to input stock tickers and the number of shares 
            you hold for each stock in your portfolio. It will validate the entered 
            tickers and shares, ensuring:
            
            1. Ticker symbols are valid and exist on Yahoo Finance.
            2. The number of shares is greater than 0.
            
            If any issues are detected, an appropriate error message will be displayed.
            Once your portfolio is valid, you can proceed to analysis.
        """)


    portfolio = pd.DataFrame(columns=["Ticker", "Shares"])

    portfolio = st.sidebar.data_editor(
        portfolio, 
        use_container_width=True,
        column_order=["Ticker", "Shares"], 
        column_config={
            "Ticker": st.column_config.TextColumn("Stock Ticker"),
            "Shares": st.column_config.NumberColumn("Number of Shares", min_value=1),
        },
        num_rows="dynamic",  # Fixed number of rows, but editable
        key="portfolio_data_editor"
    )

    # Add a submit button to trigger the portfolio analysis
    submit_button = st.sidebar.button("Submit Portfolio", type="primary")

    # Validate input when the submit button is pressed
    if submit_button:
        invalid_rows = []

        for idx, row in portfolio.iterrows():
            ticker = row['Ticker']
            shares = row['Shares']

            # Check if the ticker is empty
            if not ticker.strip():
                invalid_rows.append(f"Row {idx+1}: Ticker is empty. Please enter a valid ticker.")

            # Check if the number of shares is valid
            if shares <= 0:
                invalid_rows.append(f"Row {idx+1}: Invalid Shares - {shares}. Shares must be greater than 0.")

            # Check if the ticker exists by trying to fetch data using yfinance
            if ticker.strip():
                try:
                    stock_data = yf.Ticker(ticker).history(period="1d")
                    if stock_data.empty:
                        invalid_rows.append(f"Row {idx+1}: No data found for ticker '{ticker}'. Please enter a valid ticker.")
                except Exception as e:
                    invalid_rows.append(f"Row {idx+1}: Error fetching data for ticker '{ticker}': {e}")

        # Display error messages if any validation fails
        if invalid_rows:
            for error in invalid_rows:
                st.sidebar.error(error)
        else:
            st.sidebar.success("Portfolio is valid! Ready for analysis.")

    return portfolio, submit_button

