import pandas as pd
import sqlite3

def load_data(uploaded_file):
    """Load CSV and add date/period columns"""
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    df['Quarter'] = df['Date'].dt.to_period('Q').astype(str)
    return df

def get_kpis(df):
    """Calculate key performance indicators"""
    total_revenue = df['Sales'].sum()
    total_units = df['Units'].sum()
    churn_rate = df['Churn'].mean() * 100
    avg_order = df['Sales'].mean()
    
    # QoQ growth (compare last 2 quarters)
    q_sales = df.groupby('Quarter')['Sales'].sum().reset_index()
    if len(q_sales) >= 2:
        growth = ((q_sales.iloc[-1]['Sales'] - q_sales.iloc[-2]['Sales']) 
                  / q_sales.iloc[-2]['Sales']) * 100
    else:
        growth = 0

    return {
        "Total Revenue": f"${total_revenue:,.0f}",
        "Total Units Sold": f"{total_units:,}",
        "Churn Rate": f"{churn_rate:.1f}%",
        "Avg Order Value": f"${avg_order:,.0f}",
        "QoQ Growth": f"{growth:+.1f}%"
    }

def get_monthly_sales(df):
    """Group sales by month"""
    return df.groupby('Month')['Sales'].sum().reset_index()

def get_regional_sales(df):
    """Group sales by region"""
    return df.groupby('Region')['Sales'].sum().reset_index().sort_values('Sales', ascending=False)

def get_top_products(df):
    """Rank products by performance"""
    return df.groupby('Product').agg(
        Total_Sales=('Sales', 'sum'),
        Units_Sold=('Units', 'sum'),
        Avg_Order=('Sales', 'mean')
    ).reset_index().sort_values('Total_Sales', ascending=False)

def run_sql_query(df, query):
    """Execute SQL query on dataframe"""
    conn = sqlite3.connect(":memory:")
    df.to_sql("sales", conn, index=False, if_exists="replace")
    try:
        result = pd.read_sql_query(query, conn)
        return result, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()