import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

st.markdown("### Analysis")
st.caption("Dummy analysis page for now.")

with st.sidebar:
    st.subheader("Analysis settings")
    option = st.selectbox("Choose analysis", ["Overview", "Stats", "Export"])

st.write("This is where analysis stuff will go.")