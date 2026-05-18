import plotly.express as px
import plotly.graph_objects as go

COLORS = ["#6C63FF", "#48CAE4", "#FF6B6B", "#52B788"]

def monthly_trend_chart(df):
    """Line chart showing monthly revenue trend"""
    fig = px.line(
        df, x='Month', y='Sales',
        title='Monthly Revenue Trend',
        markers=True,
        color_discrete_sequence=[COLORS[0]]
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        xaxis_title="Month", 
        yaxis_title="Revenue ($)",
        hovermode='x unified',
        margin=dict(l=0, r=0, t=40, b=0)
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    return fig

def regional_bar_chart(df):
    """Bar chart comparing sales by region"""
    fig = px.bar(
        df, x='Region', y='Sales',
        title='Sales by Region',
        color='Region',
        color_discrete_sequence=COLORS,
        text='Sales'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(size=12),
        xaxis_title="Region",
        yaxis_title="Sales ($)",
        margin=dict(l=0, r=0, t=40, b=0)
    )
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    return fig

def product_pie_chart(df):
    """Donut chart showing product revenue share"""
    fig = px.pie(
        df, names='Product', values='Total_Sales',
        title='Revenue Share by Product',
        color_discrete_sequence=COLORS,
        hole=0.4
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig