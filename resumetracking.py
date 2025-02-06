from dotenv import load_dotenv

load_dotenv()
import streamlit as st 
import os
from PIL import Image
import pdf2image
import google.generativeai as genai 
import io
import base64

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:    
        ## Convert the pdf to image 
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]
        ##Convert to bytes 

        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() # encode to base64
            }
        ]    
        return pdf_parts
    else:
        raise FileNotFoundError('No file uploaded')
    
## Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ",key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded sucessfully")

submit1 = st.button("Tell me about the resume")
submit2 = st.button("How can I improvise my skill")
submit3 = st.button("What are the keywords that are missing")
submit4 = st.button("Percentage match")

input_prompt1 = """
You are an experienced HR manager with Tech experience in the field of data science , 
full stack web dveopment,back end apis, dev-ops . your task is to review the uploaded 
resume against the job description. Please share your professional evaluation 
highlight strengths and weakneses 
"""

input_prompt3 = """
You are an skilled  ATS(Applicant Tracking System) with Tech experience in the field of data science , 
full stack web dveopment,back end apis, dev-ops . your task is to review the uploaded 
resume against the job description. First output should come as percentage match and second 
output should be missing keywords.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The response is :")
        st.write(response)
    else:
        st.write("Please upload the resume")    
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The response is :")
        st.write(response)
    else:
        st.write("Please upload the resume") 
    
