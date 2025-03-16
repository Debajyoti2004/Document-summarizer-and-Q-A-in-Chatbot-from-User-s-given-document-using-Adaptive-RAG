from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

class GradeRelevance(BaseModel):
    binary_score: str = Field(
        description="Answer 'yes' if the generated text is relevant to the documents, otherwise 'no'."
    )

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)

structured_llm_grader = llm.bind_tools(
    tools=[GradeRelevance]
)

prompt = PromptTemplate(
    template="""
You are an AI assistant that evaluates if a generated text is relevant to retrieved documents. 
Answer 'yes' if the generation is relevant and matches the content of the documents, otherwise answer 'no'.

LLM generated text: {generation}

Documents:
{docs}

Provide a binary score ('yes' or 'no') indicating whether the generated text is relevant to the documents.
""",
    input_variables=["generation", "docs"]
)

generation_grader_chain = (
    prompt
    | structured_llm_grader
)


