"""
Retriever built on top of the vector store. This is what the policy
tool calls: given a question, it returns the top-k most relevant
chunks from the knowledge base.
"""

from langchain_core.vectorstores import VectorStoreRetriever

from ecomers_chatbot.rag.vectorstore import build_vectorstore

_vectorstore = None


def get_retriever(k: int = 3) -> VectorStoreRetriever:
    """
    Builds the vector store once (module-level cache) and returns a
    retriever over it. k=3 chunks is usually enough context for a
    single policy question without overwhelming the prompt.
    """
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = build_vectorstore()

    return _vectorstore.as_retriever(search_kwargs={"k": k})