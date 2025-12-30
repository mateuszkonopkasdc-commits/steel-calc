import streamlit as st


def section_header(title: str):
    st.markdown(f'<div class="section-label">{title}</div>', unsafe_allow_html=True)


def input_info(label_html: str, value: str):
    st.markdown(
        f'<div class="input-info-label">{label_html}</div>'
        f'<div class="input-info-value">{value}</div>',
        unsafe_allow_html=True,
    )


def result_card(label_html: str, value_html: str, color_css: str = "var(--accent)"):
    st.markdown(
        f'<div class="result-card" style="border-left-color:{color_css};">'
        f'<div class="label-text" style="color:{color_css};">{label_html}</div>'
        f'<div class="fraction-val">{value_html}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def render_sidebar() -> str | None:
    """
    Sidebar menu (toggle sections + radio modules) – jak w Twojej wersji monolitycznej.
    Zwraca: aktywny moduł (string) albo None (welcome).
    """
    if "active_section" not in st.session_state:
        st.session_state.active_section = None
    if "active_module" not in st.session_state:
        st.session_state.active_module = None

    menu_structure = {
        "🛠️ GENERAL DESIGN DATA": ["Angle Workable Gages", "ASTM Material Data", "Unit Conversions"],
        "📐 GEOMETRIC LIMITS": [
            "Bolt Hole Dimensions",
            "Bolt Min. Edge Distance",
            "Bolt Min. Spacing",
            "Effective Throat of Flare-Groove Welds",
            "Min. Throat of PJP Groove Welds",
            "Min. Size of Fillet Welds",
            "Max. Size of Fillet Welds",
        ],
        "📋 COMPONENT LIMIT STATES": ["Shear Strength of Bolts", "Tensile Strength of Bolts"],
    }

    st.sidebar.markdown("### Menu")

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
            curr_idx = modules.index(st.session_state.active_module) if st.session_state.active_module in modules else 0
            st.session_state.active_module = st.sidebar.radio(
                label="",
                options=modules,
                index=curr_idx,
                key=f"nav_radio_{label}",
            )

    return st.session_state.active_module
