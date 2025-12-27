import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Sovereign Intelligence", layout="wide")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data/Sovereign_Intelligence_Hub.csv")

df = load_data()

# Header
st.title("🛡️ Sovereign Intelligence Hub")
st.markdown("**The Global Return Risk Database** | Tracking 200+ Enterprise Assets")

# KPI Row
col1, col2, col3 = st.columns(3)
col1.metric("Brands Tracked", len(df))
col2.metric("Critical Risks Identified", len(df[df['SOVEREIGN_RISK_SCORE'] > 75]))
col3.metric("Avg Industry Risk", f"{int(df['SOVEREIGN_RISK_SCORE'].mean())}/100")

# Search Bar
brand_input = st.text_input("Search Brand Asset (e.g. Spanx, Nike)", "")

if brand_input:
    match = df[df['Brand'].str.contains(brand_input, case=False)]
    if not match.empty:
        st.dataframe(match)
        score = match.iloc[0]['SOVEREIGN_RISK_SCORE']
        if score > 75:
            st.error(f"🚨 CRITICAL RISK DETECTED: Score {score}")
        else:
            st.success(f"✅ STABLE ASSET: Score {score}")
    else:
        st.warning("Brand not found in Sovereign Index.")

# Leaderboard
st.subheader("⚠️ High Risk Watchlist")
st.dataframe(df[df['SOVEREIGN_RISK_SCORE'] > 80].sort_values('SOVEREIGN_RISK_SCORE', ascending=False).head(10))