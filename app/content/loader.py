import yaml
from pathlib import Path
import streamlit as st

@st.cache_data
def load(page_name: str) -> dict:
    path = f"app/content/{page_name}.yaml"

    print(path)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)