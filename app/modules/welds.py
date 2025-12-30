import streamlit as st
from app.ui.components import section_label, result_card
from app.utils.formatting import (
    THICKNESS_FRACTIONS_LIMIT, THICKNESS_VALUES_LIMIT,
    THICKNESS_FRACTIONS_WIDE, THICKNESS_VALUES_WIDE,
    format_eng_frac_no_unit
)
from app.utils.images import render_svg_image

def render(mod: str) -> None:
    col_in, col_res = st.columns([1, 1])

    if mod == "Effective Throat of Flare-Groove Welds":
        with col_in:
            section_label("Input Parameters")
            hss = st.radio("Is This An HSS Member?", ["Yes", "No"], key="hss_f")

            if hss == "Yes":
                t_sel = st.selectbox("Thickness [in]:", THICKNESS_FRACTIONS_LIMIT, index=0, key="t_f")
                r_v = 2.0 * THICKNESS_VALUES_LIMIT[t_sel]
            else:
                t_sel = st.selectbox("R [in]:", THICKNESS_FRACTIONS_WIDE, index=0, key="r_f")
                r_v = THICKNESS_VALUES_WIDE[t_sel]

            proc = st.selectbox("Process:", ["GMAW and FCAW-G", "SMAW and FCAW-S", "SAW"], index=0, key="p_f")
            wty = st.selectbox("Type:", ["Flare Bevel Groove", "Flare V-Groove"], index=0, key="w_f")

            with st.expander("View Reference"):
                render_svg_image("table_j2_2")

        with col_res:
            section_label("Calculated Results")
            fac = 0.625 if wty == "Flare Bevel Groove" and proc == "GMAW and FCAW-G" else 0.3125
            if wty == "Flare V-Groove":
                fac = 0.75 if proc == "GMAW and FCAW-G" else 0.625 if proc == "SMAW and FCAW-S" else 0.5
            result_card("Effective Throat of PJP Weld [in]", format_eng_frac_no_unit(r_v * fac), "var(--accent)")
        return

    if mod == "Min. Throat of PJP Groove Welds":
        with col_in:
            section_label("Input Parameters")
            ranges_pjp = [
                "To 1/4 inclusive", "Over 1/4 to 1/2 inclusive", "Over 1/2 to 3/4 inclusive",
                "Over 3/4 to 1 1/2 inclusive", "Over 1 1/2 to 2 1/4 inclusive",
                "Over 2 1/4 to 6 inclusive", "Over 6"
            ]
            t_p = st.selectbox("Thickness of Thinner Part [in]:", ranges_pjp, index=0, key="tp_f")
            with st.expander("View Reference"):
                render_svg_image("table_j2_3")

        with col_res:
            section_label("Calculated Results")
            m = {
                "To 1/4 inclusive": 0.125, "Over 1/4 to 1/2 inclusive": 0.1875,
                "Over 1/2 to 3/4 inclusive": 0.25, "Over 3/4 to 1 1/2 inclusive": 0.3125,
                "Over 1 1/2 to 2 1/4 inclusive": 0.375, "Over 2 1/4 to 6 inclusive": 0.5,
                "Over 6": 0.625
            }
            result_card("Minimum Throat of PJP Groove Weld [in]", format_eng_frac_no_unit(m[t_p]), "var(--accent)")
        return

    if mod == "Min. Size of Fillet Welds":
        with col_in:
            section_label("Input Parameters")
            ranges_f = ["To 1/4 inclusive", "Over 1/4 to 1/2 inclusive", "Over 1/2 to 3/4 inclusive", "Over 3/4"]
            t_f = st.selectbox("Thickness of Thinner Part [in]:", ranges_f, index=0, key="tf_f")
            with st.expander("View Reference"):
                render_svg_image("table_j2_4")

        with col_res:
            section_label("Calculated Results")
            m = {"To 1/4 inclusive": 0.125, "Over 1/4 to 1/2 inclusive": 0.1875, "Over 1/2 to 3/4 inclusive": 0.25, "Over 3/4": 0.3125}
            result_card("Minimum Size of Fillet Weld [in]", format_eng_frac_no_unit(m[t_f]), "var(--accent)")
        return

    if mod == "Max. Size of Fillet Welds":
        with col_in:
            section_label("Input Parameters")
            t_m = st.selectbox("Material Thickness Along Edge [in]:", THICKNESS_FRACTIONS_LIMIT, index=0, key="tm_f")
            t_val = THICKNESS_VALUES_LIMIT[t_m]
            with st.expander("View Reference"):
                render_svg_image("note_max_fillet")

        with col_res:
            section_label("Calculated Results")
            res_max = t_val if t_val < 0.25 else t_val - 0.0625
            result_card("Max Size of Fillet Weld [in]", format_eng_frac_no_unit(res_max), "var(--accent)")
        return
