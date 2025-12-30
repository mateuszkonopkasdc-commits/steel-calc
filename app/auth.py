import streamlit as st

# ======================
# AUTH (uses Streamlit secrets)
# ======================
# In Streamlit Cloud set secrets:
# STEELCALC_USER="Mateusz"
# STEELCALC_PASS="123456"

def _get_credentials() -> tuple[str, str]:
    user = st.secrets.get("STEELCALC_USER", "Mateusz")
    pwd = st.secrets.get("STEELCALC_PASS", "123456")
    return user, pwd


def logout_button() -> None:
    c1, c2 = st.columns([6, 1])
    with c2:
        if st.button("🚪 Logout"):
            st.session_state["authenticated"] = False
            st.rerun()


def require_login() -> None:
    if st.session_state.get("authenticated", False):
        return

    st.markdown("## 🔐 Login")
    st.caption("Zaloguj się, aby uzyskać dostęp do platformy.")

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Login")
        password = st.text_input("Hasło", type="password")
        submitted = st.form_submit_button("Zaloguj")

    if submitted:
        exp_user, exp_pwd = _get_credentials()
        if username == exp_user and password == exp_pwd:
            st.session_state["authenticated"] = True
            st.success("Zalogowano pomyślnie.")
            st.rerun()
        else:
            st.error("Nieprawidłowy login lub hasło.")

    st.stop()
