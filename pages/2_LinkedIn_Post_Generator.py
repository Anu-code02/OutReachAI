import sys
import os
import streamlit as st

st.set_page_config(layout="wide", page_title="LinkedIn Post Generator", page_icon="✨", initial_sidebar_state="collapsed")

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

current_dir = os.path.dirname(os.path.abspath(__file__))
linkedin_dir = os.path.join(current_dir, "..", "Linkedin Post generator")
sys.path.append(os.path.abspath(linkedin_dir))

# Back button
if st.button("← Back to Home"):
    st.switch_page("app.py")

import importlib.util
spec = importlib.util.spec_from_file_location("linkedin_main", os.path.join(linkedin_dir, "main.py"))
linkedin_main = importlib.util.module_from_spec(spec)
sys.modules["linkedin_main"] = linkedin_main
spec.loader.exec_module(linkedin_main)

# The main file in Linkedin Post Generator uses `st.set_page_config` within its `main()` loop.
# We shouldn't call `main()` since it defines `st.set_page_config` which will throw an error if called twice.
# Let's extract the UI parts or monkey-patch `st.set_page_config` before calling!

original_set_page_config = st.set_page_config
st.set_page_config = lambda *args, **kwargs: None

try:
    linkedin_main.main()
finally:
    st.set_page_config = original_set_page_config
