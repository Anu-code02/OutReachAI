try:
    import streamlit as st  # type: ignore
except Exception:
    st = None

from few_shot import FewShotPosts
from post_generator import generate_post


# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]
tone_options = ["Professional", "Inspirational", "Humorous", "Casual", "Data-Driven", "Storytelling", "Controversial/Spicy"]
format_options = ["Standard paragraphs", "Bulleted lists", "Short choppy sentences"]

# Main app layout (Streamlit)
def main():
    if st is None:
        raise RuntimeError("streamlit is not available")

    st.set_page_config(page_title="LinkedIn Post Generator", page_icon="✨", layout="centered")

    # Custom CSS for a modern light theme look
    st.markdown("""
        <style>
        .stButton>button {
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }
        div[data-testid="stExpander"] {
            border: none;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            border-radius: 8px;
            margin-bottom: 12px;
        }
        div[data-testid="stTextArea"] textarea {
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        div[data-testid="stSelectbox"] div[role="button"] {
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #0a66c2;
            margin-bottom: -0.5rem;
        }
        .sub-header {
            font-size: 1.1rem;
            color: #555555;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state for history
    if "history" not in st.session_state:
        st.session_state.history = []

    st.markdown('<p class="main-header">✨ LinkedIn Post Generator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Craft professional, engaging content effortlessly.</p>', unsafe_allow_html=True)

    st.divider()

    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts()
    tags = fs.get_tags()
    with col1:
        # Dropdown for Topic (Tags)
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        # Dropdown for Length
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        # Dropdown for Language
        selected_language = st.selectbox("Language", options=language_options)
        
    # Second row of columns for new features
    col4, col5 = st.columns(2)
    with col4:
        selected_tone = st.selectbox("Tone", options=tone_options)
    with col5:
        selected_format = st.selectbox("Formatting", options=format_options)

    st.markdown('<br>', unsafe_allow_html=True)
    
    # Optional custom prompt input
    custom_prompt = st.text_area("Custom prompt (optional)", value="", height=120, placeholder="E.g. Focus on my recent achievement in data structures...")

    # Generate Button
    col_btn, empty_col = st.columns([1, 4])
    with col_btn:
        generate_clicked = st.button("🚀 Generate Post", use_container_width=True)

    if generate_clicked:
        with st.spinner("Generating your post..."):
            post = generate_post(selected_length, selected_language, selected_tag, selected_tone, selected_format, custom_prompt=custom_prompt)
            # Add strictly to the very top of history
            st.session_state.history.insert(0, {
                "tag": selected_tag,
                "tone": selected_tone,
                "format": selected_format,
                "post": post
            })

    # Render History (Top item is newest)
    if st.session_state.history:
        st.divider()
        colA, colB = st.columns([4, 1])
        with colA:
            st.markdown("### 🗂️ Your Generated Posts")
        with colB:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.history = []
                st.rerun()
                
        for i, item in enumerate(st.session_state.history):
            # The newest item is always expanded; older items are collapsed
            with st.expander(f"📝 Post {len(st.session_state.history) - i}: {item['tag']} ({item['tone']} - {item['format']})", expanded=(i == 0)):
                # st.code provides an automatic copy-to-clipboard button in Streamlit
                st.code(item["post"], language="markdown")


def cli_fallback():
    """Run a simple CLI fallback when streamlit isn't installed."""
    from run_local import main as run_local_main

    print("Streamlit not installed — running CLI fallback.")
    run_local_main()


# Run the app or fallback to CLI
if __name__ == "__main__":
    if st is None:
        cli_fallback()
    else:
        main()
