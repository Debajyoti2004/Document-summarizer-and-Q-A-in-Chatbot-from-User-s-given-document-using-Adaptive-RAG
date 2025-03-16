from utils import generate_queries
from ranking import reciprocal_rank_fusion
from .initial_retriever import retriever

final_retrieval_chain = (
    generate_queries
    | retriever.map()
    | reciprocal_rank_fusion
)
print("----Final Retriever Workflow----")