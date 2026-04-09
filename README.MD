# Atlas Scout

Atlas Scout is a **Streamlit demo application** for **terrain-based decision support**.  
It helps users interpret **imagery and geospatial data** through a **chat-based copilot**, supporting **terrain feature identification**, **obstacle and change detection**, and **overlay visualization** in a compact interactive interface.

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
```

## Installation
```bash
pip install -r requirements.txt
```

## Run app
```bash
streamlit run app/app.py
```