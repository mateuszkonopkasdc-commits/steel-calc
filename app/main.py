import streamlit as st
import sys
import os

# Dodanie ścieżki głównej do sys.path, aby uniknąć problemów z importami na Cloud
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Próba importu z obsługą różnych środowisk (lokalne vs cloud)
try:
    from auth import require_login, logout_button
except ImportError:
    from app.auth import require_login, logout_button

from modules import bolts_strength

def main():
    st.set_page_config(page_title="US Structural Platform", layout="wide")

    # Logika autoryzacji
    if not require_login():
        st.stop()

    st.sidebar.title("Navigation")
    logout_button()
    
    menu = ["Welcome Page", "Shear Strength of Bolts", "Combined Shear + Tension", "Spacing & Geometry"]
    choice = st.sidebar.selectbox("Select Module", menu)

    if choice == "Welcome Page":
        st.title("Welcome to US Structural Platform")
        st.write("Select a module from the sidebar to begin calculations.")
    
    elif choice in ["Shear Strength of Bolts", "Combined Shear + Tension", "Spacing & Geometry"]:
        # Wywołanie modułu obliczeniowego
        bolts_strength.run_module(choice)

    # STOPKA (Zgodnie z wytycznymi)
    st.sidebar.markdown("---")
    st.sidebar.markdown("Developed by: 👨‍💻 [Twoje Imię]")
    st.sidebar.caption("Legal Disclaimer:\nThis tool is for educational purposes only. Verify all results with a licensed P.E.")

if __name__ == "__main__":
    main()