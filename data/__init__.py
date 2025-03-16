import os
from .load_docs import update_docs

pdf_paths = []
web_paths = []

uploaded_folder_path = "C:/Users/Debajyoti/OneDrive/Desktop/sample_annotaion/app/uploaded_pdfs"
uploaded_txt = "C:/Users/Debajyoti/OneDrive/Desktop/sample_annotaion/app/uploaded_links.txt"

for root, dirs, files in os.walk(uploaded_folder_path):  
    for file in files:
        if file.endswith(".pdf"):  
            file_path = os.path.join(root, file)
            pdf_paths.append(file_path)

with open(uploaded_txt, "r", encoding="utf-8") as file:
    web_paths = file.read().splitlines()


combined_docs = update_docs(web_paths, pdf_paths)

__all__ = ["update_docs", "combined_docs"]
