# ==== FIX ŚCIEŻEK DLA STREAMLIT CLOUD ====
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # steel-calc/
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# ========================================

import streamlit as st

from app.auth import require_login, logout_button
from app.ui.styles import inject_styles
from app.ui.components import render_sidebar
from app.modules.router import dispatch_module

st.set_page_config(page_title="Engineering Platform | Steel Calc", layout="wide")
inject_styles()

# LOGIN
require_login()

# SIDEBAR
selected = render_sidebar()
with st.sidebar:
    st.divider()
    logout_button("Wyloguj")

# ROUTING
if selected is None:
    st.markdown(
        """
        <h1 style="margin-bottom:0.2em;">🏗️ Steel-Calc Platform</h1>
        <p style="opacity:0.8;">Engineering calculators based on AISC 360-16</p>
        """,
        unsafe_allow_html=True,
    )
    st.info("Wybierz moduł z menu po lewej stronie, aby rozpocząć obliczenia.")
else:
    dispatch_module(selected)
