import streamlit as st
from components.layout import page_columns
from src.attributes import compute_geometry_attributes, compute_image_attributes

st.set_page_config(
    page_title="Atlas Scout",
    page_icon="static/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def compute_features(segments_gdf):
    gdf = segments_gdf.copy()
 
    gdf = compute_geometry_attributes(gdf)
    gdf = compute_image_attributes(gdf)
    
    return gdf 

left, center, right = page_columns()

with center:
    st.markdown("### Define features")

    if "segments_gdf" not in st.session_state or st.session_state.segments_gdf is None:
        st.warning("Run segmentation first to generate terrain segments.")
        st.stop()

    else:
        with st.spinner("Computing features..."):
                st.session_state.features_gdf = compute_features(
                    st.session_state.segments_gdf
                )
        st.success("Features computed")
        st.dataframe(st.session_state.features_gdf, use_container_width=True)