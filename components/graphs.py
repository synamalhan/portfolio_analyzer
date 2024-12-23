import plotly.graph_objects as go

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
