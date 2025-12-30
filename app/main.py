import sys
from pathlib import Path
import streamlit as st

# --- FIX imports for local/cloud ---
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.auth import require_login
from app.ui.styles import inject_styles
from app.ui.components import render_sidebar
from app.modules.router import dispatch_module
from app.utils.images import render_image

MENU_STRUCTURE = {
    "🛠️ GENERAL DESIGN DATA": ["Angle Workable Gages", "ASTM Material Data", "Unit Conversions"],
    "📐 GEOMETRIC LIMITS": [
        "Bolt Hole Dimensions", "Bolt Min. Edge Distance", "Bolt Min. Spacing",
        "Effective Throat of Flare-Groove Welds", "Min. Throat of PJP Groove Welds",
        "Min. Size of Fillet Welds", "Max. Size of Fillet Welds"
    ],
    "📋 COMPONENT LIMIT STATES": ["Shear Strength of Bolts", "Tensile Strength of Bolts"],
}

st.set_page_config(page_title="Engineering Platform | Steel Calc", layout="wide")
inject_styles()

require_login()

# >>> TO NAPRAWIA TWOJ TYPEERROR NA CLOUD <<<
mod = render_sidebar(MENU_STRUCTURE)

if mod is None:
    # HOME
    _, center_col, _ = st.columns([1, 6, 1])
    with center_col:
        render_image("owtc", height="520px")

        st.markdown(
            "<h1 style='text-align:center; color:white; margin-top:10px;'>Steel-Calc Platform</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align:center; color:#a0a4b5; margin-top:-6px;'>Engineering calculators based on AISC 360-16</p>",
            unsafe_allow_html=True
        )

        st.divider()

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
else:
    dispatch_module(mod)
