from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

class WebSearch(BaseModel):
    query: str = Field(description="Use this to search the internet for any questions unrelated to the vectorstore topics.")

class VectorStore(BaseModel):
    query: str = Field(description="Use this to search the vectorstore for questions about the given related topics.")

template = """You are an expert at deciding whether to use a vectorstore or a web search.
The vectorstore contains information about the following topics: {related_topics}.
- If the question is about these topics, choose VectorStore.
- If the question is about anything else, choose WebSearch.

User question: {question}
Which tool will you use?"""

router_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0
).bind_tools(
    tools=[WebSearch, VectorStore]
)

prompt = PromptTemplate(
    template=template,
    input_variables=["related_topics", "question"]
)

router_rag_chain = (
    prompt
    | router_llm
)

