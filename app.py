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
    openai.api_key = st.secrets["OPENAI_API_KEY"]  # Set your OpenAI API key in Streamlit secrets
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        return response['data'][0]['url']
    except Exception as e:
        return str(e)

# Streamlit app for QuickToolBox
def main():
    st.title("🔥 QuickToolBox - Convert, Generate & Create! 🔥")

    # Section for DOCX to PDF
    st.header("📄 DOCX to PDF Converter")
    uploaded_docx = st.file_uploader("Upload DOCX file", type="docx", key="docx")
    if uploaded_docx is not None:
        output_pdf = "converted_from_docx.pdf"
        with open("temp_uploaded.docx", "wb") as f:
            f.write(uploaded_docx.getbuffer())
        docx_to_pdf("temp_uploaded.docx", output_pdf)
        st.success("DOCX successfully converted to PDF!")
        with open(output_pdf, "rb") as f:
            st.download_button("Download PDF", f, file_name="converted.pdf", mime="application/pdf")
        os.remove("temp_uploaded.docx")

    # Section for PDF to DOCX
    st.header("🔄 PDF to DOCX Converter")
    uploaded_pdf = st.file_uploader("Upload PDF file", type="pdf", key="pdf")
    if uploaded_pdf is not None:
        output_docx = "converted_from_pdf.docx"
        with open("temp_uploaded.pdf", "wb") as f:
            f.write(uploaded_pdf.getbuffer())
        pdf_to_word("temp_uploaded.pdf", output_docx)
        st.success("PDF successfully converted to DOCX!")
        with open(output_docx, "rb") as f:
            st.download_button("Download DOCX", f, file_name="converted.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        os.remove("temp_uploaded.pdf")

    # Section for Merging PDFs
    st.header("🧩 Merge Multiple PDFs")
    uploaded_pdfs = st.file_uploader("Upload multiple PDFs", type="pdf", accept_multiple_files=True)
    if uploaded_pdfs:
        if st.button("Merge PDFs"):
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

    # Section for QR Code Generator
    st.header("🔳 QR Code Generator")
    st.write("Create a QR code with custom text")
    
    qr_text = st.text_input("Enter text for your QR code:", "https://streamlit.io")
    
    if qr_text:
        if st.button("Generate QR Code"):
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

    # Section for AI Image Generation
    st.header("🎨 AI Image Generator")
    prompt = st.text_input("Enter a prompt to generate an image")
    if prompt:
        if st.button("Generate AI Image"):
            with st.spinner("Generating your image..."):
                img_url = generate_ai_image(prompt)
                if img_url.startswith("http"):
                    st.image(img_url, caption="AI Generated Image", use_column_width=True)
                else:
                    st.error(f"Error: {img_url}")

if __name__ == "__main__":
    main()
