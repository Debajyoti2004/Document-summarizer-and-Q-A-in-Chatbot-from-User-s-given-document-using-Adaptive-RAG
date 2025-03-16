from retrievers import final_retrieval_chain
from generation import generate_chain
from fallback import llm_fallback_chain
from grader import generation_grader_chain,document_grader_chain
from typing_extensions import TypedDict
from router import router_rag_chain
from search import web_search_tool
from typing import List
from langchain.schema import Document
from summarizer import summarizer_chain
from utils import relatedTopics_finder_chain
from data import combined_docs

class GraphState(TypedDict):
    question:str
    query:str
    summary:str
    related_topics:List[str]
    documents:List[str]
    generation:str

def retrieve(state):
    print("---Retrieving---")
    question = state["question"]
    response = final_retrieval_chain.invoke({
        "question": question
    })
    return {
        **state,
        "documents": response
    }
def relative_topics_state(state):
    print("---RELATED TOPICS---")
    response = relatedTopics_finder_chain.invoke({
        "docs":combined_docs
    })
    related_topics = response.tool_calls[0]["args"]["related_topics"]
    return {
        **state,
        "related_topics":related_topics
    }


def router_state(state):
    print("---Routing---")
    related_topics = state["related_topics"]
    question = state["question"]
    response = router_rag_chain.invoke({
        "related_topics": related_topics,
        "question": question
    })

    if not response.tool_calls:
        print("---ROUTE QUESTION TO FALL BACK LLM---")
        return "llm_fallback"
    
    if len(response.tool_calls) == 0:
        raise "Router could not decide which tool to use"
    
    source = response.tool_calls[0]["name"]
    query = response.tool_calls[0]["args"]["query"]
    state["query"] = query

    if source == "WebSearch":
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return "web_search"
    elif source == "VectorStore":
        print("---ROUTE QUESTION TO VECTORSTORE---")
        return "vectorestore"
    
    else: 
        print("---ROUTE QUESTION TO FALL BACK LLM---")
        return "llm_fallback"
    
def web_search_state(state):
    print("---WEB SEARCHING---")
    question = state["question"]
    web_results = web_search_tool.invoke({
        "query":question
    })

    web_docs = "\n".join(d["content"] for d in web_results)
    web_docs = Document(page_content=web_docs)
    return {
        **state,
        "documents": web_docs
    }

def grade_documents(state):
    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    docs = state["documents"]

    filtered_docs = []

    for d in docs:
        response = document_grader_chain.invoke({
            "question": question,
            "docs": d
        })
        grade = response.content
        if grade == "yes":
            print("----Document is relevant----")
            filtered_docs.append(d)
        elif grade == "no":
            print("----Document is not relevant----")
            continue

    return {
        **state,
        "question": question,
        "documents": filtered_docs
    }

def decide_to_generate(state):
    filtered_docs = state["documents"]

    if not filtered_docs:
        print("---NO RELEVANT DOCUMENTS FOUND---")
        return "web_search"
    else:
        print("---RELEVANT DOCUMENTS FOUND \n Decide: Generate---")
        return "summarize"
    
def generate(state):
    question = state["question"]
    docs = state["documents"]

    if not isinstance(docs, list):
        docs = [docs]
    
    generation = generate_chain.invoke({
        "question": question,
        "docs": docs
    })
    return {
        **state,
        "generation": generation
    }

def grade_generation(state):
    generation = state["generation"]
    docs = state["documents"]
    question = state["question"]

    response = generation_grader_chain.invoke({
        "generation": generation,
        "docs": docs
    })
    grade = response.content
    if grade == "yes":
        print("----GENERATION IS GROUNDED IN----")
        print("----QUESTION VS DOCUMENTS----")
        response = document_grader_chain.invoke({
            "question": question,
            "docs": docs
        })
        doc_grade = response.content
        if doc_grade == "yes":
            print("----DOCUMENTS ARE RELEVANT----")
            return "success"
        else:
            print("----DOCUMENTS ARE NOT RELEVANT----")
            return "web_search"
        
    elif grade == "no":
        print("----GENERATION IS NOT GROUNDED----")
        return "generation"
    

def llm_fallback_state(state):
    print("---FALL BACK TO LLM---")
    question = state["question"]
    response = llm_fallback_chain.invoke({
        "question": question
    })
    generation = response
    return {
        **state,
        "generation": generation
    }

def summarizer_state(state):
    documents = state["documents"]
    summary = summarizer_chain.invoke({
        "docs":documents
    })

    return {
        **state,
        "summary":summary
    }