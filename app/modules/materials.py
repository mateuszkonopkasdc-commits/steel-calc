import streamlit as st
from app.data.aisc_tables import SHAPE_SERIES_LIST, ASTM_DETAILED_DATA, GAGE_DATA
from app.utils.formatting import eng_to_float, format_gage_key
from app.ui.components import section_label, result_card
from app.utils.images import render_image


def render(mod: str) -> None:
    col_in, col_res = st.columns([1, 1])

    if mod == "ASTM Material Data":
        with col_in:
            section_label("Input Parameters")
            sh_astm = st.selectbox("Select Shape Series:", SHAPE_SERIES_LIST, index=0, key="sh_astm_f")
            avail = sorted([n for n, d in ASTM_DETAILED_DATA["ASTM Designation"].items() if sh_astm in d["Shapes"]])
            astm_sel = st.selectbox("Select ASTM Designation:", avail, index=0, key="astm_sel_f")

            with st.expander("View Reference"):
                render_image("table_2_4")

        with col_res:
            section_label("Calculated Results")
            d_astm = ASTM_DETAILED_DATA["ASTM Designation"][astm_sel]

            fy_res = "42" if astm_sel == "A500 Gr. B" and sh_astm == "HSS Round" else "46" if astm_sel == "A500 Gr. B" else d_astm.get("Fy", "N/A")
            if astm_sel == "A500 Gr. C":
                fy_res = "46" if sh_astm == "HSS Round" else "50"

            result_card("Yield Stress: Fy [ksi]", fy_res, color="ok")
            result_card("Tensile Stress: Fu [ksi]", d_astm["Fu"], color="ok")

    elif mod == "Angle Workable Gages":
        with col_in:
            section_label("Input Parameters")
            leg_opts = sorted(list(GAGE_DATA.keys()), key=lambda x: eng_to_float(x))
            leg_sel = st.selectbox("Select Angle Leg Length [in]:", leg_opts, index=0, key="leg_a_f")

            with st.expander("View Reference"):
                render_image("angle_gage", width="180px")

        with col_res:
            section_label("Calculated Results")
            res_g = GAGE_DATA[leg_sel]
            for k, v in res_g.items():
                kk = format_gage_key(k)
                result_card(f"Gage {kk}: [in]", v, color="ok")

    else:
        st.info("Not handled in materials module.")
