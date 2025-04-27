import streamlit as st
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Function to convert DOCX to PDF
def docx_to_pdf(input_path, output_path):
    # Open the DOCX file using python-docx
    document = Document(input_path)
    pdf = canvas.Canvas(output_path, pagesize=letter)

    # Set the initial Y position for text
    y_position = 750  

    # Loop through the paragraphs in the DOCX file and write them to the PDF
    for para in document.paragraphs:
        pdf.drawString(100, y_position, para.text)
        y_position -= 20  # Move the Y position down for the next line

        if y_position < 50:  # If the Y position is too low, create a new page
            pdf.showPage()
            y_position = 750

    pdf.save()

# Streamlit app for file upload and conversion
def main():
    st.title("DOCX to PDF Converter")
    
    uploaded_file = st.file_uploader("Upload a DOCX file", type="docx")
    
    if uploaded_file is not None:
        # Save the uploaded DOCX file to a temporary location
        with open("uploaded_file.docx", "wb") as f:
            f.write(uploaded_file.getbuffer())

        output_pdf_path = "converted_file.pdf"

        try:
            # Convert DOCX to PDF
            docx_to_pdf("uploaded_file.docx", output_pdf_path)
            st.success("Conversion successful!")
            
            # Provide a link for downloading the PDF
            with open(output_pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name="converted_file.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"An error occurred during conversion: {e}")

        # Clean up temporary files
        os.remove("uploaded_file.docx")

if __name__ == "__main__":
    main()
