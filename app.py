import streamlit as st
from docx2pdf import convert
import os
import uuid
from instaloader import Instaloader, Post

# Folder setup
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

st.title("🔥 QuickToolBox - Download & Convert Anything! 🔥")

st.sidebar.header("Choose a Tool:")

tool = st.sidebar.selectbox(
    "Select what you want to do:",
    ("Convert Word to PDF", "Download Instagram Post/Reel")
)

if tool == "Convert Word to PDF":
    st.header("📄 Word to PDF Converter")
    uploaded_file = st.file_uploader("Upload a .docx file", type=["docx"])
    
    if uploaded_file is not None:
        file_id = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.docx")
        output_path = os.path.join(DOWNLOAD_FOLDER, f"{file_id}.pdf")
        
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        if st.button("Convert Now"):
            convert(input_path, output_path)
            st.success("Converted Successfully!")
            with open(output_path, "rb") as f:
                st.download_button("Download PDF", f, file_name="ConvertedFile.pdf")

if tool == "Download Instagram Post/Reel":
    st.header("📸 Instagram Downloader")
    instalink = st.text_input("Paste Instagram Post or Reel Link:")

    if st.button("Download Instagram Content"):
        if instalink:
            try:
                loader = Instaloader()
                shortcode = instalink.strip('/').split("/")[-1]
                post = Post.from_shortcode(loader.context, shortcode)
                
                target_folder = os.path.join(DOWNLOAD_FOLDER, shortcode)
                os.makedirs(target_folder, exist_ok=True)
                
                loader.download_post(post, target=target_folder)
                st.success(f"Downloaded Successfully to {target_folder}")
                st.info("Note: Files saved on server. Visit Downloads section.")
            except Exception as e:
                st.error(f"Download failed: {e}")
        else:
            st.warning("Please paste a valid link!")

st.markdown("---")
st.caption("© 2025 QuickToolBox - All rights reserved")
