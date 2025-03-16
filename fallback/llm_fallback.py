from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

prompt = PromptTemplate(
    template="""
    You are an AI assistant skilled in providing accurate, concise answers.
    Respond to the following user question using your knowledge.
    Keep your answer short and to the point.
    
    Question: {question}
    """
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)

llm_fallback_chain = (
    prompt
    | llm
    | StrOutputParser()
)


