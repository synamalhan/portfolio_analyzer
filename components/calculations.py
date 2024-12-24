import pandas as pd
import yfinance as yf
import streamlit as st

def calculate_total_return(portfolio_df):

    initial_value = portfolio_df['Total Portfolio Value'][0]
    final_value = portfolio_df['Total Portfolio Value'][-1]
    return (final_value / initial_value) - 1

def calculate_volatility(portfolio_df):

    daily_returns = portfolio_df['Total Portfolio Value'].pct_change()
    volatility = daily_returns.std() * (252 ** 0.5)  # Annualized volatility
    return volatility

def calculate_sharpe_ratio(portfolio_df, risk_free_rate=0.0):

    daily_returns = portfolio_df['Total Portfolio Value'].pct_change()
    annualized_return = daily_returns.mean() * 252
    volatility = calculate_volatility(portfolio_df)
    sharpe_ratio = (annualized_return - risk_free_rate) / volatility
    return sharpe_ratio


def get_sector_allocation(portfolio_df, portfolio):
    sectors = {}
    total_portfolio_value = portfolio_df['Total Portfolio Value'].iloc[-1]

    for index, row in portfolio.iterrows():
        ticker = row["Ticker"]
        shares = row["Shares"]
        if ticker and shares > 0:
            try:
                info = yf.Ticker(ticker).info
                sector = info.get("sector", "Unknown")
                if sector not in sectors:
                    sectors[sector] = 0
                sectors[sector] += portfolio_df[ticker].iloc[-1]  # Last value for the stock
            except Exception:
                st.warning(f"Could not fetch sector information for {ticker}.")
    
    # Convert to percentages
    sector_allocation = {sector: (value / total_portfolio_value) * 100 for sector, value in sectors.items()}
    return sector_allocation
