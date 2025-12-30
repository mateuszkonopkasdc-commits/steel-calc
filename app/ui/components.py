import streamlit as st

# ====== UI HELPERS (używane w modułach) ======

def section_label(text: str) -> None:
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)

def input_info(label_html: str, value: str | float) -> None:
    st.markdown(
        f'<div class="input-info-label">{label_html}</div>'
        f'<div class="input-info-value">{value}</div>',
        unsafe_allow_html=True
    )

def result_card(label_html: str, value_html: str, ok: bool = False) -> None:
    border = "var(--ok)" if ok else "var(--accent)"
    st.markdown(
        f'<div class="result-card" style="border-left-color:{border};">'
        f'<div class="label-text" style="color:{border};">{label_html}</div>'
        f'<div class="fraction-val">{value_html}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

# ====== SIDEBAR (menu) ======

MENU_STRUCTURE = {
    "🛠️ GENERAL DESIGN DATA": ["Angle Workable Gages", "ASTM Material Data", "Unit Conversions"],
    "📐 GEOMETRIC LIMITS": [
        "Bolt Hole Dimensions", "Bolt Min. Edge Distance", "Bolt Min. Spacing",
        "Effective Throat of Flare-Groove Welds", "Min. Throat of PJP Groove Welds",
        "Min. Size of Fillet Welds", "Max. Size of Fillet Welds"
    ],
    "📋 COMPONENT LIMIT STATES": ["Shear Strength of Bolts", "Tensile Strength of Bolts"]
}

def render_sidebar() -> str | None:
    if "active_section" not in st.session_state:
        st.session_state.active_section = None
    if "active_module" not in st.session_state:
        st.session_state.active_module = None

    st.sidebar.markdown("## Menu")

    for section_label_txt, modules in MENU_STRUCTURE.items():
        if st.sidebar.button(section_label_txt, key=f"sec_{section_label_txt}"):
            if st.session_state.active_section == section_label_txt:
                st.session_state.active_section = None
                st.session_state.active_module = None
            else:
                st.session_state.active_section = section_label_txt
                st.session_state.active_module = modules[0]
            st.rerun()

        if st.session_state.active_section == section_label_txt:
            idx = modules.index(st.session_state.active_module) if st.session_state.active_module in modules else 0
            st.session_state.active_module = st.sidebar.radio(
                label="",
                options=modules,
                index=idx,
                key=f"mod_{section_label_txt}",
            )

    return st.session_state.active_module
