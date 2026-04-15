import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        # Prefer environment variable, fallback to Streamlit secrets on Cloud
        api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set. Set env var or Streamlit secret.")
        self.llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )#json prompt banaye h
        chain_extract = prompt_extract | self.llm 
        #propmt ko llm se jodna(pipeline)
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        #above chain ko run karega with the page data of the career page that is cleaned text
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            
            ### INSTRUCTION:
            You are Abhijeet Kushwaha TPR at HBTU Kanpur and your role is to mail the company’s HR for conducting the On Campus Drive 
            for MCA based on the job description mentioned above and describing the capabilities of HBTU MCA Students to fulfill 
            their requirement. Ensure that the invitation letter is highly professional, formal, and contains NO emojis. Try to keep the sentence length short ,accurate and clear. If a sentence is getting too long, make a new line.
            Also add the most relevant ones from the following links to showcase HBTU MCA's portfolio: {link_list} 
            Remember you are Placement Coordinator, HBTU Kanpur. Mention this in the signature of the mail.
            Placement Coordinator, HBTU Kanpur 
            placement@hbtu.ac.in 
            +91-9xxxxxxxxx 
            Do not provide a preamble. 

            ### EMAIL (NO PREAMBLE):

            """ 

        )
        #email prompt banaya h
        chain_email = prompt_email | self.llm
        #prompt ko llm se jodna(pipeline)
        res = chain_email.invoke({"job_description": str(job), "link_list": 
        links})
        #above chain ko run karega with the job description and the links
        #yahan pe job description me job ki saari details hongi jo humlog career page se extract karenge and links me portfolio ke links honge jo humlog invitation mail me add karenge based on the semantic searching of "job skills" and "portfolio skills"
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
#Ensures code runs only when file is executed directly, not imported.