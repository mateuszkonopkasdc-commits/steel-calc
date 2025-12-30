import streamlit as st
from app.ui.components import section_label, result_card

def render(_: str) -> None:
    col_in, col_res = st.columns([1, 1])

    with col_in:
        section_label("Input Parameters")
        direction = st.radio("Select Direction:", ["Imperial to Metric", "Metric to Imperial"], key="dir_u_f")
        u_type = st.selectbox("Select Unit Type:", ["Length", "Area", "Force", "Stress / Pressure", "Weight per Length"], key="u_type_f")

        units_map = {
            "Length": (["in", "ft"], ["mm", "cm", "m"]),
            "Area": (["in²", "ft²"], ["mm²", "cm²", "m²"]),
            "Force": (["kips", "lbs"], ["kN", "N"]),
            "Stress / Pressure": (["ksi", "psi"], ["MPa", "kPa", "Pa"]),
            "Weight per Length": (["lb/in", "lb/ft", "kip/in", "kip/ft", "klf"], ["N/mm", "N/cm", "N/m", "kN/mm", "kN/cm", "kN/m"])
        }

        c1, c2 = st.columns(2)
        imp_l, met_l = units_map[u_type]
        from_opts, to_opts = (imp_l, met_l) if direction == "Imperial to Metric" else (met_l, imp_l)

        in_u = c1.selectbox("From:", from_opts, key="f_u_f")
        out_u = c2.selectbox("To:", to_opts, key="t_u_f")
        val_in = st.number_input(f"Value [{in_u}]:", value=1.0, step=0.1, key="v_u_f")

    with col_res:
        section_label("Calculated Results")
        factors = {
            "in": 0.0254, "ft": 0.3048, "mm": 0.001, "cm": 0.01, "m": 1.0,
            "in²": 0.00064516, "ft²": 0.092903, "mm²": 0.000001, "cm²": 0.0001, "m²": 1.0,
            "kips": 4448.22, "lbs": 4.44822, "kN": 1000.0, "N": 1.0,
            "ksi": 6894757.29, "psi": 6894.76, "MPa": 1000000.0, "kPa": 1000.0, "Pa": 1.0,
            "lb/in": 175.127, "lb/ft": 14.5939, "kip/in": 175127.0, "kip/ft": 14593.9, "klf": 14593.9,
            "N/mm": 1000.0, "N/cm": 100.0, "N/m": 1.0,
            "kN/mm": 1000000.0, "kN/cm": 100000.0, "kN/m": 1000.0
        }
        res_val = (val_in * factors[in_u]) / factors[out_u]
        result_card(f"Converted Value [{out_u}]", f"{res_val:.4f}", "var(--accent)")
