import streamlit as st
from content.loader import load
from components.header import render_header

st.set_page_config(
    page_title="Atlas Scout",
    page_icon="static/logo.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

render_header()

content = load("info")

st.subheader("Purpose")
st.write(content["purpose"])

with st.expander("Key Requirements"):
    for item in content.get("key_requirements", []):
        st.markdown(f"- {item}")

with st.expander("Modules Overview"):
    for module in content.get("modules", []):
        st.markdown(f"- **{module['name']}** — {module['description']}")