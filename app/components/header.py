import streamlit as st


def render_header():
    col1, col2, col3, col4 = st.columns([1,1,1,1],vertical_alignment="center")

    with col2:
        st.image("app/static/logo.png", width=200)

    with col3:    
        st.header("Atlas Scout")
