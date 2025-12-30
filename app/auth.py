import hmac
import streamlit as st


def _get_creds():
    # Dane z Streamlit Cloud → App settings → Secrets
    # STEELCALC_USER = "Mateusz A"
    # STEELCALC_PASS = "123456"
    user = st.secrets.get("STEELCALC_USER", "")
    pwd = st.secrets.get("STEELCALC_PASS", "")
    return str(user), str(pwd)


def require_login() -> bool:
    if st.session_state.get("auth_ok"):
        return True

    exp_user, exp_pass = _get_creds()

    if not exp_user or not exp_pass:
        st.error("❌ Brak danych logowania w Streamlit Secrets.")
        st.stop()

    st.markdown("## 🔐 Logowanie")
    with st.form("login_form"):
        u = st.text_input("Login")
        p = st.text_input("Hasło", type="password")
        ok = st.form_submit_button("Zaloguj")

    if ok:
        if hmac.compare_digest(u, exp_user) and hmac.compare_digest(p, exp_pass):
            st.session_state["auth_ok"] = True
            st.rerun()
        else:
            st.error("❌ Nieprawidłowy login lub hasło.")
            st.stop()

    st.stop()


def logout_button(label: str = "Wyloguj"):
    if st.button(label):
        st.session_state["auth_ok"] = False
        st.rerun()
