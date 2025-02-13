import streamlit as st 
import google.generativeai as genai 
import os
from dotenv import load_dotenv
import json

from PIL import Image


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt,image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
      # Read the file into bytes 
      bytes_data = uploaded_file.getvalue()

      image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": bytes_data 
                }
            ]    
      return image_parts
    else:
        raise FileNotFoundError('No file uploaded')
    
st.set_page_config("AI Large image model  nutritionist App")
st.header("AI Large image model  nutritionist App")    

uploaded_file = st.file_uploader("Choose an image...",type=["jpeg","jpg","png"])

if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(image,caption="Uploaded image",use_container_width=True)


submit = st.button("Tell me about the total calories")

input_prompt = """
You are an expert nutritionist where you need to see the food items from the image 
 and calculate the total calories, also provide the details of every food item 
 with calories intake in below format
    1. Item 1 - No of Calories
    2. Item 2 - No of Calories

  Finally you can also mention the food is healthy or not and also percentage split 
  ratio of the carbohydrates,fats,fibers,protien,sugar  and other important  things 
  required in our diet. 
"""
if submit:
   image_data = input_image_setup(uploaded_file)
   response = get_gemini_response(input_prompt,image_data)

   st.header("Response is:")
   st.write(response)



