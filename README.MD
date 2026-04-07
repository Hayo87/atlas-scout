# Atlas Scout

Atlas Scout is a **Streamlit demo application** for terrain analysis and geospatial exploration.  
It is designed to support **terrain segmentation**, **feature identification**, and **overlay visualization** through a compact interactive interface.

---

## Project Structure

```bash
atlas_scout/
│
├── app/                    # Streamlit application
│   ├── pages/              # Multi-page Streamlit views
│   ├── static/             # Static assets (logo, images, etc.)
│   ├── content/            # YAML-based page content
│   └── components/         # Shared UI/layout components
│
├── src/                    # Core processing and application logic
├── notebooks/              # Exploration, experiments, and prototyping
├── requirements.txt
└── README.md

## Installation
```bash
pip install -r requirements.txt

## Run app
```bash
streamlit run app/app.py