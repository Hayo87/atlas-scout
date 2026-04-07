import streamlit as st
from streamlit_extras.card_selector import *
from components.header import render_header
from components.layout import page_columns

st.set_page_config(
    page_title="Atlas Scout",
    page_icon="static/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

render_header()

left, center, right = page_columns()

with left:
    with st.container(border=True):
        st.write("LEFT")

with center:
    with st.container(border=True):
        st.write("CENTER")

with right:
    with st.container(border=True):
        st.write("RIGHT")