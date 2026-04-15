import os
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("✉️ Campus Invitation Mail Generator")
    st.write("Extract job postings from a URL or paste the job description directly.")
    
    input_method = st.radio("Choose Input Method:", ("URL", "Paste Job Description"))
    
    data = ""
    if input_method == "URL":
        url_input = st.text_input("Enter a URL:", value="https://heizen.work/careers/software-engineer")
    else:
        text_input = st.text_area("Paste Job Description:", height=200)

    submit_button = st.button("Submit")

    if submit_button:
        try:
            if input_method == "URL":
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
            else:
                data = clean_text(text_input)
                
            if not data.strip():
                st.warning("No data found to process. Please check the URL or the text pasted.")
                return

            #data me cleaned text aa jayega from the career page
            portfolio.load_portfolio()
            #ye load karega skills & links into ChromaDB.
            jobs = llm.extract_jobs(data)
            #ye json format me extract karega jobs from the cleaned text that is data variable
            #yahan jobs me information json format me h that is key value form me aur uske andar various keys h like job description,skills required,experience ,etc.
            for job in jobs:
                skills = job.get('skills', [])
                # Ensure skills is a list of strings
                if isinstance(skills, str):
                    skills = [skills]
                elif not isinstance(skills, list):
                    skills = []
                
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
            #ab har job ke liye required skills  , portfolio se links me sementic search,then llm se email write krwana h .aur use streamlit ke help se ui me email ko bhej dena h
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    # Configure page first so errors render nicely in Streamlit Cloud
    st.set_page_config(layout="wide", page_title="Campus Mail Generator", page_icon="📧")

    # Ensure GROQ key is available (env or Streamlit Cloud secrets)
    api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    if not api_key:
        st.error(
            "GROQ_API_KEY is not configured.\n\n"
            "Set it locally in app/.env or on Streamlit Cloud via Settings → Secrets with key GROQ_API_KEY."
        )
        st.info("Once the secret is set, rerun the app from the top-right 'Rerun' button.")
        st.stop()

    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)


