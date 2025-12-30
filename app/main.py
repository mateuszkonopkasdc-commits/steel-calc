import streamlit as st
from app.auth import require_login, logout_button
from app.ui.styles import inject_styles
from app.ui.components import render_sidebar
from app.modules.router import MODULE_MAP, MENU_STRUCTURE

# 1. Konfiguracja strony (musi być pierwsza)
st.set_page_config(page_title="SteelCalc", layout="wide")

# 2. Wstrzyknięcie stylów CSS (z folderu ui)
inject_styles()

# 3. Wymuszenie logowania (z folderu app)
require_login()

# 4. Renderowanie Sidebara (z folderu ui) - teraz on zawiera stopkę!
active_module_name = render_sidebar(MENU_STRUCTURE)

# 5. Routing logic (z folderu modules)
if active_module_name and active_module_name in MODULE_MAP:
    # Jeśli użytkownik coś wybrał -> uruchom odpowiedni moduł
    MODULE_MAP[active_module_name](active_module_name)
else:
    # Jeśli nic nie wybrano -> Ekran startowy (Home)
    st.title("Welcome to SteelCalc 🏗️")
    st.markdown("Select a module from the sidebar to begin calculations.")
    
    # Przycisk wylogowania na ekranie startowym
    st.divider()
    logout_button()