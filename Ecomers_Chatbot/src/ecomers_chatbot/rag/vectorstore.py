"""
Vector store setup.

Uses LangChain's built-in InMemoryVectorStore - no external vector DB
service or native dependency (Chroma/FAISS) needed, which keeps local
setup simple for this project. It rebuilds from the knowledge/ files
every time the app starts; that's fine at this scale (a handful of
short policy docs).
"""

from langchain_core.vectorstores import InMemoryVectorStore

from ecomers_chatbot.rag.loader import load_knowledge_documents
from ecomers_chatbot.rag.splitter import split_documents
from ecomers_chatbot.rag.embeddings import get_embeddings_model


def build_vectorstore() -> InMemoryVectorStore:
    documents = load_knowledge_documents()
    chunks = split_documents(documents)

    embeddings = get_embeddings_model()
    vectorstore = InMemoryVectorStore(embeddings)
    vectorstore.add_documents(chunks)

    return vectorstore