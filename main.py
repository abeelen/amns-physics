from pathlib import Path
import sys

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Bienvenue sur les exemples d'optique géométrique ! 👋")

st.sidebar.success("Selectionnez une page.")
