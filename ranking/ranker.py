import warnings
from langchain_core.load import dumps

warnings.filterwarnings("ignore", category=UserWarning)

def reciprocal_rank_fusion(results: list[list], k: int = 60) -> list[tuple]:
    fusion_scores = {}

    for docs in results:
        for rank, doc in enumerate(docs):
            doc_str = dumps(doc)
            fusion_scores[doc_str] = fusion_scores.get(doc_str, 0) + 1 / (rank + k)

    reranked_results = sorted(fusion_scores.items(), key=lambda x: x[1], reverse=True)
    return [(eval(doc), score) for doc, score in reranked_results]
