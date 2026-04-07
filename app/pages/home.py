import streamlit as st
from streamlit_extras.card_selector import *
from components.header import render_header
from components.layout import page_columns

render_header()

selected = card_selector(
[
    dict(
        icon=":material/info:",
        title="Info",
        description="App purpose, key requirements, and overview"
    ),
    dict(
        icon=":material/grid_view:",
        title="Segment",
        description="Split terrain into useful segments for analysis and planning"
    ),
    dict(
        icon=":material/tune:",
        title="Feature",
        description="Define features and classify terrain segments"
    ),
    dict(
        icon=":material/layers:",
        title="Overlay",
        description="Visualize terrain layers, markers, and map overlays"
    ),
],  # type: ignore
key="home_cards",
)

# Routing
if selected == 0:
    st.switch_page("pages/info.py")

elif selected == 1:
    st.switch_page("pages/segment.py")

elif selected == 2:
    st.switch_page("pages/feature.py")

elif selected == 3:
        st.switch_page("pages/overlay.py")

query = st.chat_input("Ask about terrain, segments, features, or overlays...")