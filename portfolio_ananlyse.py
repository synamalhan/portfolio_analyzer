import streamlit as st
import yfinance as yf
import pandas as pd
from components.sidebar import display_sidebar  # Importing sidebar functionality
from components.calculations import calculate_total_return, calculate_volatility, calculate_sharpe_ratio  # Importing calculation functions
from components.graphs import plot_portfolio_performance, plot_individual_stock_contributions  # Importing graph functions

# Title for the app
st.title("Portfolio Performance Analyzer")

# Display the sidebar and get portfolio data
portfolio, submit_button = display_sidebar()

# Process and display results after the submit button is clicked
if submit_button:
    if not portfolio.empty and not portfolio["Ticker"].isnull().all():
        # Fetch historical stock data for each ticker in the portfolio
        portfolio_data = {}
        for index, row in portfolio.iterrows():
            ticker = row["Ticker"]
            shares = row["Shares"]
            if ticker != "" and shares > 0:
                data = yf.Ticker(ticker).history(period="1y")  # 1 year of historical data
                data['Portfolio Value'] = data['Close'] * shares
                portfolio_data[ticker] = data['Portfolio Value']

        if portfolio_data:
            # Combine data for all stocks into a single DataFrame
            portfolio_df = pd.DataFrame(portfolio_data)

            # Calculate total portfolio value (sum of individual stock values)
            portfolio_df['Total Portfolio Value'] = portfolio_df.sum(axis=1)

            # Display portfolio data
            st.subheader("Portfolio Data")
            st.write(portfolio_df)

            # Calculate performance metrics using functions from calculations.py
            total_return = calculate_total_return(portfolio_df)
            st.write(f"**Total Return**: {total_return * 100:.2f}%")

            # Calculate volatility (annualized)
            volatility = calculate_volatility(portfolio_df)
            st.write(f"**Volatility (Risk)**: {volatility * 100:.2f}%")

            # Calculate Sharpe ratio (assuming a 0% risk-free rate)
            sharpe_ratio = calculate_sharpe_ratio(portfolio_df)
            st.write(f"**Sharpe Ratio**: {sharpe_ratio:.2f}")

            # Plot portfolio performance over time using the graph function
            st.subheader("Portfolio Performance Over Time")
            fig = plot_portfolio_performance(portfolio_df)
            st.pyplot(fig)

            # Plot individual stock contributions using the graph function
            st.subheader("Individual Stock Contributions")
            fig = plot_individual_stock_contributions(portfolio_df)
            st.pyplot(fig)
        else:
            st.write("No valid stocks in portfolio.")
    else:
        st.sidebar.write("Please enter stock tickers and the number of shares.")
else:
    st.sidebar.write("Enter stock tickers and number of shares, then click Submit.")
