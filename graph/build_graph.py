
from langgraph.graph import END, StateGraph, START
from .graph_state import GraphState
from .graph_state import (
    retrieve,
    router_state,
    web_search_state,
    grade_documents,
    grade_generation,
    llm_fallback_state,
    generate,
    decide_to_generate,
    summarizer_state,
    relative_topics_state
)

compiled_workflow = None

def compile_workflow():
    global compiled_workflow
    if compiled_workflow is not None:
        print("Workflow already compiled. Returning existing instance.")
        return compiled_workflow

    print("Compiling workflow...")
    workflow = StateGraph(GraphState)

    nodes = {
        "relative_topics":relative_topics_state,
        "web_search": web_search_state,
        "retrieve": retrieve,
        "grade_documents": grade_documents,
        "grade_generation": grade_generation,
        "llm_fallback_state": llm_fallback_state,
        "generate": generate,
        "summarize":summarizer_state
    }
    
    for name, func in nodes.items():
        workflow.add_node(name, func)

    workflow.add_edge(
        START,
        "relative_topics"
    )
    workflow.add_conditional_edges(
        "relative_topics",
        router_state,
        {
            "vectorestore": "retrieve",
            "web_search": "web_search",
            "llm_fallback": "llm_fallback_state"
        }
    )

    workflow.add_edge("web_search", "grade_documents")
    workflow.add_edge("retrieve", "grade_documents")

    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "web_search": "web_search",
            "summarize":"summarize"
        }
    )
    workflow.add_edge(
        "summarize",
        "generate"
    )

    workflow.add_conditional_edges(
        "generate",
        grade_generation,
        {
            "web_search": "web_search",
            "generation": "generate",
            "success": END
        }
    )
    # workflow.add_edge(
    #     "generate",
    #     END
    # )

    workflow.add_edge("llm_fallback_state", END)

    compiled_workflow = workflow.compile()
    print("Workflow compiled successfully.")
    return compiled_workflow
