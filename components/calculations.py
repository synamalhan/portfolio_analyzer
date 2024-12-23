import pandas as pd

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
