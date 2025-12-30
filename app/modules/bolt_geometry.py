import streamlit as st
from app.data.aisc_tables import BOLT_GEOM_DATA, HOLE_DATA_STR
from app.ui.components import section_label, result_card
from app.utils.formatting import format_eng_frac_no_unit
from app.utils.images import render_svg_image

def render(mod: str) -> None:
    col_in, col_res = st.columns([1, 1])

    # =========================================================
    # 1. BOLT HOLE DIMENSIONS
    # =========================================================
    if mod == "Bolt Hole Dimensions":
        with col_in:
            section_label("Input Parameters")
            bolt_h = st.selectbox("Select Bolt Diameter [in]:", list(BOLT_GEOM_DATA.keys()), index=0, key="bh_f")
            h_ty_h = st.selectbox("Select Hole Type:", ["Standard", "Oversize", "Short-Slot", "Long-Slot"], index=0, key="ht_f")
            with st.expander("View Reference"):
                render_svg_image("table_j3_3")
        with col_res:
            section_label("Calculated Results")
            res_h = HOLE_DATA_STR.get(bolt_h, {}).get(h_ty_h, "N/A")
            result_card(f"{h_ty_h} Dimension [in]", res_h, "var(--accent)")
        return

    # =========================================================
    # 2. BOLT MIN. EDGE DISTANCE
    # =========================================================
    if mod == "Bolt Min. Edge Distance":
        with col_in:
            section_label("Input Parameters")
            bolt_e = st.selectbox("Select Bolt Diameter [in]:", list(BOLT_GEOM_DATA.keys()), index=0, key="be_f")
            h_ty_e = st.selectbox("Select Hole Type:", ["Standard", "Oversize", "Short-Slot", "Long-Slot"], index=0, key="he_f")
            
            d_e = BOLT_GEOM_DATA[bolt_e]["d"]
            base_e = BOLT_GEOM_DATA[bolt_e]["base_edge"]
            
            # Logika inkrementu dla krawędzi (AISC Table J3.4/J3.5 notes)
            inc_e = 0.0625 if h_ty_e == "Oversize" else 0.125 if h_ty_e == "Short-Slot" else 0.75 * d_e if h_ty_e == "Long-Slot" else 0.0
            
            with st.expander("View Reference"):
                render_svg_image("table_j3_4")
                st.divider()
                render_svg_image("table_j3_5")
        
        with col_res:
            section_label("Calculated Results")
            result_card("Base Minimum Distance [in]", format_eng_frac_no_unit(base_e), "var(--accent)")
            
            if inc_e > 0:
                # --- NOWOŚĆ: Ostrzeżenie dla Long-Slot (jak w Spacing) ---
                if h_ty_e == "Long-Slot":
                     st.warning("⚠️ Warning: Large edge distance increment required due to Long-Slot geometry.")

                result_card("Values of Edge Distance Increment [in]", f"+ {format_eng_frac_no_unit(inc_e)}", "var(--accent)")
                result_card("Total Minimum Distance [in]", format_eng_frac_no_unit(base_e + inc_e), "var(--ok)")
        return

    # =========================================================
    # 3. BOLT MIN. SPACING
    # =========================================================
    if mod == "Bolt Min. Spacing":
        with col_in:
            section_label("Input Parameters")
            bolt_s = st.selectbox("Select Bolt Diameter [in]:", list(BOLT_GEOM_DATA.keys()), index=0, key="bs_f")
            h_ty_s = st.selectbox("Select Hole Type:", ["Standard", "Oversize", "Short-Slot", "Long-Slot"], index=0, key="hts_f")
            
            d_s = BOLT_GEOM_DATA[bolt_s]["d"]
            h_dim = BOLT_GEOM_DATA[bolt_s]["hole"][h_ty_s]
            
            # Standardowy rozstaw 2.66d (8/3 d)
            s_base = (8/3) * d_s
            
            # Sprawdzenie warunku Clear Distance >= d
            clear_dist = s_base - h_dim
            is_ok = (clear_dist >= d_s)
            
            # Obliczenie wymaganego zwiększenia (zawsze liczymy, jeśli not ok)
            increase = (h_dim + d_s - s_base) if not is_ok else 0.0
            
            with st.expander("View Reference"):
                render_svg_image("table_j3_3_text")
                st.info(
                    f"**Note:**\n"
                    f"1. The clear distance between bolt holes shall not be less than the bolt diameter **d**.\n"
                    f"2. The preferred distance between centers of standard holes is **3d** ({format_eng_frac_no_unit(3*d_s)} in)."
                )
        
        with col_res:
            section_label("Calculated Results")
            result_card("Standard Minimum Spacing [in]", format_eng_frac_no_unit(s_base), "var(--accent)")
            
            # Status Check
            result_card("Clear Distance Check", "OK" if is_ok else "NOT OK", "var(--ok)" if is_ok else "var(--accent)")
            
            if not is_ok:
                # Ostrzeżenie dla Spacing (już wdrożone wcześniej)
                if h_ty_s == "Long-Slot":
                     st.warning("⚠️ Warning: Large spacing increment required due to Long-Slot geometry.")
                
                result_card("Values of Spacing Distance Increment [in]", f"+ {format_eng_frac_no_unit(increase)}", "var(--accent)")
                result_card("Total Minimum Spacing [in]", format_eng_frac_no_unit(s_base + increase), "var(--ok)")
        return