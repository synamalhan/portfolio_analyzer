import matplotlib.pyplot as plt

def plot_portfolio_performance(portfolio_df):
    fig, ax = plt.subplots(figsize=(10, 6))
    portfolio_df['Total Portfolio Value'].plot(ax=ax)
    ax.set_title("Portfolio Performance")
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value ($)")
    return fig

def plot_individual_stock_contributions(portfolio_df):
    fig, ax = plt.subplots(figsize=(10, 6))
    portfolio_df.plot(ax=ax)
    ax.set_title("Individual Stock Contributions to Portfolio")
    ax.set_xlabel("Date")
    ax.set_ylabel("Stock Value ($)")
    return fig
