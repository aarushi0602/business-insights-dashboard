import streamlit as st
import pandas as pd
from data_processor import load_data, get_kpis, get_monthly_sales, get_regional_sales, get_top_products, run_sql_query
from charts import monthly_trend_chart, regional_bar_chart, product_pie_chart
from ai_insights import generate_insights

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Insights Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 AI-Powered Sales Insights Dashboard")
st.caption("Upload your sales CSV to get instant KPIs, charts, and AI-generated insights.")

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    uploaded_file = st.file_uploader("Upload Sales CSV", type=["csv"])
    use_sample = st.checkbox("Use sample data", value=True)
    st.divider()
    st.markdown("**Required CSV columns:**")
    st.code("Date, Region, Product,\nSales, Units, CustomerID, Churn")
    
    st.divider()
    st.markdown("**About**")
    st.markdown("""
    This dashboard provides:
    - Real-time KPI metrics
    - Interactive visualizations
    - SQL data exploration
    - AI-powered insights
    """)

# ── Load data ─────────────────────────────────────────────────
df = None
if uploaded_file:
    try:
        df = load_data(uploaded_file)
        st.sidebar.success(f"✅ Loaded {len(df):,} rows")
    except Exception as e:
        st.sidebar.error(f"Error loading file: {str(e)}")
elif use_sample:
    try:
        df = load_data("sample_data.csv")
        st.sidebar.info("✅ Using sample data")
    except FileNotFoundError:
        st.sidebar.error("❌ sample_data.csv not found")

if df is None:
    st.info("👈 Upload a CSV or check 'Use sample data' to get started.")
    st.stop()

# ── KPI Cards ─────────────────────────────────────────────────
st.subheader("📈 Key Performance Indicators")
kpis = get_kpis(df)
cols = st.columns(5)

kpi_items = list(kpis.items())
for col, (label, value) in zip(cols, kpi_items):
    col.metric(label, value)

st.divider()

# ── Charts ────────────────────────────────────────────────────
st.subheader("📊 Sales Analytics")
col1, col2 = st.columns(2)

with col1:
    monthly = get_monthly_sales(df)
    st.plotly_chart(monthly_trend_chart(monthly), use_container_width=True)

with col2:
    regional = get_regional_sales(df)
    st.plotly_chart(regional_bar_chart(regional), use_container_width=True)

st.divider()

# ── Product breakdown ─────────────────────────────────────────
st.subheader("🏆 Product Performance")
col3, col4 = st.columns([1, 1])
products = get_top_products(df)

with col3:
    st.plotly_chart(product_pie_chart(products), use_container_width=True)

with col4:
    st.markdown("**Top Products Table**")
    display_df = products.copy()
    display_df['Total_Sales'] = display_df['Total_Sales'].apply(lambda x: f"${x:,.0f}")
    display_df['Avg_Order'] = display_df['Avg_Order'].apply(lambda x: f"${x:,.0f}")
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ── AI Insights ───────────────────────────────────────────────
st.subheader("🤖 AI-Generated Business Insights")
if st.button("Generate Insights", type="primary", use_container_width=True):
    with st.spinner("🔍 Analyzing your data..."):
        insights = generate_insights(kpis, regional, products)
        st.markdown(insights)

st.divider()

# ── SQL Explorer ──────────────────────────────────────────────
st.subheader("🔍 SQL Explorer")
st.caption("Query the `sales` table directly")

example_queries = {
    "Top regions by revenue": "SELECT Region, SUM(Sales) as Total_Revenue, COUNT(*) as Transactions FROM sales GROUP BY Region ORDER BY Total_Revenue DESC",
    "Monthly churn analysis": "SELECT Month, COUNT(*) as Total_Customers, SUM(Churn) as Churned, ROUND(AVG(Churn)*100, 2) as Churn_Rate FROM sales GROUP BY Month ORDER BY Month",
    "Product performance by region": "SELECT Region, Product, SUM(Sales) as Revenue, SUM(Units) as Units FROM sales GROUP BY Region, Product ORDER BY Region, Revenue DESC",
    "High-value customers": "SELECT CustomerID, SUM(Sales) as Total_Sales, COUNT(*) as Purchases, AVG(Sales) as Avg_Purchase FROM sales GROUP BY CustomerID HAVING SUM(Sales) > 100000 ORDER BY Total_Sales DESC",
}

selected = st.selectbox("📋 Example queries", ["Custom..."] + list(example_queries.keys()))

if selected == "Custom...":
    default_query = "SELECT * FROM sales LIMIT 10"
else:
    default_query = example_queries[selected]

query = st.text_area("SQL Query", value=default_query, height=100)

if st.button("▶️ Run Query", use_container_width=True):
    result, error = run_sql_query(df, query)
    if error:
        st.error(f"❌ SQL Error: {error}")
    else:
        st.success(f"✅ {len(result)} rows returned")
        st.dataframe(result, use_container_width=True, hide_index=True)

st.divider()

# ── Footer ────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("📊 Built with Streamlit")
with col2:
    st.caption("🔧 Powered by Pandas & Plotly")
with col3:
    st.caption("🤖 AI by Anthropic & Google")