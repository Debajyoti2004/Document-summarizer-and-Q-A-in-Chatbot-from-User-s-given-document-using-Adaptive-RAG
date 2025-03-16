from langchain.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
from dotenv import load_dotenv
import os
from data import combined_docs

load_dotenv()

api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise ValueError("COHERE_API_KEY not found in environment variables.")


splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="gpt2",
    chunk_size=512,
    chunk_overlap=64
)
split_docs = splitter.split_documents(combined_docs)

vector_store = FAISS.from_documents(
    documents=split_docs,
    embedding=CohereEmbeddings(
        model="embed-english-v2.0"
    )
)

retriever = vector_store.as_retriever(search_kwargs={"k": 2})
print("----Initial Retriever Workflow----")

