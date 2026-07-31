import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as gg
import os
import sys

# Add parent directory to path if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crime_analytics import CrimeDataAnalyzer, HotspotDetector, RiskScorer, generate_automated_insights

st.set_page_config(
    page_title="Crime Analytics Dashboard | ML-CaPsule",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), "crime_dataset.csv")
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

df_raw = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.title("🚨 Filter Dashboard")
st.sidebar.markdown("Filter analytics by timeline, district, and crime categories.")

# District Filter
districts = ["All Districts"] + list(df_raw["district"].unique())
selected_district = st.sidebar.selectbox("Select District", districts)

# Crime Type Filter
crime_types = ["All Categories"] + list(df_raw["crime_type"].unique())
selected_crime = st.sidebar.selectbox("Select Crime Category", crime_types)

# Date Range Filter
min_date = df_raw["timestamp"].min().date()
max_date = df_raw["timestamp"].max().date()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Apply Filters
df_filtered = df_raw.copy()
if selected_district != "All Districts":
    df_filtered = df_filtered[df_filtered["district"] == selected_district]
if selected_crime != "All Categories":
    df_filtered = df_filtered[df_filtered["crime_type"] == selected_crime]

if len(date_range) == 2:
    start_d, end_d = date_range
    df_filtered = df_filtered[(df_filtered["timestamp"].dt.date >= start_d) & (df_filtered["timestamp"].dt.date <= end_d)]

# Instantiating Analyzers
analyzer = CrimeDataAnalyzer(df_filtered)
hotspot_engine = HotspotDetector(df_filtered)
risk_engine = RiskScorer(df_filtered)

# Header Section
st.markdown("<div class='main-title'>🚨 Crime Analytics & Hotspot Intelligence Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Advanced spatial-temporal crime trend analysis, risk scoring, and automated insights module.</div>", unsafe_allow_html=True)

# KPI Cards Row
kpis = analyzer.get_summary_kpis()
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("Total Incidents", f"{kpis['total_incidents']:,}")
with c2:
    st.metric("Avg Severity Score", f"{kpis['avg_severity']}/10")
with c3:
    st.metric("Top Crime Category", kpis['top_crime_type'])
with c4:
    st.metric("Avg Response Time", f"{kpis['avg_response_time_min']} mins")
with c5:
    st.metric("Case Solved Rate", f"{kpis['solved_rate_pct']}%")

st.markdown("---")

# Main Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Temporal Trends & Growth",
    "🗺️ Hotspots & GIS Heatmap",
    "📊 Category Distribution",
    "🛡️ Risk Scoring Matrix",
    "🤖 Automated Insights"
])

# --- TAB 1: TEMPORAL TRENDS ---
with tab1:
    st.subheader("Crime Frequency & Trend Analysis")
    freq_choice = st.radio("Resample Trend Frequency:", ["Monthly", "Yearly"], horizontal=True)
    freq_code = "ME" if freq_choice == "Monthly" else "YE"
    
    ts_df = analyzer.get_time_series_trends(freq=freq_code)
    
    fig_ts = px.line(
        ts_df, 
        x="timestamp", 
        y="total_incidents",
        title=f"Crime Volume Trend ({freq_choice})",
        labels={"timestamp": "Timeline", "total_incidents": "Incident Count"},
        markers=True,
        color_discrete_sequence=["#EF4444"]
    )
    fig_ts.update_layout(hovermode="x unified", template="plotly_white")
    st.plotly_chart(fig_ts, use_container_width=True)
    
    st.subheader("Month-over-Month (MoM) & Year-over-Year (YoY) Comparison")
    growth_df = analyzer.get_mom_yoy_comparison()
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig_mom = px.bar(
            growth_df,
            x="year_month",
            y="MoM_Growth_%",
            title="Month-over-Month (MoM) Growth Rate (%)",
            labels={"year_month": "Month", "MoM_Growth_%": "Growth %"},
            color="MoM_Growth_%",
            color_continuous_scale="Reds"
        )
        fig_mom.update_layout(template="plotly_white")
        st.plotly_chart(fig_mom, use_container_width=True)
        
    with col_b:
        fig_yoy = px.bar(
            growth_df.dropna(subset=["YoY_Growth_%"]),
            x="year_month",
            y="YoY_Growth_%",
            title="Year-over-Year (YoY) Comparison (%)",
            labels={"year_month": "Month", "YoY_Growth_%": "YoY Change %"},
            color="YoY_Growth_%",
            color_continuous_scale="Oranges"
        )
        fig_yoy.update_layout(template="plotly_white")
        st.plotly_chart(fig_yoy, use_container_width=True)

# --- TAB 2: GEOSPATIAL HOTSPOTS ---
with tab2:
    st.subheader("Geographical Crime Hotspots & Spatial Distribution")
    
    if not df_filtered.empty:
        fig_map = px.density_mapbox(
            df_filtered,
            lat="latitude",
            lon="longitude",
            z="severity_score",
            radius=15,
            center=dict(lat=df_filtered["latitude"].mean(), lon=df_filtered["longitude"].mean()),
            zoom=10,
            mapbox_style="open-street-map",
            title="Spatial Density Heatmap (Weighted by Severity)"
        )
        fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)
        
        st.subheader("District Crime Volume & Coordinates Breakdown")
        hotspot_df = hotspot_engine.get_district_hotspots()
        st.dataframe(hotspot_df, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

# --- TAB 3: CATEGORY DISTRIBUTION ---
with tab3:
    st.subheader("Crime Category Distribution & Peak Hours")
    cat_df = analyzer.get_category_distribution()
    
    c1, c2 = st.columns(2)
    with c1:
        fig_pie = px.pie(
            cat_df,
            names="crime_type",
            values="count",
            title="Crime Category Proportion",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        fig_sev = px.bar(
            cat_df,
            x="crime_type",
            y="avg_severity",
            title="Average Severity per Crime Type",
            color="avg_severity",
            color_continuous_scale="Purples",
            labels={"crime_type": "Crime Category", "avg_severity": "Avg Severity"}
        )
        fig_sev.update_layout(template="plotly_white")
        st.plotly_chart(fig_sev, use_container_width=True)
        
    st.subheader("Peak Hour vs. Day of Week Crime Heatmap")
    heatmap_data = analyzer.get_hourly_day_heatmap_data()
    fig_heat = px.imshow(
        heatmap_data,
        labels=dict(x="Hour of Day", y="Day of Week", color="Incidents"),
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale="Viridis",
        aspect="auto",
        title="Incident Intensity Matrix (Hour vs Day)"
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# --- TAB 4: RISK SCORING MATRIX ---
with tab4:
    st.subheader("Location Risk Score Assessment")
    st.markdown("Risk scores are dynamically generated based on incident volume, average severity, and 90-day recency weights.")
    
    w_vol = st.slider("Volume Weight", 0.0, 1.0, 0.4, step=0.1)
    w_sev = st.slider("Severity Weight", 0.0, 1.0, 0.3, step=0.1)
    w_rec = st.slider("Recency Weight (Last 90 Days)", 0.0, 1.0, 0.3, step=0.1)
    
    risk_df = risk_engine.calculate_district_risk_scores(
        recency_weight=w_rec, 
        volume_weight=w_vol, 
        severity_weight=w_sev
    )
    
    fig_risk = px.bar(
        risk_df,
        x="district",
        y="risk_score",
        color="risk_level",
        title="District Risk Index (Scale 0-100)",
        color_discrete_map={"Critical": "#DC2626", "High": "#EA580C", "Medium": "#F59E0B", "Low": "#10B981"},
        labels={"district": "District", "risk_score": "Risk Score"}
    )
    fig_risk.update_layout(template="plotly_white")
    st.plotly_chart(fig_risk, use_container_width=True)
    
    st.dataframe(risk_df, use_container_width=True)

# --- TAB 5: AUTOMATED INSIGHTS ---
with tab5:
    st.subheader("Automated Data Observations & Analytical Summary")
    insights = generate_automated_insights(df_filtered)
    
    for idx, insight in enumerate(insights, 1):
        st.info(f"{idx}. {insight}")
        
    st.markdown("### Summary Note")
    st.write(
        "This analytics engine continuously evaluates baseline shifts, geographical density transitions, "
        "and seasonal spike vectors to assist policy makers and law enforcement in proactive resource allocation."
    )
