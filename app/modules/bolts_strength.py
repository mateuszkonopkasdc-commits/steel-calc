import streamlit as st
import pandas as pd
import math
from fractions import Fraction

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="US Structural Bolt Platform", layout="wide")

# --- 2. FUNKCJE POMOCNICZE ---
def to_fraction_str(val):
    """Konwertuje float na string w formacie ułamka (dokładność 1/16 cala)."""
    if val is None:
        return "-"
    if isinstance(val, int) or (isinstance(val, float) and val.is_integer()):
        return str(int(val))
    
    # Precyzja inżynierska do 1/16 cala
    f = Fraction(val).limit_denominator(16)
    
    # Obsługa liczb mieszanych (np. 1 1/2)
    if f.numerator > f.denominator:
        whole = f.numerator // f.denominator
        rem_num = f.numerator % f.denominator
        if rem_num == 0:
            return str(whole)
        return f"{whole} {rem_num}/{f.denominator}"
    
    return f"{f.numerator}/{f.denominator}"

# --- 3. DANE NORMOWE (AISC Table J3.2 - FULL DATASET) ---
# Zakaz spłaszczania tabeli. Wszystkie grupy i typy gwintów.
data_bolts = {
    "ASTM Designation": [
        "A307", 
        "A325 / F1852 (Group A)", "A325 / F1852 (Group A)", 
        "A490 / F2280 (Group B)", "A490 / F2280 (Group B)",
        "F3043 (Group C)", "F3043 (Group C)",
        "F3111 (Group C)", "F3111 (Group C)"
    ],
    "Thread Condition": [
        "N/A", 
        "Excluded (X)", "Included (N)", 
        "Excluded (X)", "Included (N)",
        "Excluded (X)", "Included (N)",
        "Excluded (X)", "Included (N)"
    ],
    "Fnt [ksi] (Tension)": [
        45, 
        90, 90, 
        113, 113,
        150, 150,
        150, 150
    ],
    "Fnv [ksi] (Shear)": [
        27, 
        68, 54, 
        84, 68,
        113, 90,
        113, 90
    ]
}

df_bolts = pd.DataFrame(data_bolts)

# --- 4. SIDEBAR - GLOBAL SETTINGS ---
st.sidebar.header("Global Settings")

# Wybór śruby
bolt_idx = st.sidebar.selectbox(
    "Select Bolt Designation & Thread Condition", 
    range(len(df_bolts)), 
    format_func=lambda x: f"{df_bolts.iloc[x]['ASTM Designation']} - Threads {df_bolts.iloc[x]['Thread Condition']}"
)
selected_bolt = df_bolts.iloc[bolt_idx]

# Parametry wybranej śruby
Fnt = selected_bolt["Fnt [ksi] (Tension)"]
Fnv = selected_bolt["Fnv [ksi] (Shear)"]

# Średnica
diameter = st.sidebar.selectbox("Bolt Diameter [in]", [0.5, 0.625, 0.75, 0.875, 1.0, 1.125, 1.25, 1.375, 1.5])
area_bolt = math.pi * (diameter/2)**2

st.sidebar.markdown("---")

# Metoda obliczeń
method = st.sidebar.radio("Design Method", ["LRFD", "ASD"])
phi = 0.75
omega = 2.00

# --- 5. ZAKŁADKI (MODULE LOGIC) ---
# Resetowanie stanu zakładek przy zmianie nie jest wymagane tutaj, 
# ale logika wewnątrz zakładek zapewnia odświeżanie obliczeń.
tab1, tab2, tab3 = st.tabs(["Shear Strength of Bolts", "Combined Shear + Tension", "Spacing & Geometry"])

# === TAB 1: SHEAR STRENGTH ===
with tab1:
    st.markdown("### Shear Strength of Bolts (AISC J3.6)")
    st.info("Calculation for bolts subject to Single Shear plane.")
    
    # Nominal Strength
    Rn_shear = Fnv * area_bolt
    
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**Bolt Type:** {selected_bolt['ASTM Designation']}")
        st.write(f"**Diameter ($d_b$):** {to_fraction_str(diameter)} in")
        st.write(f"**Area ($A_b$):** {round(area_bolt, 4)} in²")
        st.write(f"**Nominal Shear Stress ($F_{{nv}}$):** {Fnv} ksi")
    
    with c2:
        st.markdown(f"**Nominal Strength ($R_n$):** {to_fraction_str(Rn_shear) if Rn_shear.is_integer() else round(Rn_shear, 2)} kips")
        
        if method == "LRFD":
            design_val = phi * Rn_shear
            st.success(f"**Design Strength ($\phi R_n$):** {to_fraction_str(design_val) if design_val.is_integer() else round(design_val, 2)} kips")
        else:
            allow_val = Rn_shear / omega
            st.success(f"**Allowable Strength ($R_n / \Omega$):** {to_fraction_str(allow_val) if allow_val.is_integer() else round(allow_val, 2)} kips")

# === TAB 2: COMBINED SHEAR + TENSION ===
with tab2:
    st.markdown("### Combined Tension and Shear (AISC J3.7)")
    st.caption("Verification of bolts subject to simultaneous shear and tension forces.")
    
    # Input Forces
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        req_shear = st.number_input(f"Required Shear Force ({'Vu' if method=='LRFD' else 'Va'}) [kips]", min_value=0.0, value=5.0, step=0.5)
    with col_in2:
        req_tension = st.number_input(f"Required Tension Force ({'Tu' if method=='LRFD' else 'Ta'}) [kips]", min_value=0.0, value=10.0, step=0.5)
    
    st.markdown("---")
    
    # 1. Obliczenie naprężenia ścinającego
    frv = req_shear / area_bolt
    
    # 2. Limit ścinania (Check if fail solely on shear)
    shear_limit_stress = (phi * Fnv) if method == "LRFD" else (Fnv / omega)
    
    if frv > shear_limit_stress:
        st.error(f"❌ **FAIL:** Shear stress $f_{{rv}}$ ({round(frv, 2)} ksi) exceeds capacity ({round(shear_limit_stress, 2)} ksi).")
    else:
        # 3. Obliczenie zredukowanego naprężenia rozciągającego F'nt
        # LRFD: Eq J3-3a, ASD: Eq J3-3b
        if method == "LRFD":
            f_prime_nt_calc = 1.3 * Fnt - (Fnt / (phi * Fnv)) * frv
        else:
            f_prime_nt_calc = 1.3 * Fnt - ((omega * Fnt) / Fnv) * frv
            
        # Ograniczenie: F'nt <= Fnt
        f_prime_nt = min(f_prime_nt_calc, float(Fnt))
        
        # Wyświetlanie wyników interakcji
        res_c1, res_c2 = st.columns(2)
        with res_c1:
            st.markdown(f"**Required Shear Stress ($f_{{rv}}$):** {round(frv, 2)} ksi")
            st.markdown(f"**Modified Tension Stress ($F'_{{nt}}$):** {round(f_prime_nt, 2)} ksi")
            
        with res_c2:
            # Final Capacity Check
            Rn_comb = f_prime_nt * area_bolt
            
            if method == "LRFD":
                capacity = phi * Rn_comb
                label_cap = "$\phi R_n$"
            else:
                capacity = Rn_comb / omega
                label_cap = "$R_n / \Omega$"
            
            # Unikamy dzielenia przez zero
            if capacity <= 0:
                st.error("❌ Capacity is 0 (High Shear)")
                uc = 999.0
            else:
                uc = req_tension / capacity
                
            st.metric(f"Tension Capacity ({label_cap})", f"{round(capacity, 2)} kips")
            st.metric("Interaction Ratio (D/C)", f"{round(uc, 3)}")
            
        if uc <= 1.0 and capacity > 0:
            st.success("✅ **Interaction OK**")
        else:
            st.error("❌ **Interaction FAIL**")

# === TAB 3: SPACING & GEOMETRY ===
with tab3:
    st.markdown("### Geometry Checks (AISC J3.3)")
    
    # Input Geometrii
    col_geo_in1, col_geo_in2 = st.columns(2)
    with col_geo_in1:
        # Domyślnie resetujemy wybór przy starcie (standard behavior)
        hole_type = st.selectbox("Hole Type", ["Standard (STD)", "Oversized (OVS)", "Short Slot (SSL)", "Long Slot (LSL)"])
    with col_geo_in2:
        edge_dist = st.number_input("Actual Edge Distance ($L_e$) [in]", min_value=0.0, value=1.5, step=0.125)

    st.markdown("#### Values of Spacing Distance Increment [in]")
    
    # Logika AISC
    min_spacing = 2.66 * diameter # 2 2/3 d
    pref_spacing = 3.0 * diameter
    
    # Minimalna odległość od krawędzi (uproszczona Tabela J3.4 dla przykładu)
    if diameter <= 0.5: min_edge_req = 0.75
    elif diameter <= 0.625: min_edge_req = 0.875
    elif diameter <= 0.75: min_edge_req = 1.0
    elif diameter <= 0.875: min_edge_req = 1.125
    elif diameter <= 1.0: min_edge_req = 1.25
    elif diameter <= 1.125: min_edge_req = 1.5
    elif diameter <= 1.25: min_edge_req = 1.625
    else: min_edge_req = 1.25 * diameter # Generic fallback
    
    # Wyświetlanie wyników
    g1, g2 = st.columns(2)
    with g1:
        st.write(f"**Preferred Min Spacing (3d):** {to_fraction_str(pref_spacing)} in")
        st.write(f"**Min Spacing (2 2/3 d):** {to_fraction_str(min_spacing)} in")
    
    with g2:
        st.write(f"**Min Edge Distance (Table J3.4):** {to_fraction_str(min_edge_req)} in")
        
        # Check logic
        if edge_dist >= min_edge_req:
            st.success("✅ Edge Distance OK")
        else:
            st.error("❌ Edge Distance too small")
            
    # Logika dla Long Slots (Krytyczna zasada)
    if "Long Slot" in hole_type:
        st.info("ℹ️ **Long Slots:** If geometry checks fail or are tight, consider increasing spacing perpendicular to the slot axis.")

# --- FOOTER ---
st.markdown("---")
st.markdown("Developed by: 👨‍💻 US Structural Platform Dev")
st.caption("Legal Disclaimer:\nThis tool is for educational purposes only. Verify all results with a licensed P.E.")