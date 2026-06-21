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
# File Uploader
uploaded_file = st.file_uploader(
    "📤 Upload Satellite Image",
    type=["tif", "tiff", "png", "jpg", "jpeg"],
    accept_multiple_files=False
)

@st.cache_data(show_spinner=False)
def load_image(uploaded_file):
    """Load image using PIL only — works everywhere including Streamlit Cloud."""
    file_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(file_bytes))
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Ensure shape is (bands, h, w)
    if len(img_array.shape) == 2:
        # Grayscale
        img_array = img_array[np.newaxis, :, :]  # (1, h, w)
        img_display = np.stack([img_array[0]] * 3, axis=-1)  # (h, w, 3)
    elif len(img_array.shape) == 3:
        # Color image (h, w, bands)
        img_display = img_array
        img_array = np.transpose(img_array, (2, 0, 1))  # (bands, h, w)
    else:
        raise ValueError("Unsupported image dimensions")
    
    return {
        'array': img_array,        # (bands, h, w)
        'display': img_display,    # (h, w, bands)
        'name': uploaded_file.name,
        'mode': image.mode
    }