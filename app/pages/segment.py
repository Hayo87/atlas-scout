import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import leafmap.foliumap as leafmap

from src.config import ORIGINAL_PATH, PREVIEW_PATH
from src.raster import load_tif
from src.segmentation import build_segments, segments_to_gdf
from components.layout import page_columns


st.set_page_config(
    page_title="Atlas Scout",
    page_icon="static/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_data
def get_preview(resize: int):
    return load_tif(str(ORIGINAL_PATH), resize=resize)

if "segments_gdf" not in st.session_state:
    st.session_state.segments_gdf = None

if "segment_count" not in st.session_state:
    st.session_state.segment_count = None


left, center, right = page_columns()

with left:
    with st.container(border=True):
        with st.form("segmentation_form", border=False):
            st.subheader("Settings")
            resize = st.slider("Preview downscale factor", 1, 8, 4)
            scale = st.slider("Scale", 50, 1000, 100, step=25)
            sigma = st.slider("Sigma", 0.0, 2.0, 1.0, step=0.1)
            min_size = st.slider("Min size", 20, 3000, 1000, step=100)

            apply_segmentation = st.form_submit_button(
                "Apply segmentation",
                use_container_width=True
            )

with center:
    with st.container(border=True):
        st.markdown("### Segmentation")
        st.caption(f"Preview segmentation on `{ORIGINAL_PATH.name}` with adjustable parameters.")

        if apply_segmentation:
            with st.spinner("Updating segmentation..."):
                img, crs, transform = get_preview(resize)

                segments = build_segments(
                    img,
                    scale=scale,
                    sigma=sigma,
                    min_size=min_size,
                )

                gdf = segments_to_gdf(segments, transform, crs)

                st.session_state.segments_gdf = gdf
                st.session_state.segment_count = len(gdf)

            st.toast(f"Segmentation ready • {len(gdf)} segments")

        m = leafmap.Map()
        m.add_raster(str(PREVIEW_PATH), layer_name="Image")

        if st.session_state.segments_gdf is not None:
            m.add_gdf(
                st.session_state.segments_gdf,
                layer_name="Segments",
                style={
                    "color": "red",
                    "weight": 1,
                    "fillOpacity": 0,
                },
            )

        m.to_streamlit(height=450)

 
        with st.expander("ℹ️ Information", expanded=True):
            st.markdown("""
            **What is this map?**  
            This is a preview satellite or aerial image used to test image segmentation.
            The segmentation overlay splits the image into visual regions based on color and texture.

            **Scale**  
            Controls how large segments become.  
            - Lower → more detail, more segments  
            - Higher → fewer, larger regions  

            **Sigma**  
            Controls how much the image is smoothed before segmentation.  
            - Lower → sharper boundaries  
            - Higher → smoother, less noisy segmentation  

            **Min size**  
            Controls the minimum allowed segment size.  
            - Lower → keeps tiny fragments  
            - Higher → removes small noisy pieces  
            """)

with right:
    with st.container(border=True):
        st.subheader("Results")

        if st.session_state.segments_gdf is not None:
            gdf = st.session_state.segments_gdf

            count = len(gdf)
            avg_area = gdf.area.mean()
            min_area = gdf.area.min()
            max_area = gdf.area.max()

            st.metric("Segments", count)
            st.metric("Avg size", f"{avg_area:.1f}")
            st.metric("Min size", f"{min_area:.1f}")
            st.metric("Max size", f"{max_area:.1f}")

        else:
            st.caption("No segmentation applied yet.")