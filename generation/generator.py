from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

prompt = PromptTemplate(
    template="""
    You are an AI assistant skilled in providing accurate, concise answers.
    Respond to the following user question using follwing documents.

    Required Documents: {docs}
    Keep your answer short and to the point.
    
    Question: {question}
    """,
    input_variables=["question","docs"]
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)

generate_chain = (
    prompt
    | llm
    | StrOutputParser()
)