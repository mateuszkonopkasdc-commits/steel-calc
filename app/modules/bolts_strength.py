import streamlit as st
from app.data.aisc_tables import BOLT_AREAS, NOMINAL_BOLT_STRESS
from app.ui.components import section_label, input_info, result_card

def render(mod: str) -> None:
    col_in, col_res = st.columns([1, 1])

    with col_in:
        section_label("Input Parameters")

        method = st.radio("Select Design Method:", ["LRFD", "ASD"], index=0, key="meth_bolt")
        bolt_d = st.selectbox("Select Bolt Diameter [in]:", list(BOLT_AREAS.keys()), index=0, key="d_bolt_s")
        bolt_g = st.selectbox("Select Bolt Group:", list(NOMINAL_BOLT_STRESS.keys()), index=0, key="g_bolt_s")

        is_unavail = ("Group C" in bolt_g and bolt_d in ["5/8", "3/4", "7/8", "1 3/8", "1 1/2"])
        area_val = BOLT_AREAS[bolt_d]

        if mod == "Shear Strength of Bolts":
            t_cond = "N" if "A307" in bolt_g else st.radio(
                "Thread Condition:", ["N (Included)", "X (Excluded)"], index=0, key="t_b_s"
            )[0]
            fn_val = NOMINAL_BOLT_STRESS[bolt_g][f"Shear_{t_cond}"]
            fn_label_html = "Nominal Shear Stress: F<sub>nv</sub> [ksi]"
        else:
            fn_val = NOMINAL_BOLT_STRESS[bolt_g]["Tension"]
            fn_label_html = "Nominal Tensile Stress: F<sub>nt</sub> [ksi]"

        PHI = "&Phi;"        # Φ (LRFD)
        OMEGA = "&Omega;"    # Ω (ASD)

        if method == "LRFD":
            coeff_label_html = f"Resistance Factor {PHI}"
            coeff_val = "0.75"
        else:
            coeff_label_html = f"Safety Factor {OMEGA}"
            coeff_val = "2.00"

        input_info("Nominal Bolt Area: A<sub>b</sub> [in²]", f"{area_val}")
        input_info(fn_label_html, f"{fn_val}")
        input_info(coeff_label_html, coeff_val)

        n_planes = 1
        if mod == "Shear Strength of Bolts":
            planes_opt = st.radio("Shear Planes:", ["Single Shear (S)", "Double Shear (D)"], index=0, key="p_b_s")
            n_planes = 1 if "Single" in planes_opt else 2

    with col_res:
        section_label("Calculated Results")

        if is_unavail:
            result_card("Information:", "Selected grade is unavailable for this diameter", "var(--accent)")
            return

        rn = fn_val * area_val * n_planes
        final = rn * 0.75 if method == "LRFD" else rn / 2.0
        strength_type = "Shear" if "Shear" in mod else "Tensile"

        if method == "LRFD":
            label = f"The Design {strength_type} Strength {PHI}R<sub>n</sub> [kips]"
        else:
            label = f"The Available {strength_type} Strength R<sub>n</sub>/{OMEGA} [kips]"

        result_card(label, f"{final:.2f}", "var(--ok)")
