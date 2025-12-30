import streamlit as st

from app.data.aisc_tables import SHAPE_SERIES_LIST, ASTM_DETAILED_DATA, GAGE_DATA
from app.ui.components import section_label, result_card
from app.utils.images import render_image
from app.utils.formatting import eng_to_float, format_gage_key


def render(mod: str) -> None:
    col_in, col_res = st.columns([1, 1])

    # ===== ASTM =====
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

            fy_res = "42" if astm_sel == "A500 Gr. B" and sh_astm == "HSS Round" else \
                     "46" if astm_sel == "A500 Gr. B" else d_astm.get("Fy", "N/A")

            if astm_sel == "A500 Gr. C":
                fy_res = "46" if sh_astm == "HSS Round" else "50"

            result_card("Yield Stress: Fy [ksi]", fy_res, ok=True)
            result_card("Tensile Stress: Fu [ksi]", d_astm.get("Fu", "N/A"), ok=True)

        return

    # ===== GAGES =====
    if mod == "Angle Workable Gages":
        with col_in:
            section_label("Input Parameters")
            leg_opts = sorted(list(GAGE_DATA.keys()), key=lambda x: eng_to_float(x))
            leg_sel = st.selectbox("Select Angle Leg Length [in]:", leg_opts, index=0, key="leg_a_f")

            with st.expander("View Reference"):
                render_image("angle_gage", width="180px")

        with col_res:
            section_label("Calculated Results")
            res_g = GAGE_DATA[leg_sel]

            # stabilna kolejność: g, g1, g2...
            def g_sort_key(k: str) -> int:
                k = str(k)
                if k == "g":
                    return 0
                if k.startswith("g") and k[1:].isdigit():
                    return int(k[1:])
                return 999

            for k in sorted(res_g.keys(), key=g_sort_key):
                kk = format_gage_key(k)
                result_card(f"Gage {kk}: [in]", res_g[k], ok=True)

        return

    st.info("Not handled in materials module.")
