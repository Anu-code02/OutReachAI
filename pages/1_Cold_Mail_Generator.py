import sys
import os
import streamlit as st

st.set_page_config(layout="wide", page_title="Campus Mail Generator", page_icon="✉️", initial_sidebar_state="collapsed")

# Hide the sidebar completely
st.markdown(
    """
    <style>
        [data-testid="collapsedControl"] { display: none; }
        section[data-testid="stSidebar"] { display: none; }
        .stApp, [data-testid="stAppViewContainer"] {
            background: #ffd6e7;
            background: radial-gradient(circle, rgba(255, 214, 231, 1) 0%, rgba(176, 193, 235, 1) 100%);
        }
        .stMainBlockContainer { background: transparent; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Append the correct directory to sys.path so modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
cold_mail_dir = os.path.join(current_dir, "..", "Cold mail generator", "app")
sys.path.append(os.path.abspath(cold_mail_dir))

import importlib.util
spec = importlib.util.spec_from_file_location("cold_mail_main", os.path.join(cold_mail_dir, "main.py"))
cold_mail_main = importlib.util.module_from_spec(spec)
sys.modules["cold_mail_main"] = cold_mail_main
spec.loader.exec_module(cold_mail_main)

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error(
        "GROQ_API_KEY is not configured.\n\n"
        "Set it locally in app/.env or on Streamlit Cloud via Settings → Secrets with key GROQ_API_KEY."
    )
    st.info("Once the secret is set, rerun the app from the top-right 'Rerun' button.")
    st.stop()

# Go back to home button
if st.button("← Back to Home"):
    st.switch_page("app.py")

chain = Chain()
portfolio = Portfolio()

# Avoid multiple `st.set_page_config` exceptions if any inner functions call it
original_set_page_config = st.set_page_config
st.set_page_config = lambda *args, **kwargs: None
try:
    cold_mail_main.create_streamlit_app(chain, portfolio, clean_text)
finally:
    st.set_page_config = original_set_page_config
