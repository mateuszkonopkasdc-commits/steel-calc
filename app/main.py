import streamlit as st

from app.auth import require_login, logout_button
from app.ui.styles import inject_styles
from app.ui.components import render_sidebar
from app.modules.router import dispatch_module
from app.utils.images import render_image  # zakładam że masz render_image w utils/images.py

# ====== KONFIGURACJA STRONY ======
st.set_page_config(page_title="Engineering Platform | Steel Calc", layout="wide")
inject_styles()

# ====== LOGIN ======
require_login()

# ====== SIDEBAR ======
mod = render_sidebar()
logout_button()

# ====== MAIN ======
if mod:
    dispatch_module(mod)
else:
    # ====== HOME / START PAGE ======
    _, center_col, _ = st.columns([1, 6, 1])
    with center_col:
        # obrazek startowy (wraca)
        render_image("owtc", height="520px")

        st.markdown(
            "<h1 style='text-align:center; color:white; margin-top:10px;'>Steel-Calc Platform</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align:center; color:#a0a4b5; margin-top:-6px;'>Engineering calculators based on AISC 360-16</p>",
            unsafe_allow_html=True
        )

        # żółta informacja
        st.warning("Wybierz moduł z menu po lewej stronie, aby rozpocząć obliczenia.")

        st.divider()

        # autor + disclaimer jak wcześniej
        f_col1, f_col2, f_col3 = st.columns([1, 0.1, 3])
        with f_col1:
            st.markdown("Developed by:")
            st.markdown("👨‍💻 **Mateusz Konopka**")
        with f_col2:
            st.markdown('<div class="v-line"></div>', unsafe_allow_html=True)
        with f_col3:
            st.warning(
                "**Legal Disclaimer:** \n\nResults must be verified by a licensed PE. "
                "The author assumes no liability for compliance with AISC 360-16 or building codes."
            )
