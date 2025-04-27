import streamlit as st
import os
from docx import Document
from fpdf import FPDF
import base64
import qrcode
from PyPDF2 import PdfReader, PdfMerger
import requests
from transformers import pipeline

# Function to convert Word to PDF
def word_to_pdf(input_path, output_path):
    try:
        document = Document(input_path)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Loop through paragraphs and add to PDF
        for para in document.paragraphs:
            pdf.multi_cell(0, 10, para.text)
        
        pdf.output(output_path)
        return f"Converted Word to PDF: {output_path}"
    except Exception as e:
        return f"Error converting Word to PDF: {e}"

# Function to merge PDFs
def merge_pdfs(pdf_list, output_path):
    try:
        merger = PdfMerger()
        for pdf in pdf_list:
            merger.append(pdf)
        merger.write(output_path)
        merger.close()
        return f"Merged PDFs into: {output_path}"
    except Exception as e:
        return f"Error merging PDFs: {e}"

# Function to convert Image to URL (Base64 Encoding)
def image_to_url(input_image_path):
    try:
        with open(input_image_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{img_base64}"
    except Exception as e:
        return f"Error converting image to URL: {e}"

# Function to generate QR Code from text or URL
def generate_qr_code(data, output_path):
    try:
        img = qrcode.make(data)
        img.save(output_path)
        return f"QR Code generated: {output_path}"
    except Exception as e:
        return f"Error generating QR Code: {e}"

# Function to convert text to PDF
def text_to_pdf(text, output_path):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf.output(output_path)
        return f"Text converted to PDF: {output_path}"
    except Exception as e:
        return f"Error converting text to PDF: {e}"

# Function to get currency conversion rate
def convert_currency(amount, from_currency, to_currency):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()
        rate = data['rates'].get(to_currency)
        if rate:
            return amount * rate
        else:
            return f"Currency {to_currency} not supported."
    except Exception as e:
        return f"Error fetching currency rates: {e}"

# Function for AI-powered school/college answers using HuggingFace transformer
def ai_chat_answer(question):
    try:
        qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
        context = """
        1st Grade to 12th Grade curriculum and college-level topics across subjects.
        It covers Mathematics, Science, History, Geography, Languages, and more.
        Each grade's syllabus has specific chapters and subjects that students need to understand.
        College-level answers cover subjects like Engineering, Medicine, Humanities, Social Sciences, and more.
        """
        result = qa_pipeline(question=question, context=context)
        return result['answer']
    except Exception as e:
        return f"Error answering question: {e}"

# Streamlit app for file upload and conversion
def main():
    st.title("QuickToolBox - Conversion, Currency, and AI Education")

    # Word to PDF Conversion
    st.subheader("Word to PDF Converter")
    uploaded_word = st.file_uploader("Upload a Word document", type="docx")
    if uploaded_word is not None:
        with open("uploaded_file.docx", "wb") as f:
            f.write(uploaded_word.getbuffer())
        
        output_pdf_path = "converted_file.pdf"
        
        try:
            message = word_to_pdf("uploaded_file.docx", output_pdf_path)
            st.success(message)
            with open(output_pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name="converted_file.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"An error occurred during conversion: {e}")
        
        os.remove("uploaded_file.docx")

    # Merge PDFs
    st.subheader("Merge PDFs")
    uploaded_pdfs = st.file_uploader("Upload PDFs to Merge", type="pdf", accept_multiple_files=True)
    if uploaded_pdfs:
        with open("merged_output.pdf", "wb") as f:
            pdf_list = []
            for pdf in uploaded_pdfs:
                with open(pdf.name, "wb") as temp_pdf:
                    temp_pdf.write(pdf.getbuffer())
                    pdf_list.append(temp_pdf.name)
            merge_message = merge_pdfs(pdf_list, "merged_output.pdf")
            st.success(merge_message)
            with open("merged_output.pdf", "rb") as merged_pdf:
                st.download_button(
                    label="Download Merged PDF",
                    data=merged_pdf,
                    file_name="merged_output.pdf",
                    mime="application/pdf"
                )
            for pdf in pdf_list:
                os.remove(pdf)

    # Currency Conversion
    st.subheader("Currency Converter")
    amount = st.number_input("Enter Amount")
    from_currency = st.text_input("From Currency (e.g., USD)")
    to_currency = st.text_input("To Currency (e.g., EUR)")
    if st.button("Convert"):
        if amount and from_currency and to_currency:
            conversion_result = convert_currency(amount, from_currency.upper(), to_currency.upper())
            st.write(f"Converted Amount: {conversion_result}")
        else:
            st.write("Please fill in all fields.")

    # AI Chat for Education (School & College)
    st.subheader("AI Education Chat (School & College)")
    question = st.text_input("Ask your question")
    if question:
        answer = ai_chat_answer(question)
        st.write(answer)

if __name__ == "__main__":
    main()
