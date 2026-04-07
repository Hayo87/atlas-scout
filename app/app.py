import sys
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Atlas Scout",
    page_icon="static/logo.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

pages = [
        st.Page("pages/home.py", title="Home", url_path="home", icon=":material/home:"),
        st.Page("pages/info.py", title="Info", url_path="info", icon=":material/info:"),
        st.Page("pages/segment.py", title="Segement", url_path="feed", icon=":material/photo_library:"),
        st.Page("pages/feature.py", title="Feature", url_path="calendar", icon=":material/edit:"),
        st.Page("pages/overlay.py", title="Overlay", url_path="overlay", icon=":material/edit:"),
    ]

pg = st.navigation(pages, position="top")
pg.run()