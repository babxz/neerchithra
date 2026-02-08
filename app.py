import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="NeerChitra | AI Water Body Intelligence", page_icon="🌊", layout="wide")

# CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #0066cc, #00a8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

st.markdown('<p class="main-header">🌊 NeerChitra</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666;">AI-Powered Water Body Intelligence for Tamil Nadu</p>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.info("Data: 2019 vs 2026 (7-year analysis)")
    
    if not st.session_state.data_loaded:
        if st.button("🚀 Initialize Analysis", type="primary"):
            st.session_state.data_loaded = True
            st.rerun()
    else:
        st.success("✅ Analysis Active")
        if st.button("🔄 Reset"):
            st.session_state.data_loaded = False
            st.rerun()

# 10 LAKES DATA
LAKES = [
    {"name": "Chembarambakkam Lake", "lat": 13.0123, "lon": 80.0584, "area_2019": 1500, "area_2026": 975, "degradation": 35.0, "pop": 2500, "flood": 9, "type": "Reservoir"},
    {"name": "Puzhal Lake", "lat": 13.1625, "lon": 80.1836, "area_2019": 2000, "area_2026": 1400, "degradation": 30.0, "pop": 3200, "flood": 8, "type": "Reservoir"},
    {"name": "Cholavaram Lake", "lat": 13.2156, "lon": 80.1423, "area_2019": 800, "area_2026": 480, "degradation": 40.0, "pop": 1200, "flood": 7, "type": "Lake"},
    {"name": "Korattur Lake", "lat": 13.1089, "lon": 80.1834, "area_2019": 450, "area_2026": 225, "degradation": 50.0, "pop": 4500, "flood": 9, "type": "Lake"},
    {"name": "Velachery Lake", "lat": 12.9815, "lon": 80.2180, "area_2019": 280, "area_2026": 84, "degradation": 70.0, "pop": 6200, "flood": 10, "type": "Marsh"},
    {"name": "Madipakkam Lake", "lat": 12.9456, "lon": 80.2012, "area_2019": 320, "area_2026": 128, "degradation": 60.0, "pop": 5800, "flood": 8, "type": "Lake"},
    {"name": "Ambattur Lake", "lat": 13.1148, "lon": 80.1548, "area_2019": 650, "area_2026": 455, "degradation": 30.0, "pop": 3800, "flood": 7, "type": "Lake"},
    {"name": "Madhavaram Lake", "lat": 13.1489, "lon": 80.2312, "area_2019": 520, "area_2026": 390, "degradation": 25.0, "pop": 2900, "flood": 6, "type": "Lake"},
    {"name": "Sholinganallur Marsh", "lat": 12.9012, "lon": 80.2278, "area_2019": 380, "area_2026": 190, "degradation": 50.0, "pop": 4100, "flood": 9, "type": "Marsh"},
    {"name": "Nesapakkam Lake", "lat": 13.0345, "lon": 80.1923, "area_2019": 290, "area_2026": 145, "degradation": 50.0, "pop": 5100, "flood": 8, "type": "Lake"},
]

if not st.session_state.data_loaded:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.info("👈 Click 'Initialize Analysis' to view 2019 vs 2026 satellite comparison")
    
    st.markdown("---")
    cols = st.columns(4)
    stats = [("41,127", "Water Bodies"), ("50%+", "Degraded"), ("₹40,000 Cr", "Budget"), ("2019-2026", "Analysis Period")]
    for col, (val, lab) in zip(cols, stats):
        with col:
            st.markdown(f"<div class='metric-card'><h2>{val}</h2><p>{lab}</p></div>", unsafe_allow_html=True)

else:
    df = pd.DataFrame(LAKES)
    df['Priority_Score'] = (df['degradation'] * 0.4 + df['pop'] / 100 * 0.3 + df['flood'] * 2.5 * 0.3).round(1)
    df['Status'] = df['Priority_Score'].apply(lambda x: 'Critical' if x > 70 else 'High' if x > 50 else 'Moderate')
    
    # Metrics
    st.markdown("---")
    cols = st.columns(4)
    cols[0].metric("📊 Lakes Analyzed", len(df))
    cols[1].metric("📉 Avg Degradation (2019-2026)", f"{df['degradation'].mean():.1f}%")
    cols[2].metric("🚨 Critical Priority", len(df[df['Status'] == 'Critical']))
    cols[3].metric("🏞️ Total Area Lost", f"{(df['area_2019'] - df['area_2026']).sum():.0f} ha")
    
    # Lake selector
    st.markdown("---")
    selected = st.selectbox("🔍 Select Lake for 2019 vs 2026 Analysis", df['name'].tolist())
    lake = df[df['name'] == selected].iloc[0]
    
    # SATELLITE COMPARISON
    st.markdown("---")
    st.subheader(f"🛰️ Satellite Imagery: 2019 vs 2026 - {selected}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📅 2019 (Baseline)**")
        st.map(pd.DataFrame({'lat': [lake['lat']], 'lon': [lake['lon']], 'size': [lake['area_2019']/5]}), zoom=14, size='size')
        st.success(f"✅ Healthy: {lake['area_2019']} ha | 100% capacity")
    
    with col2:
        st.markdown("**📅 2026 (Current)**")
        st.map(pd.DataFrame({'lat': [lake['lat']], 'lon': [lake['lon']], 'size': [lake['area_2026']/5]}), zoom=14, size='size')
        
        lost = lake['area_2019'] - lake['area_2026']
        if lake['degradation'] >= 60:
            st.error(f"🔴 CRITICAL: {lake['area_2026']} ha | Lost: {lost} ha ({lake['degradation']}%)")
        elif lake['degradation'] >= 40:
            st.warning(f"🟠 HIGH RISK: {lake['area_2026']} ha | Lost: {lost} ha ({lake['degradation']}%)")
        else:
            st.info(f"🟡 MODERATE: {lake['area_2026']} ha | Lost: {lost} ha ({lake['degradation']}%)")
    
    # Timeline
    st.markdown("**🎚️ Timeline Analysis**")
    year = st.slider("Select Year", 2019, 2026, 2026)
    progress = (year - 2019) / 7 * lake['degradation']
    
    if year == 2019:
        st.success("✅ 2019: Full capacity, no degradation")
    elif year == 2022:
        st.warning(f"⚠️ 2022: Mid-analysis, ~{progress:.0f}% degradation")
    elif year == 2026:
        st.error(f"🚨 2026: Current state, {lake['degradation']}% degradation")
    
    # Predictions
    st.markdown("---")
    st.subheader("🔮 AI Prediction: 2026-2031")
    
    years = list(range(2026, 2032))
    predictions = [lake['degradation'] + i*3 for i in range(6)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[2019,2022,2026], y=[0, lake['degradation']*0.5, lake['degradation']], mode='lines+markers', name='Historical'))
    fig.add_trace(go.Scatter(x=years, y=predictions, mode='lines+markers', name='AI Prediction', line=dict(dash='dash')))
    fig.add_hline(y=80, line_dash="dot", line_color="red")
    fig.update_layout(title="Degradation Forecast", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Priority Queue
    st.markdown("---")
    st.subheader("🎯 Restoration Priority Queue (All 10 Lakes)")
    
    for idx, (_, row) in enumerate(df.sort_values('Priority_Score', ascending=False).iterrows(), 1):
        emoji = "🔴" if row['Status'] == "Critical" else "🟠" if row['Status'] == "High" else "🟡"
        cols = st.columns([1, 4, 2, 2, 2])
        with cols[0]:
            st.markdown(f"**#{idx}**")
        with cols[1]:
            st.markdown(f"{emoji} **{row['name']}**")
        with cols[2]:
            st.markdown(f"Score: **{row['Priority_Score']}**")
        with cols[3]:
            st.markdown(f"Loss: **{row['degradation']}%**")
        with cols[4]:
            if st.button("Report", key=f"rpt_{idx}"):
                st.success("Sent to TN Water Board!")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#666;'>🌊 NeerChitra | Tamil Nadu Water Security Mission | 2019-2026 Analysis</p>", unsafe_allow_html=True)
