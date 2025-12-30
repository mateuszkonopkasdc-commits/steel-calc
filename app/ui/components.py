import streamlit as st

def section_label(text: str) -> None:
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)

def ref_text(text: str) -> None:
    st.markdown(f'<div class="ref-text">{text}</div>', unsafe_allow_html=True)

def input_info(label_html: str, value: str) -> None:
    st.markdown(
        f'<div class="input-info-label">{label_html}</div>'
        f'<div class="input-info-value">{value}</div>',
        unsafe_allow_html=True
    )

def result_card(label_html: str, value_html: str, color_css: str = "var(--accent)") -> None:
    st.markdown(
        f'<div class="result-card" style="border-left-color:{color_css};">'
        f'<div class="label-text" style="color:{color_css};">{label_html}</div>'
        f'<div class="fraction-val">{value_html}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
