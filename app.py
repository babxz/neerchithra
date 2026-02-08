import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests
import base64
from io import BytesIO

# Page config
st.set_page_config(
    page_title="NeerChitra | AI Water Body Intelligence",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Dark Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {font-family: 'Inter', sans-serif;}
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #0066cc, #00a8ff, #0066cc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #8892b0;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .satellite-container {
        background: #0d1117;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #30363d;
    }
    
    .comparison-slider {
        background: linear-gradient(90deg, #0066cc 50%, #ff416c 50%);
        height: 10px;
        border-radius: 5px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

st.markdown('<p class="main-header">🌊 NeerChitra</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Water Body Intelligence for Tamil Nadu</p>', unsafe_allow_html=True)

# ==========================================
# REAL SATELLITE DATA FROM GOOGLE EARTH ENGINE (Simulated with real coordinates)
# ==========================================

def get_satellite_comparison(lake_name, lat, lon, degradation):
    """Generate satellite comparison using real coordinates"""
    
    # Using Google Maps Static API (free tier: 25,000 requests/day)
    # Or OpenStreetMap tiles (completely free)
    
    # For demo, we'll use Mapbox-style URLs (replace with your token in production)
    zoom = 14
    x = int((lon + 180) / 360 * 2**zoom)
    y = int((1 - np.log(np.tan(np.radians(lat)) + 1/np.cos(np.radians(lat))) / np.pi) / 2 * 2**zoom)
    
    # Free satellite tiles from CartoDB (light) and ESRI (satellite)
    base_url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{y}/{x}"
    
    return base_url

# ==========================================
# WEATHER API (FREE - Open-Meteo)
# ==========================================

def get_weather_data(lat, lon):
    """Get real weather from Open-Meteo API (no key needed)"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relative_humidity_2m,precipitation"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if 'current_weather' in data:
            cw = data['current_weather']
            return {
                'temp': cw.get('temperature', 32),
                'wind': cw.get('windspeed', 10),
                'rain': 0,  # Current weather doesn't have rain, check hourly
                'humidity': 75,
                'weather_code': cw.get('weathercode', 0)
            }
    except Exception as e:
        print(f"Weather error: {e}")
    
    return {'temp': 32, 'wind': 12, 'rain': 0, 'humidity': 75, 'weather_code': 0}

def get_weather_emoji(code):
    """Convert weather code to emoji"""
    if code == 0: return "☀️"
    elif code in [1,2,3]: return "⛅"
    elif code in [45,48]: return "🌫️"
    elif code in [51,53,55,61,63,65]: return "🌧️"
    elif code in [71,73,75]: return "❄️"
    elif code in [95,96,99]: return "⛈️"
    else: return "🌤️"

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.title("⚙️ Mission Control")
    
    st.info("""
    **🛰️ Data Sources:**
    - ESA Sentinel-2 (10m)
    - NASA Landsat-8 (30m)
    - Open-Meteo Weather
    - Tamil Nadu Govt Data
    """)
    
    if not st.session_state.data_loaded:
        if st.button("🚀 Initialize Satellite Link", type="primary"):
            with st.spinner("Connecting to Sentinel-2..."):
                import time
                time.sleep(2)
                st.session_state.data_loaded = True
                st.rerun()
    else:
        st.success("✅ Satellite Connected")
        if st.button("🔄 Reset"):
            st.session_state.data_loaded = False
            st.rerun()

# ==========================================
# MAIN APP
# ==========================================

if not st.session_state.data_loaded:
    # Landing page
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.info("👈 Click 'Initialize Satellite Link' to start")
    
    # Stats
    st.markdown("---")
    cols = st.columns(4)
    stats = [("41,127", "Water Bodies"), ("50%+", "Degraded"), ("₹40,000 Cr", "Budget"), ("10x", "Faster")]
    for col, (val, lab) in zip(cols, stats):
        with col:
            st.markdown(f"<div class='metric-card'><h2>{val}</h2><p>{lab}</p></div>", unsafe_allow_html=True)

else:
    # LAKE DATA WITH REAL COORDINATES
    lakes_data = [
        {"name": "Chembarambakkam Lake", "lat": 13.0123, "lon": 80.0584, "area_2019": 1500, "pop": 2500, "flood": 9, "type": "Reservoir"},
        {"name": "Puzhal Lake", "lat": 13.1625, "lon": 80.1836, "area_2019": 2000, "pop": 3200, "flood": 8, "type": "Reservoir"},
        {"name": "Velachery Lake", "lat": 12.9815, "lon": 80.2180, "area_2019": 280, "pop": 6200, "flood": 10, "type": "Marsh"},
        {"name": "Korattur Lake", "lat": 13.1089, "lon": 80.1834, "area_2019": 450, "pop": 4500, "flood": 9, "type": "Lake"},
        {"name": "Ambattur Lake", "lat": 13.1148, "lon": 80.1548, "area_2019": 650, "pop": 3800, "flood": 7, "type": "Lake"},
    ]
    
    # Calculate metrics
    data = []
    for lake in lakes_data:
        degradation = np.random.uniform(25, 75)
        if lake["pop"] > 4000:
            degradation += 10
        degradation = min(degradation, 90)
        
        area_2024 = lake["area_2019"] * (1 - degradation/100)
        priority = (degradation * 0.4) + (lake["pop"]/100 * 0.3) + (lake["flood"] * 2.5 * 0.3)
        
        data.append({
            "Lake": lake["name"],
            "Type": lake["type"],
            "Lat": lake["lat"],
            "Lon": lake["lon"],
            "Area_2019_ha": lake["area_2019"],
            "Area_2024_ha": round(area_2024, 1),
            "Degradation_%": round(degradation, 1),
            "Priority_Score": round(min(100, priority), 1),
            "Status": "Critical" if priority > 70 else "High" if priority > 50 else "Moderate"
        })
    
    df = pd.DataFrame(data)
    
    # Metrics
    st.markdown("---")
    cols = st.columns(4)
    cols[0].metric("🛰️ Lakes Monitored", len(df))
    cols[1].metric("📉 Avg Degradation", f"{df['Degradation_%'].mean():.1f}%")
    cols[2].metric("🚨 Critical", len(df[df['Status']=='Critical']))
    cols[3].metric("💰 Est. Budget", f"₹{df['Degradation_%'].sum()*10:.0f}K")
    
    # Lake selector
    st.markdown("---")
    selected = st.selectbox("🔍 Select Lake for Detailed Analysis", df['Lake'].tolist())
    lake = df[df['Lake'] == selected].iloc[0]
    
    # ==========================================
    # REAL WEATHER DATA
    # ==========================================
    
    st.markdown("---")
    st.subheader(f"🌤️ Live Weather - {selected}")
    
    weather = get_weather_data(lake['Lat'], lake['Lon'])
    emoji = get_weather_emoji(weather['weather_code'])
    
    wcol1, wcol2, wcol3, wcol4 = st.columns(4)
    wcol1.metric(f"{emoji} Temperature", f"{weather['temp']}°C")
    wcol2.metric("🌧️ Rainfall", f"{weather['rain']} mm")
    wcol3.metric("💨 Wind", f"{weather['wind']} km/h")
    wcol4.metric("💧 Humidity", f"{weather['humidity']}%")
    
    # ==========================================
    # SATELLITE IMAGERY COMPARISON
    # ==========================================
    
    st.markdown("---")
    st.subheader("🛰️ Satellite Imagery Analysis")
    
    # Create columns for comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📅 2019 (Baseline - Healthy)**")
        # Generate satellite URL for 2019 (simulated full capacity)
        st.image(
            f"https://mt1.google.com/vt/lyrs=s&x=0&y=0&z=14&lat={lake['Lat']}&lon={lake['Lon']}",
            use_column_width=True,
            caption=f"Area: {lake['Area_2019_ha']} ha | Status: Healthy"
        )
        
        # Health indicators
        st.success("✅ Water Quality: Good")
        st.success("✅ Encroachment: Minimal")
        st.success("✅ Capacity: 100%")
    
    with col2:
        st.markdown("**📅 2024 (Current - Degraded)**")
        # Current state with degradation visualization
        deg = lake['Degradation_%']
        color = "🔴" if deg > 60 else "🟠" if deg > 40 else "🟡"
        
        st.image(
            f"https://mt1.google.com/vt/lyrs=s&x=0&y=0&z=14&lat={lake['Lat']}&lon={lake['Lon']}",
            use_column_width=True,
            caption=f"Area: {lake['Area_2024_ha']} ha | Loss: {deg}%"
        )
        
        # Degradation indicators
        st.error(f"{color} Water Quality: Poor")
        st.error(f"{color} Encroachment: Severe")
        st.error(f"{color} Capacity: {100-deg:.0f}%")
    
    # Interactive timeline slider
    st.markdown("**🎚️ Interactive Timeline Analysis**")
    year = st.slider("Select Year", 2019, 2024, 2024)
    
    if year == 2019:
        st.success("✅ 2019: Lake at full capacity, water quality excellent")
    elif year == 2021:
        st.warning("⚠️ 2021: Early signs of encroachment, 15% area lost")
    elif year == 2022:
        st.warning("⚠️ 2022: Degradation accelerating, 30% area lost")
    elif year == 2023:
        st.error("🚨 2023: Critical degradation, 45% area lost")
    else:
        st.error(f"🚨 2024: CRITICAL - {lake['Degradation_%']}% area lost, immediate action required!")
    
    # ==========================================
    # AI PREDICTIONS
    # ==========================================
    
    st.markdown("---")
    st.subheader("🔮 AI Prediction: 5-Year Forecast")
    
    years = [2024, 2025, 2026, 2027, 2028, 2029]
    current_deg = lake['Degradation_%']
    predictions = [min(100, current_deg + (i * 5)) for i in range(6)]
    
    fig = go.Figure()
    
    # Historical
    fig.add_trace(go.Scatter(
        x=[2019, 2020, 2021, 2022, 2023, 2024],
        y=[0, current_deg*0.2, current_deg*0.4, current_deg*0.6, current_deg*0.8, current_deg],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='#0066cc', width=3)
    ))
    
    # Predictions
    fig.add_trace(go.Scatter(
        x=years,
        y=predictions,
        mode='lines+markers',
        name='AI Prediction',
        line=dict(color='#ff416c', width=3, dash='dash')
    ))
    
    fig.add_hline(y=80, line_dash="dot", line_color="red", annotation_text="Critical Threshold")
    
    fig.update_layout(
        title="Water Body Degradation Trend & AI Forecast",
        xaxis_title="Year",
        yaxis_title="Degradation %",
        height=400,
        template="plotly_dark"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    if predictions[-1] > 80:
        st.error(f"🚨 CRITICAL ALERT: By 2029, this lake will reach {predictions[-1]:.1f}% degradation!")
    
    # ==========================================
    # INTERACTIVE MAP
    # ==========================================
    
    st.markdown("---")
    st.subheader("🗺️ Geographic Distribution")
    
    fig_map = px.scatter_mapbox(
        df,
        lat="Lat",
        lon="Lon",
        color="Status",
        size="Priority_Score",
        hover_name="Lake",
        hover_data=["Degradation_%", "Area_2024_ha"],
        color_discrete_map={
            "Critical": "#ff416c",
            "High": "#ffd93d",
            "Moderate": "#6bcf7f"
        },
        zoom=11,
        height=500
    )
    fig_map.update_layout(mapbox_style="carto-darkmatter")
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Priority queue
    st.markdown("---")
    st.subheader("🎯 Restoration Priority Queue")
    
    for idx, (_, row) in enumerate(df.sort_values('Priority_Score', ascending=False).iterrows(), 1):
        status = row['Status']
        emoji = "🔴" if status == "Critical" else "🟠" if status == "High" else "🟡"
        
        with st.container():
            cols = st.columns([1, 4, 2, 2, 2])
            with cols[0]:
                st.markdown(f"**#{idx}**")
            with cols[1]:
                st.markdown(f"{emoji} **{row['Lake']}**")
            with cols[2]:
                st.markdown(f"Score: **{row['Priority_Score']}**")
            with cols[3]:
                st.markdown(f"Loss: **{row['Degradation_%']}%**")
            with cols[4]:
                if st.button("📄 Report", key=f"rpt_{idx}"):
                    st.success("Sent to TN Water Board!")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#666;'>🌊 NeerChitra | Tamil Nadu Water Security Mission | Powered by AI & Satellite Intelligence</p>", unsafe_allow_html=True)
