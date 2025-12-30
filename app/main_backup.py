import streamlit as st

from app.ui.styles import inject_styles
from app.ui.components import ref_text
from app.modules import bolts_strength, bolt_geometry, materials, conversions, welds, angle_gages
from app.utils.images import render_svg_image

st.set_page_config(page_title="Engineering Platform | AISC Tools", layout="wide")
inject_styles()

# --- NAV STATE ---
if "active_section" not in st.session_state:
    st.session_state.active_section = None
if "active_module" not in st.session_state:
    st.session_state.active_module = None

menu_structure = {
    "🛠️ GENERAL DESIGN DATA": ["Angle Workable Gages", "ASTM Material Data", "Unit Conversions"],
    "📐 GEOMETRIC LIMITS": [
        "Bolt Hole Dimensions", "Bolt Min. Edge Distance", "Bolt Min. Spacing",
        "Effective Throat of Flare-Groove Welds", "Min. Throat of PJP Groove Welds",
        "Min. Size of Fillet Welds", "Max. Size of Fillet Welds"
    ],
    "📋 COMPONENT LIMIT STATES": ["Shear Strength of Bolts", "Tensile Strength of Bolts"]
}

for label, modules in menu_structure.items():
    if st.sidebar.button(label, key=f"btn_{label}"):
        if st.session_state.active_section == label:
            st.session_state.active_section = None
            st.session_state.active_module = None
        else:
            st.session_state.active_section = label
            st.session_state.active_module = modules[0]
        st.rerun()

    if st.session_state.active_section == label:
        idx = modules.index(st.session_state.active_module) if st.session_state.active_module in modules else 0
        st.session_state.active_module = st.sidebar.radio("", options=modules, index=idx, key=f"nav_{label}")

mod = st.session_state.active_module

if mod is not None:
    icon = "📋" if "📋" in (st.session_state.active_section or "") else "📐" if "📐" in (st.session_state.active_section or "") else "📏"
    st.markdown(f'<h1 style="font-size: 1.6rem; margin-bottom: 0;">{icon} {mod}</h1>', unsafe_allow_html=True)

    ref_map = {
        "Angle Workable Gages": "Reference: AISC 15th Ed. Table 1-7A",
        "ASTM Material Data": "Reference: AISC 360-16 Table 2-4",
        "Bolt Hole Dimensions": "Reference: AISC 360-16 Table J3.3",
        "Bolt Min. Edge Distance": "Reference: AISC 360-16 Table J3.4 & Table J3.5",
        "Bolt Min. Spacing": "Reference: AISC 360-16 Section J3.3",
        "Effective Throat of Flare-Groove Welds": "Reference: AISC 360-16 Table J2.2",
        "Min. Throat of PJP Groove Welds": "Reference: AISC 360-16 Table J2.3",
        "Min. Size of Fillet Welds": "Reference: AISC 360-16 Table J2.4",
        "Max. Size of Fillet Welds": "Reference: AISC 360-16 Section J2.2b",
        "Shear Strength of Bolts": "Reference: AISC 360-16 Section J3.6",
        "Tensile Strength of Bolts": "Reference: AISC 360-16 Section J3.6"
    }
    if mod in ref_map:
        ref_text(ref_map[mod])

    st.divider()

    if mod in ["Shear Strength of Bolts", "Tensile Strength of Bolts"]:
        bolts_strength.render(mod)
    elif mod in ["Bolt Hole Dimensions", "Bolt Min. Edge Distance", "Bolt Min. Spacing"]:
        bolt_geometry.render(mod)
    elif mod == "ASTM Material Data":
        materials.render(mod)
    elif mod == "Unit Conversions":
        conversions.render(mod)
    elif mod in [
        "Effective Throat of Flare-Groove Welds",
        "Min. Throat of PJP Groove Welds",
        "Min. Size of Fillet Welds",
        "Max. Size of Fillet Welds"
    ]:
        welds.render(mod)
    elif mod == "Angle Workable Gages":
        angle_gages.render(mod)

else:
    _, center_col, _ = st.columns([1, 6, 1])
    with center_col:
        render_svg_image("owtc", height="530px")
        st.markdown("<h1 style='text-align: center; color: white;'>Engineering Platform</h1>", unsafe_allow_html=True)
        st.divider()
        f_col1, f_col2, f_col3 = st.columns([1, 0.1, 3])
        with f_col1:
            st.markdown("Developed by:")
            st.markdown("👨‍💻 **Mateusz Konopka**")
        with f_col2:
            st.markdown('<div class="v-line"></div>', unsafe_allow_html=True)
        with f_col3:
            st.warning("**Legal Disclaimer:** \n\nResults must be verified by a licensed PE. The author assumes no liability for compliance with AISC 360-16 or building codes.")
