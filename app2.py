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
    def normalize_for_display(arr):
    """Normalize array to 0-255 for display."""
    arr = arr.astype(np.float32)
    min_val = np.percentile(arr, 2)
    max_val = np.percentile(arr, 98)
    arr = np.clip((arr - min_val) / (max_val - min_val + 1e-8), 0, 1)
    return (arr * 255).astype(np.uint8)

if uploaded_file is not None:
    with st.spinner("🔄 Processing image..."):
        try:
            data = load_image(uploaded_file)
        except Exception as e:
            st.error(f"Error loading image: {e}")
            st.stop()
    
    arr = data['array']  # (bands, h, w)
    display_img = data['display']
    n_bands = arr.shape[0]
    height, width = arr.shape[1], arr.shape[2]
    
    # ==================== OVERVIEW METRICS ====================
    st.markdown("---")
    st.subheader("📊 Image Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Width", f"{width:,} px")
    with col2:
        st.metric("Height", f"{height:,} px")
    with col3:
        st.metric("Bands", n_bands)
    with col4:
        st.metric("Data Type", str(arr.dtype))
    with col5:
        st.metric("Mode", data['mode'])
    
    st.info("ℹ️ Running in **PIL-only mode** — no GDAL required. For GeoTIFF metadata, use a local Python environment with rasterio installed.")
    
    # ==================== TABS ====================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🖼️ Image Viewer", 
        "📈 Band Statistics", 
        "📉 Histograms", 
        "🌿 NDVI / Indices", 
        "🔬 Spectral Profile"
    ])
     # -------- TAB 1: Image Viewer --------
    with tab1:
        st.subheader("Image Preview")
        
        viz_col1, viz_col2 = st.columns([3, 1])
        
        with viz_col2:
            st.markdown("**Visualization Options**")
            
            if n_bands >= 3:
                composite = st.selectbox(
                    "Color Composite",
                    ["True Color (R-G-B)", "False Color (Band 3-Band 1-Band 2)", "False Color (Band 4-Band 3-Band 1)", "Custom"]
                )
                
                if composite == "Custom":
                    r_band = st.selectbox("Red Channel", range(1, n_bands+1), index=0) - 1
                    g_band = st.selectbox("Green Channel", range(1, n_bands+1), index=min(1, n_bands-1)) - 1
                    b_band = st.selectbox("Blue Channel", range(1, n_bands+1), index=min(2, n_bands-1)) - 1
                elif composite == "True Color (R-G-B)":
                    r_band, g_band, b_band = 0, 1, 2
                elif composite == "False Color (Band 3-Band 1-Band 2)":
                    r_band, g_band, b_band = min(2, n_bands-1), 0, 1
                else:  # Band 4-Band 3-Band 1
                    r_band, g_band, b_band = min(3, n_bands-1), min(2, n_bands-1), 0
            else:
                r_band = g_band = b_band = 0
                composite = "Grayscale"
            
            enhance = st.checkbox("Auto-Enhance Contrast (2-98%)", value=True)
            show_original = st.checkbox("Show Original (no enhance)", value=False)
        
        with viz_col1:
            if n_bands >= 3 and composite != "Grayscale":
                rgb = np.stack([arr[r_band], arr[g_band], arr[b_band]], axis=-1)
                if enhance and not show_original:
                    rgb = normalize_for_display(rgb)
                fig = px.imshow(rgb, title=f"Composite: {composite}")
            else:
                band_to_show = arr[0]
                if enhance and not show_original:
                    band_to_show = normalize_for_display(band_to_show)
                fig = px.imshow(band_to_show, color_continuous_scale='gray', title="Grayscale")
            
            fig.update_layout(
                xaxis_title="Pixel Column",
                yaxis_title="Pixel Row",
                coloraxis_showscale=True,
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # -------- TAB 2: Band Statistics --------
    with tab2:
        st.subheader("Per-Band Statistics")
        
        import pandas as pd
        stats_data = []
        for b in range(n_bands):
            band = arr[b]
            stats_data.append({
                'Band': f'Band {b+1}',
                'Min': np.min(band),
                'Max': np.max(band),
                'Mean': round(np.mean(band), 2),
                'Median': round(np.median(band), 2),
                'Std Dev': round(np.std(band), 2),
                'Non-Zero %': round(100 * np.count_nonzero(band) / band.size, 2)
            })
        
        df_stats = pd.DataFrame(stats_data)
        st.dataframe(df_stats, use_container_width=True, hide_index=True)
        
        # Bar chart of means
        fig_means = go.Figure()
        fig_means.add_trace(go.Bar(
            x=df_stats['Band'],
            y=df_stats['Mean'],
            marker_color='#1f77b4',
            name='Mean'
        ))
        fig_means.add_trace(go.Bar(
            x=df_stats['Band'],
            y=df_stats['Std Dev'],
            marker_color='#ff7f0e',
            name='Std Dev'
        ))
        fig_means.update_layout(
            barmode='group',
            title="Mean vs Standard Deviation by Band",
            xaxis_title="Band",
            yaxis_title="Value",
            height=400
        )
        st.plotly_chart(fig_means, use_container_width=True)
    
    # -------- TAB 3: Histograms --------
    with tab3:
        st.subheader("Pixel Distribution Histograms")
        
        hist_col1, hist_col2 = st.columns(2)
        with hist_col1:
            selected_bands = st.multiselect(
                "Select bands to plot",
                [f"Band {i+1}" for i in range(n_bands)],
                default=[f"Band {i+1}" for i in range(min(3, n_bands))]
            )
        with hist_col2:
            bins = st.slider("Number of Bins", min_value=50, max_value=500, value=256)
        
        fig_hist = go.Figure()
        colors = px.colors.qualitative.Plotly
        
        for idx, band_name in enumerate(selected_bands):
            b = int(band_name.split()[1]) - 1
            band_data = arr[b].flatten()
            # Remove no-data values for histogram
            band_data = band_data[band_data > 0] if np.any(band_data == 0) else band_data
            
            fig_hist.add_trace(go.Histogram(
                x=band_data,
                name=band_name,
                opacity=0.6,
                nbinsx=bins,
                marker_color=colors[idx % len(colors)]
            ))
        
        fig_hist.update_layout(
            barmode='overlay',
            title="Pixel Intensity Distribution",
            xaxis_title="Pixel Value",
            yaxis_title="Frequency",
            height=500
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Box plot
        st.markdown("**Box Plot Comparison**")
        fig_box = go.Figure()
        for b in range(n_bands):
            fig_box.add_trace(go.Box(
                y=arr[b].flatten(),
                name=f'Band {b+1}',
                boxpoints=False
            ))
        fig_box.update_layout(
            title="Box Plot by Band",
            yaxis_title="Pixel Value",
            height=400
        )
        st.plotly_chart(fig_box, use_container_width=True)