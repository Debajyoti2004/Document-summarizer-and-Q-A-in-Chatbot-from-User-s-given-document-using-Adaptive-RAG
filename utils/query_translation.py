from langchain_cohere import ChatCohere
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

template = """You are a helpful assistant that generates multiple search queries based on a single input query. \n
Generate multiple search queries related to: {question} \n
Output (4 queries):"""

prompt = PromptTemplate(
    template=template,
    input_variables=["question"]
)

llm = ChatCohere(
    model="command",
    cohere_api_key=os.getenv("COHERE_API_KEY")
)

generate_queries = (
    prompt
    | llm
    | StrOutputParser()
    | (lambda x: x.strip().split("\n"))
)
print("----Query Translation Workflow----")



