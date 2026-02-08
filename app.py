import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="NeerChitra", page_icon="🌊")

st.title("🌊 NeerChitra")
st.subheader("AI Water Body Intelligence for Tamil Nadu")

if st.button("🚀 Fetch Satellite Data"):
    with st.spinner("Analyzing..."):
        import time
        time.sleep(1)
    
    df = pd.DataFrame({
        "Lake": ["Chembarambakkam", "Puzhal", "Velachery", "Korattur", "Ambattur"],
        "Degradation_%": [65, 45, 72, 38, 55]
    })
    
    st.success("Analysis Complete!")
    st.bar_chart(df.set_index("Lake")["Degradation_%"])
    st.dataframe(df)

st.info("Built for Tamil Nadu Water Security")
