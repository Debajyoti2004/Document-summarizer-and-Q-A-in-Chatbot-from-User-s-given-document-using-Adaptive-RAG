from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

class RelatedTopics(BaseModel):
    related_topics: list[str] = Field(
        description="List of related topics based on the user's question"
    )

prompt = PromptTemplate(
    template="""
    You are an AI assistant skilled at analyzing documents and extracting key related topics. 
    Given the following document(s), identify and list the most relevant related topics.

    Document(s): {docs}

    Ensure the topics are concise, meaningful, and directly related to the document's content.
    Provide a diverse set of related topics that cover different aspects of the document(s).
    """,
    input_variables=["docs"]
) 
 

structured_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
).bind_tools(
    tools=[RelatedTopics]
)

relatedTopics_finder_chain = (
    prompt
    | structured_llm
)

