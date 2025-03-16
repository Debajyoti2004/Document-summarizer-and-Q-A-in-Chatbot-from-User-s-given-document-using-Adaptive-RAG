from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

prompt = PromptTemplate(
    template="""
You are an expert summarizer who can summarize a retrieved document from documents string

Documents:{docs}
Use this documents to summarize 

""",
input_variables=["docs"]
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)

summarizer_chain = (
    prompt
    | llm
    | StrOutputParser()
)