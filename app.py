import streamlit as st

st.set_page_config(
    page_title="OutReachAI",
    page_icon="👋",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
        /* Make background visible by making the main block transparent */
        .stMainBlockContainer { background: transparent; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Welcome to OutReachAI 👋")
st.subheader("A platform to connect and network.")

st.write("OutReachAI helps you streamline your outreach process. Please select what you want to create today:")

col1, col2 = st.columns(2)

with col1:
    st.info("✉️ **Cold Mail Generator**\n\nGenerate customized cold emails for job applications based on a job description URL and your portfolio.")
    if st.button("Go to Cold Mail Generator", use_container_width=True):
        st.switch_page("pages/1_Cold_Mail_Generator.py")

with col2:
    st.info("✨ **LinkedIn Post Generator**\n\nCraft professional, engaging LinkedIn posts tailored to your tone, format, and language preferences.")
    if st.button("Go to LinkedIn Post Gen", use_container_width=True):
        st.switch_page("pages/2_LinkedIn_Post_Generator.py")
