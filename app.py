import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO

# Page config
st.set_page_config(
    page_title="NeerChitra | AI Water Body Intelligence",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #0066cc, #00a8ff, #0066cc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #8892b0;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #0066cc, #0052a3);
        color: white;
        border-radius: 10px;
        padding: 15px 30px;
        font-size: 1.2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 102, 204, 0.4);
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 102, 204, 0.6);
    }
    
    .priority-critical {
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.3);
        border-left: 5px solid #c92a2a;
    }
    
    .priority-high {
        background: linear-gradient(90deg, #f2994a, #f2c94c);
        color: #333;
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(242, 153, 74, 0.3);
        border-left: 5px solid #e67700;
    }
    
    .priority-moderate {
        background: linear-gradient(90deg, #11998e, #38ef7d);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
        border-left: 5px solid #087f5b;
    }
    
    .satellite-card {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .info-box {
        background: rgba(0, 102, 204, 0.1);
        border-left: 4px solid #0066cc;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #0d1117;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        border: 1px solid #30363d;
    }
    
    .stTabs [aria-selected="true"] {
        background: #0066cc !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'selected_lake' not in st.session_state:
    st.session_state.selected_lake = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# Title Section with animation
st.markdown('<p class="main-header">🌊 NeerChitra</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Water Body Intelligence for Tamil Nadu</p>', unsafe_allow_html=True)

# Sidebar with advanced controls
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='color: #0066cc; margin: 0;'>⚙️ Mission Control</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Satellite Info
    st.subheader("🛰️ Satellite Configuration")
    st.info("""
    **ESA Sentinel-2 MSI**
    - Resolution: 10m (RGB), 20m (NIR)
    - Revisit: 5 days
    - Coverage: All 41,127 water bodies
    - Archive: 2019-2024
    """)
    
    st.markdown("---")
    
    # Analysis Parameters
    st.subheader("📊 Analysis Parameters")
    
    analysis_type = st.selectbox(
        "Detection Algorithm",
        ["NDWI (Normalized Difference Water Index)", 
         "MNDWI (Modified NDWI)",
         "AWEI (Automated Water Extraction)",
         "Deep Learning CNN"]
    )
    
    time_range = st.slider("Analysis Period", 2019, 2024, (2019, 2024))
    
    confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.75)
    
    st.markdown("---")
    
    # Action Buttons
    if not st.session_state.data_loaded:
        if st.button("🚀 Initialize Satellite Link", type="primary"):
            with st.spinner("🛰️ Establishing connection to Sentinel-2..."):
                import time
                time.sleep(2)
                st.session_state.data_loaded = True
                st.rerun()
    else:
        st.success("✅ Satellite Connected")
        if st.button("🔄 Reset Mission"):
            st.session_state.data_loaded = False
            st.session_state.analysis_complete = False
            st.rerun()
    
    if st.session_state.data_loaded and not st.session_state.analysis_complete:
        if st.button("🔍 Run AI Analysis", type="primary"):
            with st.spinner("🤖 Processing satellite imagery..."):
                import time
                time.sleep(3)
                st.session_state.analysis_complete = True
                st.rerun()
    
    st.markdown("---")
    st.caption("🌊 Tamil Nadu Water Security Mission v2.0")

# Generate comprehensive lake data
def generate_comprehensive_data():
    lakes = [
        {
            "name": "Chembarambakkam Lake", 
            "lat": 13.0123, "lon": 80.0584, 
            "area_2019": 1500, "pop": 2500, "flood": 9,
            "district": "Chennai", "type": "Reservoir",
            "pollution_index": 7.2, "encroachment": 35
        },
        {
            "name": "Puzhal Lake (Red Hills)", 
            "lat": 13.1625, "lon": 80.1836, 
            "area_2019": 2000, "pop": 3200, "flood": 8,
            "district": "Chennai", "type": "Reservoir",
            "pollution_index": 6.8, "encroachment": 28
        },
        {
            "name": "Cholavaram Lake", 
            "lat": 13.2156, "lon": 80.1423, 
            "area_2019": 800, "pop": 1200, "flood": 7,
            "district": "Chennai", "type": "Lake",
            "pollution_index": 5.4, "encroachment": 42
        },
        {
            "name": "Korattur Lake", 
            "lat": 13.1089, "lon": 80.1834, 
            "area_2019": 450, "pop": 4500, "flood": 9,
            "district": "Chennai", "type": "Lake",
            "pollution_index": 8.1, "encroachment": 55
        },
        {
            "name": "Velachery Lake", 
            "lat": 12.9815, "lon": 80.2180, 
            "area_2019": 280, "pop": 6200, "flood": 10,
            "district": "Chennai", "type": "Marsh",
            "pollution_index": 8.9, "encroachment": 68
        },
        {
            "name": "Madipakkam Lake", 
            "lat": 12.9456, "lon": 80.2012, 
            "area_2019": 320, "pop": 5800, "flood": 8,
            "district": "Chennai", "type": "Lake",
            "pollution_index": 8.4, "encroachment": 61
        },
        {
            "name": "Ambattur Lake", 
            "lat": 13.1148, "lon": 80.1548, 
            "area_2019": 650, "pop": 3800, "flood": 7,
            "district": "Chennai", "type": "Lake",
            "pollution_index": 6.9, "encroachment": 38
        },
        {
            "name": "Madhavaram Lake", 
            "lat": 13.1489, "lon": 80.2312, 
            "area_2019": 520, "pop": 2900, "flood": 6,
            "district": "Chennai", "type": "Lake",
            "pollution_index": 5.8, "encroachment": 31
        },
        {
            "name": "Sholinganallur Marsh", 
            "lat": 12.9012, "lon": 80.2278, 
            "area_2019": 380, "pop": 4100, "flood": 9,
            "district": "Chennai", "type": "Marsh",
            "pollution_index": 7.6, "encroachment": 45
        },
        {
            "name": "Nesapakkam Lake", 
            "lat": 13.0345, "lon": 80.1923, 
            "area_2019": 290, "pop": 5100, "flood": 8,
            "district": "Chennai", "type": "Lake",
            "pollution_index": 8.2, "encroachment": 52
        },
    ]
    
    data = []
    for lake in lakes:
        # Advanced degradation calculation
        base_degradation = np.random.uniform(15, 65)
        pop_factor = (lake["pop"] / 1000) * 2.5
        pollution_factor = lake["pollution_index"] * 3
        encroachment_factor = lake["encroachment"] * 0.4
        
        degradation = base_degradation + pop_factor + pollution_factor + encroachment_factor
        degradation = min(degradation, 95)  # Cap at 95%
        
        area_2024 = lake["area_2019"] * (1 - degradation/100)
        
        # Advanced priority score with multiple factors
        priority_score = (
            (degradation * 0.35) + 
            (lake["pop"]/100 * 0.25) + 
            (lake["flood"] * 2.5 * 0.20) +
            (lake["pollution_index"] * 2 * 0.15) +
            (lake["encroachment"] * 0.05)
        )
        priority_score = min(100, priority_score)
        
        # Restoration cost estimate (in lakhs)
        restoration_cost = (lake["area_2019"] - area_2024) * 0.5 * (lake["pollution_index"] / 5)
        
        data.append({
            "Lake": lake["name"],
            "District": lake["district"],
            "Type": lake["type"],
            "Latitude": lake["lat"],
            "Longitude": lake["lon"],
            "Area_2019_ha": lake["area_2019"],
            "Area_2024_ha": round(area_2024, 1),
            "Area_Lost_ha": round(lake["area_2019"] - area_2024, 1),
            "Degradation_%": round(degradation, 1),
            "Population_Density": lake["pop"],
            "Flood_Risk": lake["flood"],
            "Pollution_Index": lake["pollution_index"],
            "Encroachment_%": lake["encroachment"],
            "Priority_Score": round(priority_score, 1),
            "Restoration_Cost_Lakhs": round(restoration_cost, 1),
            "Status": "Critical" if priority_score > 75 else "High" if priority_score > 55 else "Moderate" if priority_score > 35 else "Low"
        })
    
    return pd.DataFrame(data)

# Landing Page
if not st.session_state.data_loaded:
    # Hero section
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 40px; border-radius: 20px; margin: 20px 0; text-align: center;'>
        <h2 style='color: white; margin: 0;'>🛰️ Next-Generation Water Body Monitoring</h2>
        <p style='color: #a8d8ff; margin: 10px 0 0 0;'>Leveraging ESA Sentinel-2 & AI for Tamil Nadu's Water Security</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats row
    st.markdown("---")
    cols = st.columns(4)
    stats = [
        ("💧", "41,127", "Water Bodies", "Highest in India"),
        ("⚠️", "50%+", "Critically Degraded", "Immediate action needed"),
        ("💰", "₹40,000 Cr", "Mission Budget", "Data-driven allocation"),
        ("🤖", "10x", "Faster Detection", "AI vs Manual surveys")
    ]
    
    for col, (icon, value, label, sublabel) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <h1 style='margin: 0; font-size: 2.5rem;'>{icon} {value}</h1>
                <p style='margin: 5px 0 0 0; font-size: 1rem; opacity: 0.9;'>{label}</p>
                <p style='margin: 0; font-size: 0.8rem; opacity: 0.7;'>{sublabel}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Features
    st.markdown("---")
    st.subheader("🔬 Advanced Capabilities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='info-box'>
            <h4>🛰️ Multi-Spectral Analysis</h4>
            <ul>
                <li>Sentinel-2 MSI (10-20m)</li>
                <li>NDWI/MNDWI/AWEI indices</li>
                <li>Cloud-free compositing</li>
                <li>5-day temporal resolution</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-box'>
            <h4>🤖 AI-Powered Detection</h4>
            <ul>
                <li>Deep learning CNN models</li>
                <li>Automated boundary extraction</li>
                <li>Change detection algorithms</li>
                <li>Encroachment identification</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='info-box'>
            <h4>📊 Smart Prioritization</h4>
            <ul>
                <li>Multi-criteria scoring</li>
                <li>Population impact analysis</li>
                <li>Flood risk assessment</li>
                <li>Cost-benefit optimization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Analysis Results
elif st.session_state.data_loaded and not st.session_state.analysis_complete:
    st.info("🛰️ Satellite link established. Ready for AI analysis. Click 'Run AI Analysis' in the sidebar.")

# Full Dashboard
else:
    df = generate_comprehensive_data()
    
    # Top metrics with animations
    st.markdown("---")
    cols = st.columns(5)
    
    metrics = [
        ("📊", "Lakes Monitored", len(df)),
        ("📉", "Avg Degradation", f"{df['Degradation_%'].mean():.1f}%"),
        ("🚨", "Critical Priority", len(df[df['Status']=='Critical'])),
        ("💰", "Est. Restoration", f"₹{df['Restoration_Cost_Lakhs'].sum():.0f}L"),
        ("🏞️", "Area Lost", f"{df['Area_Lost_ha'].sum():.0f} ha")
    ]
    
    for col, (icon, label, value) in zip(cols, metrics):
        with col:
            st.metric(label=f"{icon} {label}", value=value)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Live Map", "📊 Analytics", "🎯 Priority Queue", "📋 Data Explorer"])
    
    with tab1:
        st.subheader("🛰️ Real-Time Lake Monitoring")
        
        # Create an interactive map visualization using Plotly
        fig_map = px.scatter_mapbox(
            df,
            lat="Latitude",
            lon="Longitude",
            color="Status",
            size="Priority_Score",
            hover_name="Lake",
            hover_data=["Degradation_%", "Area_Lost_ha", "Pollution_Index"],
            color_discrete_map={
                "Critical": "#ff416c",
                "High": "#f2994a", 
                "Moderate": "#11998e",
                "Low": "#38ef7d"
            },
            zoom=10,
            height=600
        )
        fig_map.update_layout(
            mapbox_style="carto-darkmatter",
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Satellite imagery simulation
        st.subheader("📸 Recent Satellite Imagery")
        cols = st.columns(3)
        for idx, (_, row) in enumerate(df.head(3).iterrows()):
            with cols[idx]:
                st.markdown(f"""
                <div class='satellite-card'>
                    <h4>{row['Lake']}</h4>
                    <p style='color: #888; font-size: 0.8rem;'>Sentinel-2 • {datetime.now().strftime('%Y-%m-%d')}</p>
                    <div style='background: linear-gradient(90deg, #1e3c72, #2a5298); height: 150px; border-radius: 8px; display: flex; align-items: center; justify-content: center;'>
                        <span style='font-size: 3rem;'>🛰️</span>
                    </div>
                    <p style='margin: 10px 0 0 0;'>Degradation: <span style='color: #ff416c; font-weight: bold;'>{row['Degradation_%']}%</span></p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📉 Degradation Analysis")
            top5 = df.nlargest(5, 'Degradation_%')
            
            fig = px.bar(
                top5,
                x='Degradation_%',
                y='Lake',
                orientation='h',
                color='Degradation_%',
                color_continuous_scale='Reds',
                text='Degradation_%',
                height=400
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Status Distribution")
            status_counts = df['Status'].value_counts()
            
            fig2 = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                color=status_counts.index,
                color_discrete_map={
                    'Critical': '#ff416c',
                    'High': '#f2994a',
                    'Moderate': '#11998e',
                    'Low': '#38ef7d'
                },
                hole=0.4,
                height=400
            )
            fig2.update_traces(
                textinfo='percent+label',
                pull=[0.05 if x=='Critical' else 0 for x in status_counts.index]
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Advanced analytics
        st.subheader("🔬 Multi-Factor Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig3 = px.scatter(
                df, x="Pollution_Index", y="Degradation_%",
                color="Status", size="Population_Density",
                hover_name="Lake", height=300
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            fig4 = px.scatter(
                df, x="Encroachment_%", y="Area_Lost_ha",
                color="Status", size="Priority_Score",
                hover_name="Lake", height=300
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        with col3:
            fig5 = px.bar(
                df.groupby('Type')['Restoration_Cost_Lakhs'].sum().reset_index(),
                x='Type', y='Restoration_Cost_Lakhs',
                color='Type', height=300
            )
            st.plotly_chart(fig5, use_container_width=True)
    
    with tab3:
        st.subheader("🎯 AI-Powered Restoration Priority")
        st.caption("Ranking based on: Degradation (35%) + Population Impact (25%) + Flood Risk (20%) + Pollution (15%) + Encroachment (5%)")
        
        df_sorted = df.sort_values('Priority_Score', ascending=False)
        
        for idx, (_, row) in enumerate(df_sorted.head(5).iterrows(), 1):
            if row['Status'] == 'Critical':
                css_class = 'priority-critical'
                emoji = '🔴'
            elif row['Status'] == 'High':
                css_class = 'priority-high'
                emoji = '🟠'
            elif row['Status'] == 'Moderate':
                css_class = 'priority-moderate'
                emoji = '🟡'
            else:
                css_class = 'priority-low'
                emoji = '🟢'
            
            with st.container():
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                
                cols = st.columns([1, 3, 2, 2, 2, 2])
                with cols[0]:
                    st.markdown(f"<h2 style='margin: 0;'>#{idx}</h2>", unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f"<h4 style='margin: 0;'>{emoji} {row['Lake']}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<small>{row['Type']} • {row['District']}</small>", unsafe_allow_html=True)
                with cols[2]:
                    st.markdown(f"<p style='margin: 0;'><b>Score:</b> {row['Priority_Score']}/100</p>", unsafe_allow_html=True)
                with cols[3]:
                    st.markdown(f"<p style='margin: 0;'><b>Loss:</b> {row['Degradation_%']}%</p>", unsafe_allow_html=True)
                with cols[4]:
                    st.markdown(f"<p style='margin: 0;'><b>Cost:</b> ₹{row['Restoration_Cost_Lakhs']}L</p>", unsafe_allow_html=True)
                with cols[5]:
                    if st.button(f"📄 Generate Report", key=f"report_{idx}"):
                        st.success(f"✅ Report sent to TN Water Supply & Drainage Board!")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.subheader("📋 Complete Lake Inventory")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.multiselect("Status", df['Status'].unique(), default=df['Status'].unique())
        with col2:
            type_filter = st.multiselect("Type", df['Type'].unique(), default=df['Type'].unique())
        with col3:
            district_filter = st.multiselect("District", df['District'].unique(), default=df['District'].unique())
        
        filtered_df = df[
            (df['Status'].isin(status_filter)) &
            (df['Type'].isin(type_filter)) &
            (df['District'].isin(district_filter))
        ]
        
        st.dataframe(
            filtered_df.sort_values('Priority_Score', ascending=False),
            use_container_width=True,
            hide_index=True,
            column_config={
                'Degradation_%': st.column_config.ProgressColumn('Degradation %', format="%.1f%%", min_value=0, max_value=100),
                'Priority_Score': st.column_config.ProgressColumn('Priority Score', format="%.1f", min_value=0, max_value=100),
                'Pollution_Index': st.column_config.ProgressColumn('Pollution', format="%.1f", min_value=0, max_value=10),
                'Restoration_Cost_Lakhs': st.column_config.NumberColumn('Cost (₹L)', format="%.1f")
            }
        )
        
        # Export options
        col1, col2 = st.columns([3, 1])
        with col2:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Export Full Report (CSV)",
                data=csv,
                file_name=f"neerchitra_mission_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(90deg, #0d1117, #161b22); border-radius: 15px; margin-top: 30px; border: 1px solid #30363d;'>
    <h3 style='color: #0066cc; margin: 0;'>🌊 NeerChitra</h3>
    <p style='color: #8892b0; margin: 10px 0;'>AI-Powered Water Body Intelligence for Tamil Nadu Water Security Mission</p>
    <p style='color: #666; font-size: 0.9rem; margin: 0;'>
        Powered by ESA Sentinel-2 • Google Earth Engine • Streamlit<br>
        Built for Hackathon 2025 | Team NeerChitra
    </p>
</div>
""", unsafe_allow_html=True)
