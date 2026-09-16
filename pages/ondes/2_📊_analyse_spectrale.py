import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))


import matplotlib.pyplot as plt
import streamlit as st

st.title("Analyse Spectrale")

fig, axes = plt.subplots(ncols=2)

st_plt = st.pyplot(fig)
