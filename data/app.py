import streamlit as st
import pandas as pd
from data_processor import load_data, get_kpis, get_monthly_sales, get_regional_sales, get_top_products, run_sql_query
from charts import monthly_trend_chart, regional_bar_chart, product_pie_chart
from ai_insights import generate_insights

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

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

# ── Load data ─────────────────────────────────────────────────
df = None
if uploaded_file:
    df = load_data(uploaded_file)
    st.sidebar.success(f"✅ Loaded {len(df):,} rows")
elif use_sample:
    try:
        df = load_data("sample_data.csv")
        st.sidebar.info("Using sample data")
    except FileNotFoundError:
        st.sidebar.error("sample_data.csv not found")

if df is None:
    st.info("👈 Upload a CSV or check 'Use sample data' to get started.")
    st.stop()

# ── KPI Cards ─────────────────────────────────────────────────
st.subheader("Key Performance Indicators")
kpis = get_kpis(df)
cols = st.columns(5)
for col, (label, value) in zip(cols, kpis.items()):
    col.metric(label, value)

st.divider()

# ── Charts ────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    monthly = get_monthly_sales(df)
    st.plotly_chart(monthly_trend_chart(monthly), use_container_width=True)

with col2:
    regional = get_regional_sales(df)
    st.plotly_chart(regional_bar_chart(regional), use_container_width=True)

# Product breakdown
col3, col4 = st.columns([1, 1])
products = get_top_products(df)

with col3:
    st.plotly_chart(product_pie_chart(products), use_container_width=True)

with col4:
    st.subheader("Top Products Table")
    st.dataframe(
        products.style.format({
            "Total_Sales": "${:,.0f}",
            "Avg_Order": "${:,.0f}"
        }),
        use_container_width=True
    )

st.divider()

# ── AI Insights ───────────────────────────────────────────────
st.subheader("🤖 AI-Generated Business Insights")
if st.button("Generate Insights", type="primary"):
    with st.spinner("Analyzing your data..."):
        try:
            insights = generate_insights(kpis, regional, products)
            st.markdown(insights)
        except Exception as e:
            st.warning(f"Error: {e}")
            st.markdown("""
            **Sample insight format:**
            - **North region** leads with highest revenue, contributing 32% of total sales
            - **Laptop** is the top product with $635K revenue, 3× tablet performance  
            - Customer churn concentrated in Q2 — recommend retention campaign for South region
            """)

st.divider()

# ── SQL Explorer ──────────────────────────────────────────────
st.subheader("🔍 SQL Explorer")
st.caption("Query the `sales` table directly")

example_queries = {
    "Top regions by revenue": "SELECT Region, SUM(Sales) as Revenue FROM sales GROUP BY Region ORDER BY Revenue DESC",
    "Monthly churn rate": "SELECT Month, AVG(Churn)*100 as ChurnPct FROM sales GROUP BY Month",
    "Best product per region": "SELECT Region, Product, SUM(Sales) as Sales FROM sales GROUP BY Region, Product ORDER BY Region, Sales DESC",
}

selected = st.selectbox("Example queries", ["Custom..."] + list(example_queries.keys()))
default_query = example_queries.get(selected, "SELECT * FROM sales LIMIT 10")

query = st.text_area("SQL Query", value=default_query, height=80)

if st.button("Run Query"):
    result, error = run_sql_query(df, query)
    if error:
        st.error(f"SQL Error: {error}")
    else:
        st.dataframe(result, use_container_width=True)
        st.caption(f"{len(result)} rows returned")

# ── Footer ────────────────────────────────────────────────────
st.divider()
st.caption("AI-Powered Sales Dashboard · Built with Streamlit, Pandas, Plotly, Anthropic API")