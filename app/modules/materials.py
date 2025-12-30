import streamlit as st
from app.data.aisc_tables import ASTM_DETAILED_DATA, SHAPE_SERIES_LIST
from app.ui.components import section_label, result_card
from app.utils.images import render_svg_image

def render(_: str) -> None:
    col_in, col_res = st.columns([1, 1])

    with col_in:
        section_label("Input Parameters")
        sh_astm = st.selectbox("Select Shape Series:", SHAPE_SERIES_LIST, index=0, key="sh_astm_f")
        avail = sorted([n for n, d in ASTM_DETAILED_DATA["ASTM Designation"].items() if sh_astm in d["Shapes"]])
        astm_sel = st.selectbox("Select ASTM Designation:", avail, index=0, key="astm_sel_f")
        with st.expander("View Reference"):
            render_svg_image("table_2_4")

    with col_res:
        section_label("Calculated Results")
        d_astm = ASTM_DETAILED_DATA["ASTM Designation"][astm_sel]

        fy_res = "42" if astm_sel == "A500 Gr. B" and sh_astm == "HSS Round" else "46" if astm_sel == "A500 Gr. B" else d_astm.get("Fy", "N/A")
        if astm_sel == "A500 Gr. C":
            fy_res = "46" if sh_astm == "HSS Round" else "50"

        result_card("Yield Stress: Fy [ksi]", fy_res, "var(--accent)")
        result_card("Tensile Stress: Fu [ksi]", d_astm["Fu"], "var(--accent)")
