import os
from langchain.document_loaders import WebBaseLoader, PyPDFLoader

def load_web_docs(web_paths):
    web_loader = WebBaseLoader(web_paths=web_paths)
    return web_loader.load()

def load_pdf_docs(pdf_paths):
    pdf_docs = []
    for pdf in pdf_paths:
        loader = PyPDFLoader(pdf)
        pdf_docs.extend(loader.load())
    return pdf_docs

def update_docs(web_paths, pdf_paths):
    web_docs = load_web_docs(web_paths)
    pdf_docs = load_pdf_docs(pdf_paths)
    combined_docs = web_docs + pdf_docs

    return combined_docs
