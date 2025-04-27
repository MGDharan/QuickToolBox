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

# Function to convert DOCX to PDF
def docx_to_pdf(input_path, output_path):
    document = Document(input_path)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for para in document.paragraphs:
        text = para.text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, text)

    pdf.output(output_path)

# Function to convert PDF to DOCX
def pdf_to_word(input_pdf, output_docx):
    cv = Converter(input_pdf)
    cv.convert(output_docx)
    cv.close()

# Function to merge PDFs
def merge_pdfs(pdf_list, output_path):
    merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

# Function to create a simple QR code with text
def create_text_qr(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    
    # Create a PIL image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert PIL image to bytes for Streamlit
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return buffered.getvalue()

# Function to generate image from text (AI)
def generate_ai_image(prompt):
    # Try to get API key from Streamlit secrets or environment variables
    try:
        # First try to get from Streamlit secrets
        api_key = st.secrets.get("OPENAI_API_KEY")
        
        # If not found in secrets, try environment variables
        if api_key is None:
            api_key = os.environ.get("OPENAI_API_KEY")
            
        # If still not found, return an error
        if api_key is None:
            return "API key not found. Please set OPENAI_API_KEY in Streamlit secrets or environment variables."
            
        openai.api_key = api_key
        
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        return response['data'][0]['url']
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app for QuickToolBox
def main():
    st.title("🔥 QuickToolBox - Convert, Generate & Create! 🔥")

    # Section for DOCX to PDF
    st.header("📄 DOCX to PDF Converter")
    uploaded_docx = st.file_uploader("Upload DOCX file", type="docx", key="docx")
    if uploaded_docx is not None:
        if st.button("Convert to PDF", key="convert_docx"):
            try:
                output_pdf = "converted_from_docx.pdf"
                with open("temp_uploaded.docx", "wb") as f:
                    f.write(uploaded_docx.getbuffer())
                docx_to_pdf("temp_uploaded.docx", output_pdf)
                st.success("DOCX successfully converted to PDF!")
                with open(output_pdf, "rb") as f:
                    st.download_button("Download PDF", f, file_name="converted.pdf", mime="application/pdf")
                os.remove("temp_uploaded.docx")
            except Exception as e:
                st.error(f"An error occurred during conversion: {e}")

    # Section for PDF to DOCX
    st.header("🔄 PDF to DOCX Converter")
    uploaded_pdf = st.file_uploader("Upload PDF file", type="pdf", key="pdf")
    if uploaded_pdf is not None:
        if st.button("Convert to DOCX", key="convert_pdf"):
            try:
                output_docx = "converted_from_pdf.docx"
                with open("temp_uploaded.pdf", "wb") as f:
                    f.write(uploaded_pdf.getbuffer())
                pdf_to_word("temp_uploaded.pdf", output_docx)
                st.success("PDF successfully converted to DOCX!")
                with open(output_docx, "rb") as f:
                    st.download_button("Download DOCX", f, file_name="converted.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                os.remove("temp_uploaded.pdf")
            except Exception as e:
                st.error(f"An error occurred during conversion: {e}")

    # Section for Merging PDFs
    st.header("🧩 Merge Multiple PDFs")
    uploaded_pdfs = st.file_uploader("Upload multiple PDFs", type="pdf", accept_multiple_files=True)
    if uploaded_pdfs:
        if st.button("Merge PDFs", key="merge_pdfs"):
            try:
                pdf_paths = []
                for i, uploaded_pdf in enumerate(uploaded_pdfs):
                    pdf_path = f"temp_{i}.pdf"
                    with open(pdf_path, "wb") as f:
                        f.write(uploaded_pdf.getbuffer())
                    pdf_paths.append(pdf_path)

                merged_output = "merged_output.pdf"
                merge_pdfs(pdf_paths, merged_output)

                st.success("PDFs merged successfully!")
                with open(merged_output, "rb") as f:
                    st.download_button("Download Merged PDF", f, file_name="merged.pdf", mime="application/pdf")

                # Clean up temporary files
                for path in pdf_paths:
                    os.remove(path)
            except Exception as e:
                st.error(f"An error occurred while merging PDFs: {e}")

    # Section for QR Code Generator
    st.header("🔳 QR Code Generator")
    st.write("Create a QR code with custom text")
    
    qr_text = st.text_input("Enter text for your QR code:", "https://streamlit.io")
    
    if qr_text:
        if st.button("Generate QR Code", key="generate_qr"):
            try:
                # Generate QR code as bytes
                qr_bytes = create_text_qr(qr_text)
                
                # Display the QR code
                st.image(qr_bytes, caption="Generated QR Code", width=300)
                
                # Offer download option
                st.download_button(
                    label="Download QR Code",
                    data=qr_bytes,
                    file_name="qr_code.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"An error occurred while generating the QR code: {e}")

    # Section for AI Image Generation
    st.header("🎨 AI Image Generator")
    
    # Notice about API key requirement
    st.info("Note: This feature requires an OpenAI API key. You can set it up in Streamlit secrets or as an environment variable named 'OPENAI_API_KEY'.")
    
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
