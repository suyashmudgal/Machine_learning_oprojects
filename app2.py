import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io
import os

st.set_page_config(
    page_title="Satellite Image Analyzer",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🛰️ Satellite Image Analysis Dashboard</p>', unsafe_allow_html=True)
st.markdown("Upload satellite imagery (PNG, JPG, TIFF) to extract insights, statistics, and visualizations.")

# Sidebar
st.sidebar.header("⚙️ Settings")
st.sidebar.info("This app runs on Streamlit Cloud using only pure Python packages (no GDAL required).")
