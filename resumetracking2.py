
import streamlit as st 
import google.generativeai as genai 
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())   
    return text   

input_prompt = """
You are an skilled  ATS(Applicant Tracking System) with Tech experience in the field of data science , 
full stack web dveopment,back end apis, dev-ops . your task is to review the uploaded 
resume against the job description(JD). First output should come as percentage match and second 
output should be missing keywords.Assign the percentage matching based on JD and missing keywords 
with high accuracy 
resume:{text}
description:{jd} 

I want the response in one single string having the structure 
{{"JD Match": "%","Missing Keywords:[]", "Profile Summary":""}}
"""     

## Streamlit App
st.set_page_config(page_title="SMART ATS Resume Expert")
st.header("ATS Tracking System")
jd = st.text_area("Job Description: ",key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        input_prompt = input_prompt.format(jd=jd, text=text)
        response = get_gemini_response(input_prompt)
        st.subheader("The response in raw json format is :")
        st.write(response)
        data = json.loads(response)
        pretty_json = json.dumps(data, indent=4)
        st.write(pretty_json)



