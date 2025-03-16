import streamlit as st
import requests
import os

UPLOAD_FOLDER = "uploaded_pdfs"
LINKS_FILE = "uploaded_links.txt"

st.set_page_config(page_title="PDF & Link Uploader", layout="centered")

st.title("Upload PDFs & Links")

pdfs = st.file_uploader("Upload PDFs", accept_multiple_files=True, type=["pdf"])
links = st.text_area("Enter website links (comma separated)")

if st.button("Submit & Proceed to Chatbot"):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    for pdf in pdfs:
        with open(os.path.join(UPLOAD_FOLDER, pdf.name), "wb") as f:
            f.write(pdf.getbuffer())

    with open(LINKS_FILE, "w") as f:
        f.write(links)
    
    st.success("Files and links saved successfully! Redirecting to chatbot...")
    st.switch_page("chatbot")
