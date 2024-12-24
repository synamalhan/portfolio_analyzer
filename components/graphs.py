import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import plotly.express as px
import yfinance as yf

def plot_portfolio_performance(portfolio_df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=portfolio_df.index,
        y=portfolio_df['Total Portfolio Value'],
        mode='lines',
        name='Total Portfolio Value',
        line=dict(color='purple')
    ))

    fig.update_layout(
        title="Portfolio Performance",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        template="plotly_dark"
    )

    return fig

def plot_individual_stock_contributions(portfolio_df):
    fig = go.Figure()

    for column in portfolio_df.columns:
        if column != 'Total Portfolio Value':
            fig.add_trace(go.Scatter(
                x=portfolio_df.index,
                y=portfolio_df[column],
                mode='lines',
                name=column
            ))

    fig.update_layout(
        title="Individual Stock Contributions to Portfolio",
        xaxis_title="Date",
        yaxis_title="Stock Value ($)",
        template="plotly_dark"
    )

    return fig


def plot_risk_return_scatter(portfolio_df, portfolio):
    risk_return_data = []

    for index, row in portfolio.iterrows():
        ticker = row["Ticker"]
        shares = row["Shares"]
        if ticker and shares > 0:
            try:
                data = yf.Ticker(ticker).history(period="1y")
                returns = data["Close"].pct_change().dropna()
                mean_return = returns.mean() * 252  # Annualized return
                risk = returns.std() * (252 ** 0.5)  # Annualized risk
                weight = portfolio_df[ticker].iloc[-1] / portfolio_df["Total Portfolio Value"].iloc[-1]
                risk_return_data.append({"Ticker": ticker, "Return": mean_return, "Risk": risk, "Weight": weight})
            except Exception:
                st.warning(f"Could not fetch risk-return data for {ticker}.")

    if risk_return_data:
        df = pd.DataFrame(risk_return_data)
        fig = px.scatter(
            df,
            x="Risk",
            y="Return",
            size="Weight",
            color="Ticker",
            hover_name="Ticker",
            title="Risk vs. Return Scatter Plot",
            labels={"Risk": "Annualized Risk (Volatility)", "Return": "Annualized Return"},
            color_discrete_sequence=px.colors.sequential.Rainbow,

        )
        
        return fig
    return None
