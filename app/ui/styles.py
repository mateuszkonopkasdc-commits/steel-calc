import streamlit as st

def inject_styles() -> None:
    st.markdown("""
    <style>
    :root{
      --accent: #ff4b4b;
      --ok: #22c55e;
    }

    [data-testid="stSidebar"] { min-width: 290px; background-color: #0e1117; }
    [data-testid="stAppViewBlockContainer"] { padding: 0.35rem 1.6rem; }

    div.stButton > button {
      width: 100%;
      border: 1px solid #464855;
      background-color: #1e2130;
      color: #ffffff;
      text-align: left;
      padding: 6px;
      font-size: 0.82rem;
    }

    .section-label {
      font-size: 1.05rem !important;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 2px;
      text-transform: uppercase;
      border-bottom: 2px solid var(--accent);
      display: inline-block;
    }

    .ref-text {
      font-size: 0.9rem !important;
      color: #a0a4b5;
      margin-top: -8px;
      margin-bottom: 5px;
      font-style: italic;
    }

    .result-card {
      background-color: #1e2130;
      border-radius: 12px;
      padding: 10px 12px;
      border-left: 3.5px solid var(--accent);
      box-shadow: 0 1px 3px rgba(0,0,0,0.3);
      margin-bottom: 6px;
    }

    .fraction-val {
      font-family: 'Roboto Mono', monospace;
      font-size: 1.15rem;
      font-weight: 700;
      color: #ffffff;
    }

    .label-text {
      color: var(--accent);
      font-weight: 750;
      font-size: 0.92rem;
      margin-bottom: -2px;
    }

    hr {
      margin-top: 0.20rem !important;
      margin-bottom: 0.20rem !important;
    }

    .input-info-label{
      font-family: "Source Sans Pro", sans-serif;
      font-size: 0.92rem;
      font-weight: 650;
      color: rgba(250, 250, 250, 0.85);
      margin-top: 8px;
      margin-bottom: 1px;
      line-height: 1.15;
    }

    .input-info-value{
      font-family: 'Roboto Mono', monospace;
      font-size: 1.02rem;
      font-weight: 700;
      color: rgba(250, 250, 250, 0.95);
      margin-top: 0px;
      margin-bottom: 6px;
      line-height: 1.15;
    }

    .v-line { border-left: 1px solid #464855; height: 40px; margin: 0 20px; }
    </style>
    """, unsafe_allow_html=True)
