import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from components.sidebar import display_sidebar  # Importing sidebar functionality
from components.calculations import calculate_total_return, calculate_volatility, calculate_sharpe_ratio , get_sector_allocation
from components.graphs import plot_portfolio_performance, plot_individual_stock_contributions , plot_risk_return_scatter
# Main App Configuration
st.set_page_config(page_title="Portfolio Analyzer")

# Title
st.title("Portfolio Performance Analyzer")

# Sidebar Input
portfolio, submit_button = display_sidebar()

# Containers for sections
port = st.expander("📊 Portfolio Data")
calc = st.container(border=True)
sector_analysis = st.container(border=True)
graphs = st.container(border=True)
risk_return_graph = st.container(border=True)

# Process and Display Results
if submit_button:
    if not portfolio.empty and not portfolio["Ticker"].isnull().all():
        portfolio_data = {}
        for index, row in portfolio.iterrows():
            ticker = row["Ticker"]
            shares = row["Shares"]
            if ticker and shares > 0:
                try:
                    data = yf.Ticker(ticker).history(period="1y")
                    data["Portfolio Value"] = data["Close"] * shares
                    portfolio_data[ticker] = data["Portfolio Value"]
                except Exception as e:
                    st.warning(f"Could not fetch data for {ticker}: {e}")

        if portfolio_data:
            # Combine data
            portfolio_df = pd.DataFrame(portfolio_data)
            portfolio_df["Total Portfolio Value"] = portfolio_df.sum(axis=1)

            # Display portfolio data
            port.write(portfolio_df)

            # Calculate performance metrics
            total_return = calculate_total_return(portfolio_df)
            calc.write(f"**Total Return**: {total_return * 100:.2f}%")

            volatility = calculate_volatility(portfolio_df)
            calc.write(f"**Volatility (Risk)**: {volatility * 100:.2f}%")

            sharpe_ratio = calculate_sharpe_ratio(portfolio_df)
            calc.write(f"**Sharpe Ratio**: {sharpe_ratio:.2f}")

            # Plot Portfolio Performance
            graphs.subheader("📈 Portfolio Performance Over Time")
            fig = plot_portfolio_performance(portfolio_df)
            graphs.plotly_chart(fig)

            # Plot individual stock contributions
            graphs.subheader("📊 Individual Stock Contributions")
            fig = plot_individual_stock_contributions(portfolio_df)
            graphs.plotly_chart(fig)

            # Sector Allocation Analysis
            sector_allocation = get_sector_allocation(portfolio_df, portfolio)
            if sector_allocation:
                sector_df = pd.DataFrame(
                    list(sector_allocation.items()), columns=["Sector", "Allocation"]
                )
                fig = px.pie(
                    sector_df,
                    values="Allocation",
                    names="Sector",
                    title="Sector Allocation Breakdown",
                    color_discrete_sequence=px.colors.sequential.Viridis,
                )
                sector_analysis.subheader("Sector Analysis")
                sector_analysis.write("### Sector Allocation Breakdown")
                sector_analysis.plotly_chart(fig)

            # Risk-Return Scatter Plot
            fig = plot_risk_return_scatter(portfolio_df, portfolio)
            if fig:
                risk_return_graph.subheader("📊 Risk vs. Return")
                risk_return_graph.plotly_chart(fig)
            else:
                st.warning("Could not generate risk-return scatter plot.")
        else:
            st.error("No valid stocks in portfolio. Please check the tickers.")
    else:
        st.sidebar.error("Please enter valid stock tickers and the number of shares.")
else:
    st.sidebar.info("Enter stock tickers and number of shares, then click Submit.")