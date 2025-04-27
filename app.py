import streamlit as st
import os
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import instaloader
from pytube import YouTube

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

# Function to download Instagram post or video
def download_instagram_post(post_url, download_dir):
    loader = instaloader.Instaloader()

    try:
        shortcode = post_url.split("/")[-2]  # Extract the shortcode from the URL
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        filename = os.path.join(download_dir, f"{post.owner_username}_{post.shortcode}")
        
        if not os.path.exists(download_dir):  # Ensure download directory exists
            os.makedirs(download_dir)
        
        loader.download_post(post, target=filename)
        return f"Downloaded to {filename}"
    except Exception as e:
        return f"Error downloading post: {e}"

# Function to download YouTube video
def download_youtube_video(url, download_dir):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()

        if not os.path.exists(download_dir):  # Ensure download directory exists
            os.makedirs(download_dir)

        stream.download(download_dir)
        return f"Downloaded video: {yt.title}"
    except Exception as e:
        return f"Error downloading video: {e}"

# Streamlit app for file upload and conversion
def main():
    st.title("QuickToolBox - DOCX to PDF, Instagram & YouTube Downloader")

    # DOCX to PDF Conversion
    st.subheader("DOCX to PDF Converter")
    uploaded_file = st.file_uploader("Upload a DOCX file", type="docx")
    if uploaded_file is not None:
        with open("uploaded_file.docx", "wb") as f:
            f.write(uploaded_file.getbuffer())

        output_pdf_path = "converted_file.pdf"

        try:
            docx_to_pdf("uploaded_file.docx", output_pdf_path)
            st.success("Conversion successful!")
            
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

    # Instagram Post/Video Downloader
    st.subheader("Instagram Post/Video Downloader")
    instagram_url = st.text_input("Enter Instagram Post URL")
    if instagram_url:
        download_button = st.button("Download Instagram Post")
        if download_button:
            download_message = download_instagram_post(instagram_url, "downloads/")
            st.write(download_message)

    # YouTube Video Downloader
    st.subheader("YouTube Video Downloader")
    youtube_url = st.text_input("Enter YouTube Video URL")
    if youtube_url:
        download_button = st.button("Download YouTube Video")
        if download_button:
            download_message = download_youtube_video(youtube_url, "downloads/")
            st.write(download_message)

if __name__ == "__main__":
    main()
