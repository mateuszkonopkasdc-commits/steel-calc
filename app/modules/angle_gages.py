import streamlit as st
from app.data.aisc_tables import GAGE_DATA
from app.ui.components import section_label
from app.utils.images import render_svg_image
from app.utils.formatting import eng_to_float, format_gage_key

def render(_: str) -> None:
    col_in, col_res = st.columns([1, 1])
    with col_in:
        section_label("Input Parameters")
        leg_opts = sorted(list(GAGE_DATA.keys()), key=lambda x: eng_to_float(x))
        leg_sel = st.selectbox("Select Angle Leg Length [in]:", leg_opts, index=0, key="leg_a_f")
        with st.expander("View Reference"):
            render_svg_image("angle_gage", width="180px")
    with col_res:
        section_label("Calculated Results")
        res_g = GAGE_DATA[leg_sel]
        for k, v in res_g.items():
            kk = format_gage_key(k)
            st.markdown(
                f'<div class="result-card"><div class="label-text">Gage {kk}: [in]</div><div class="fraction-val">{v}</div></div>',
                unsafe_allow_html=True
            )
