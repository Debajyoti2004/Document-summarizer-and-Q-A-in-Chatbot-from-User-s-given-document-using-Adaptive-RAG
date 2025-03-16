from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

class GradeAnswer(BaseModel):
    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)
structured_llm_grader = llm.bind_tools(
    tools=[GradeAnswer]
)

prompt = PromptTemplate(
    template="""
You are an AI assistant that grades documents based on a user question. 
Answer 'yes' if the documents are relevant to the question, otherwise answer 'no'.

User question: {question}

Documents:
{docs}

Provide a binary score ('yes' or 'no') indicating if the documents address the user's question.
""",
    input_variables=["question", "docs"]
)


document_grader_chain = (
    prompt
    | structured_llm_grader
)
