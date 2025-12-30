import streamlit as st
from fractions import Fraction

from app.data.aisc_tables import GAGE_DATA, ASTM_DETAILED_DATA, SHAPE_SERIES_LIST
from app.ui.components import section_label, result_card

# --- pomocnicze: sort "1 1/4" itd. ---
def eng_to_float(val_str: str) -> float:
    try:
        s = str(val_str).strip()
        if " " in s:
            a, b = s.split(" ", 1)
            return float(a) + float(Fraction(b))
        return float(Fraction(s))
    except Exception:
        return 0.0

# --- subskrypty g1 -> g₁ ---
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
def format_gage_key(k: str) -> str:
    k = str(k)
    if k.startswith("g") and len(k) > 1 and k[1:].isdigit():
        return "g" + k[1:].translate(SUB)
    return k

def render(mod: str) -> None:
    col_in, col_res = st.columns([1, 1])

    # ========= ANGLE WORKABLE GAGES =========
    if mod == "Angle Workable Gages":
        with col_in:
            section_label("Input Parameters")
            leg_opts = sorted(list(GAGE_DATA.keys()), key=eng_to_float)
            leg_sel = st.selectbox("Select Angle Leg Length [in]:", leg_opts, index=0, key="leg_a_f")

            # referencja (jeśli masz obrazek)
            with st.expander("View Reference"):
                try:
                    from app.utils.images import render_image
                    render_image("angle_gage", width="180px")
                except Exception:
                    st.info("Reference image not found (angle_gage).")

        with col_res:
            section_label("Calculated Results")
            res_g = GAGE_DATA[leg_sel]

            # stabilna kolejność: g, g1, g2...
            def g_sort_key(x: str):
                x = str(x)
                if x == "g":
                    return 0
                if x.startswith("g") and x[1:].isdigit():
                    return int(x[1:])
                return 999

            for k in sorted(res_g.keys(), key=g_sort_key):
                kk = format_gage_key(k)
                result_card(f"Gage {kk}: [in]", f"{res_g[k]}")

        return

    # ========= ASTM MATERIAL DATA =========
    if mod == "ASTM Material Data":
        with col_in:
            section_label("Input Parameters")
            sh_astm = st.selectbox("Select Shape Series:", SHAPE_SERIES_LIST, index=0, key="sh_astm_f")
            avail = sorted([n for n, d in ASTM_DETAILED_DATA["ASTM Designation"].items() if sh_astm in d["Shapes"]])
            astm_sel = st.selectbox("Select ASTM Designation:", avail, index=0, key="astm_sel_f")

            with st.expander("View Reference"):
                try:
                    from app.utils.images import render_image
                    render_image("table_2_4")
                except Exception:
                    st.info("Reference image not found (table_2_4).")

        with col_res:
            section_label("Calculated Results")
            d_astm = ASTM_DETAILED_DATA["ASTM Designation"][astm_sel]

            fy_res = "42" if astm_sel == "A500 Gr. B" and sh_astm == "HSS Round" else "46" if astm_sel == "A500 Gr. B" else d_astm.get("Fy", "N/A")
            if astm_sel == "A500 Gr. C":
                fy_res = "46" if sh_astm == "HSS Round" else "50"

            result_card("Yield Stress: Fy [ksi]", fy_res)
            result_card("Tensile Stress: Fu [ksi]", d_astm.get("Fu", "N/A"))

        return

    # fallback
    st.info(f"Module '{mod}' is not handled by materials.py")
