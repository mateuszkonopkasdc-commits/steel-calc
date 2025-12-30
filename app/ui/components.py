import streamlit as st

# ===== UI helpers =====

def section_label(text: str) -> None:
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def reference_text(text: str) -> None:
    # używa stylu .ref-text, który masz w styles.py
    st.markdown(f'<div class="ref-text">{text}</div>', unsafe_allow_html=True)


def input_info(label_html: str, value: str) -> None:
    st.markdown(
        f'<div class="input-info-label">{label_html}</div>'
        f'<div class="input-info-value">{value}</div>',
        unsafe_allow_html=True,
    )


def result_card(label_html: str, value_html: str, ok: bool = False) -> None:
    color = "var(--ok)" if ok else "var(--accent)"
    st.markdown(
        f'<div class="result-card" style="border-left-color:{color};">'
        f'<div class="label-text" style="color:{color};">{label_html}</div>'
        f'<div class="fraction-val">{value_html}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_sidebar(menu_structure: dict[str, list[str]]) -> str | None:
    """
    Renders the sidebar menu and returns the currently selected module name.
    No 'Menu' header, no logout button here.
    """
    if "active_section" not in st.session_state:
        st.session_state.active_section = None
    if "active_module" not in st.session_state:
        st.session_state.active_module = None

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
            curr_idx = 0
            if st.session_state.active_module in modules:
                curr_idx = modules.index(st.session_state.active_module)

            st.session_state.active_module = st.sidebar.radio(
                label="",
                options=modules,
                index=curr_idx,
                key=f"nav_radio_{label}",
            )

    return st.session_state.active_module
