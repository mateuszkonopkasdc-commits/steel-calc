import streamlit as st

from app.modules import bolts_strength, bolt_geometry, materials, conversions, welds
from app.ui.components import reference_text


MENU_STRUCTURE = {
    "🛠️ GENERAL DESIGN DATA": ["Angle Workable Gages", "ASTM Material Data", "Unit Conversions"],
    "📐 GEOMETRIC LIMITS": [
        "Bolt Hole Dimensions", "Bolt Min. Edge Distance", "Bolt Min. Spacing",
        "Effective Throat of Flare-Groove Welds", "Min. Throat of PJP Groove Welds",
        "Min. Size of Fillet Welds", "Max. Size of Fillet Welds"
    ],
    "📋 COMPONENT LIMIT STATES": ["Shear Strength of Bolts", "Tensile Strength of Bolts"]
}

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
    "Shear Strength of Bolts": bolts_strength.render,
    "Tensile Strength of Bolts": bolts_strength.render,
    "Bolt Hole Dimensions": bolt_geometry.render,
    "Bolt Min. Edge Distance": bolt_geometry.render,
    "Bolt Min. Spacing": bolt_geometry.render,
    "Angle Workable Gages": materials.render,
    "ASTM Material Data": materials.render,
    "Unit Conversions": conversions.render,
    "Effective Throat of Flare-Groove Welds": welds.render,
    "Min. Throat of PJP Groove Welds": welds.render,
    "Min. Size of Fillet Welds": welds.render,
    "Max. Size of Fillet Welds": welds.render,
}


def dispatch_module(mod: str | None) -> None:
    # Punkt 2: usuwamy żółty tekst (nie pokazujemy żadnego "info boxa" na start)
    if not mod:
        return

    # Punkt 4: Reference ma się wyświetlać zawsze, jeśli istnieje
    ref = REF_MAP.get(mod)
    if ref:
        reference_text(ref)

    # Render modułu
    handler = DISPATCH.get(mod)
    if handler:
        handler(mod)
    else:
        st.warning("Module not implemented yet.")
