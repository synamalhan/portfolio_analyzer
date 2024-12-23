import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Title for the app
st.title("Portfolio Performance Analyzer")

# Sidebar header
st.sidebar.header("Portfolio Editor")

portfolio = pd.DataFrame(columns=["Ticker", "Shares"])


# Use the data editor to allow users to input stock tickers and number of shares
portfolio = st.sidebar.data_editor(
    portfolio, 
    use_container_width=True,
    column_order=["Ticker", "Shares"], 
    column_config={
        "Ticker": st.column_config.TextColumn("Stock Ticker"),
        "Shares": st.column_config.NumberColumn("Number of Shares", min_value=1),
    },
    num_rows="dynamic",
    key="portfolio_data_editor"
)

# Add a submit button to trigger the portfolio analysis
submit_button = st.sidebar.button("Submit Portfolio")

# Process and display results after the submit button is clicked
if submit_button:
    if not portfolio.empty:
        # Fetch historical stock data for each ticker in the portfolio
        portfolio_data = {}
        for index, row in portfolio.iterrows():
            ticker = row["Ticker"]
            shares = row["Shares"]
            data = yf.Ticker(ticker).history(period="1y")  # 1 year of historical data
            data['Portfolio Value'] = data['Close'] * shares
            portfolio_data[ticker] = data['Portfolio Value']

        # Combine data for all stocks into a single DataFrame
        portfolio_df = pd.DataFrame(portfolio_data)

        # Calculate total portfolio value (sum of individual stock values)
        portfolio_df['Total Portfolio Value'] = portfolio_df.sum(axis=1)

        # Display portfolio data
        st.subheader("Portfolio Data")
        st.write(portfolio_df)

        # Calculate performance metrics
        total_return = (portfolio_df['Total Portfolio Value'][-1] / portfolio_df['Total Portfolio Value'][0]) - 1
        st.write(f"**Total Return**: {total_return * 100:.2f}%")

        # Calculate daily returns and volatility (annualized)
        daily_returns = portfolio_df['Total Portfolio Value'].pct_change()
        volatility = daily_returns.std() * (252**0.5)  # Annualized volatility
        st.write(f"**Volatility (Risk)**: {volatility * 100:.2f}%")

        # Sharpe ratio (assuming a 0% risk-free rate)
        risk_free_rate = 0.0
        annualized_return = daily_returns.mean() * 252
        sharpe_ratio = (annualized_return - risk_free_rate) / volatility
        st.write(f"**Sharpe Ratio**: {sharpe_ratio:.2f}")

        # Plot portfolio value over time
        st.subheader("Portfolio Performance Over Time")
        fig, ax = plt.subplots(figsize=(10, 6))
        portfolio_df['Total Portfolio Value'].plot(ax=ax)
        ax.set_title("Portfolio Performance")
        ax.set_xlabel("Date")
        ax.set_ylabel("Portfolio Value ($)")
        st.pyplot(fig)

        # Additional visualization for individual stocks
        st.subheader("Individual Stock Contributions")
        fig, ax = plt.subplots(figsize=(10, 6))
        portfolio_df.plot(ax=ax)
        ax.set_title("Individual Stock Contributions to Portfolio")
        ax.set_xlabel("Date")
        ax.set_ylabel("Stock Value ($)")
        st.pyplot(fig)

    else:
        st.sidebar.write("Please enter stock tickers and the number of shares.")
else:
    st.sidebar.write("Enter stock tickers and number of shares, then click Submit.")
