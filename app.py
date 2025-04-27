import streamlit as st
import os
from docx import Document
from fpdf import FPDF
import qrcode
from PIL import Image
import base64
import PyPDF2
from pdf2docx import Converter
import openai
from io import BytesIO

# Initialize OpenAI client with API key
# Ensure you're getting the OpenAI API key from secrets
api_key = st.secrets.get("openai", {}).get("api_key")
if api_key:
    openai.api_key = api_key
else:
    st.error("OpenAI API key is missing. Please check your secrets file.")

# Function to generate image from text (AI) with better error handling
def generate_ai_image(prompt):
    try:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024"
        )

        # Check if the response contains an image URL
        if "data" in response:
            return response["data"][0]["url"]
        else:
            return f"Error: No data returned from OpenAI API."
    
    except openai.error.InvalidRequestError as e:
        st.error(f"Invalid Request Error: {str(e)}")
        return f"Invalid request: {str(e)}"
    except openai.error.AuthenticationError as e:
        st.error(f"Authentication Error: {str(e)}")
        return f"Authentication failed: {str(e)}"
    except openai.error.APIError as e:
        st.error(f"API Error: {str(e)}")
        return f"API error: {str(e)}"
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return f"An unexpected error occurred: {str(e)}"

# Streamlit app for QuickToolBox
def main():
    st.title("🔥 QuickToolBox - Convert, Generate & Create! 🔥")

    # Section for AI Image Generator
    st.header("🎨 AI Image Generator")
    
    prompt = st.text_input("Enter a prompt to generate an image")
    if prompt:
        if st.button("Generate AI Image", key="generate_ai"):
            with st.spinner("Generating your image..."):
                img_url = generate_ai_image(prompt)
                if img_url.startswith("http"):
                    st.image(img_url, caption="AI Generated Image", use_column_width=True)
                else:
                    st.error(img_url)  # Display the error message returned from the function

if __name__ == "__main__":
    main()
