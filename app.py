import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    try:
        return pd.read_csv("blinkit_lastmile_data.csv")
    except Exception as e:
        st.warning("Using fallback demo dataset (CSV not found)")

        data = {
            "city": ["Bangalore"]*8,
            "cluster": ["East","East","East","East","South","South","South","South"],
            "store": ["Whitefield","Whitefield","Marathahalli","Marathahalli","HSR","HSR","BTM","BTM"],
            "category": ["Grocery","Dairy","Grocery","Pharma","Grocery","Dairy","Pharma","Grocery"],
            "orders": [120,80,150,60,200,90,70,130],
            "delivery_time": [18,15,20,22,17,16,21,19],
            "breach": [0.1,0.08,0.15,0.2,0.07,0.09,0.18,0.11],
            "rider_cost": [3000,1800,4000,2000,5000,2200,2100,3200]
        }

        return pd.DataFrame(data)

# ---- SIDEBAR ----
st.sidebar.title("Ops Control Panel")

city = st.sidebar.selectbox("City", df["city"].unique())
cluster = st.sidebar.selectbox("Cluster", df[df.city == city]["cluster"].unique())
store = st.sidebar.selectbox("Store", df[df.cluster == cluster]["store"].unique())

# ---- FILTER ----
filtered = df[
    (df.city == city) &
    (df.cluster == cluster) &
    (df.store == store)
]

# ---- KPIs ----
total_orders = filtered["orders"].sum()
avg_time = filtered["delivery_time"].mean()
breach = filtered["breach"].mean()
cost_per_order = filtered["rider_cost"].sum() / max(total_orders,1)

st.title("⚡ Blinkit Last Mile Ops Intelligence")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Orders", int(total_orders))
c2.metric("Avg Delivery Time", round(avg_time,1))
c3.metric("Breach %", round(breach*100,1))
c4.metric("Cost / Order (₹)", round(cost_per_order,1))

# ---- TABS ----
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Store Intelligence",
    "Rider Efficiency",
    "Rate Card Optimizer",
    "Action Engine"
])

# ---- TAB 1 ----
with tab1:
    st.subheader("Demand vs Breach")
    fig = px.scatter(filtered, x="orders", y="breach", size="orders", color="category")
    st.plotly_chart(fig, use_container_width=True)

# ---- TAB 2 ----
with tab2:
    st.subheader("Store Comparison")

    store_df = df[df.cluster == cluster].groupby("store").agg({
        "orders":"sum",
        "breach":"mean",
        "rider_cost":"sum"
    }).reset_index()

    store_df["cost_per_order"] = store_df["rider_cost"] / store_df["orders"]

    fig2 = px.bar(store_df, x="store", y="cost_per_order", color="breach")
    st.plotly_chart(fig2, use_container_width=True)

# ---- TAB 3 ----
with tab3:
    st.subheader("Rider Efficiency Score")

    filtered["efficiency_score"] = (
        (1 - filtered["breach"]) * 0.5 +
        (1 / filtered["delivery_time"]) * 0.5
    )

    fig3 = px.scatter(
        filtered,
        x="delivery_time",
        y="efficiency_score",
        size="orders",
        color="breach"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ---- TAB 4 ----
with tab4:
    st.subheader("Rate Card Simulator")

    orders_day = st.slider("Orders / Rider / Day", 10, 100, 40)
    payout_per_order = st.slider("Base Pay / Order (₹)", 10, 50, 25)
    incentive = st.slider("Incentive Bonus (₹)", 0, 500, 100)

    earnings = orders_day * payout_per_order + incentive

    st.metric("Estimated Rider Earnings (₹/day)", earnings)

    st.write("👉 Use this to balance cost vs retention")

# ---- TAB 5 ----
with tab5:
    st.subheader("⚠️ Action Recommendations")

    if breach > 0.12:
        st.error("High breach → Add riders OR reduce batching")

    if cost_per_order > 40:
        st.warning("High cost → Optimize rate card or increase utilization")

    if avg_time > 20:
        st.info("Slow deliveries → Investigate routing / rider idle time")

    st.success("✔ Suggested Actions Generated")
