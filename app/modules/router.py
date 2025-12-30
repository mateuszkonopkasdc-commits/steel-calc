import streamlit as st
from app.ui.components import reference_text

# Importy modułów (bez importowania w app/modules/__init__.py!)
from app.modules import bolts_strength, bolt_geometry, materials, conversions, welds

REF_MAP = {
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
    "Tensile Strength of Bolts": "Reference: AISC 360-16 Section J3.6",
}

DISPATCH = {
    # COMPONENT LIMIT STATES
    "Shear Strength of Bolts": bolts_strength.render,
    "Tensile Strength of Bolts": bolts_strength.render,

    # GEOMETRIC LIMITS
    "Bolt Hole Dimensions": bolt_geometry.render,
    "Bolt Min. Edge Distance": bolt_geometry.render,
    "Bolt Min. Spacing": bolt_geometry.render,

    # GENERAL DESIGN DATA
    "Angle Workable Gages": materials.render,
    "ASTM Material Data": materials.render,
    "Unit Conversions": conversions.render,

    # WELDS
    "Effective Throat of Flare-Groove Welds": welds.render,
    "Min. Throat of PJP Groove Welds": welds.render,
    "Min. Size of Fillet Welds": welds.render,
    "Max. Size of Fillet Welds": welds.render,
}

def dispatch_module(mod: str) -> None:
    # nagłówek
    icon = "📋" if st.session_state.get("active_section") and "📋" in st.session_state.get("active_section") else \
           "📐" if st.session_state.get("active_section") and "📐" in st.session_state.get("active_section") else "📏"
    st.markdown(f'<h1 style="font-size: 1.6rem; margin-bottom: 0;">{icon} {mod}</h1>', unsafe_allow_html=True)

    # reference (tekst)
    ref = REF_MAP.get(mod)
    if ref:
        reference_text(ref)

    st.divider()

    handler = DISPATCH.get(mod)
    if not handler:
        st.error(f"Brak obsługi modułu: {mod}")
        return

    handler(mod)
