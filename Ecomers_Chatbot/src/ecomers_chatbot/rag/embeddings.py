"""
Embeddings model used to turn text chunks into vectors for similarity
search. Kept as its own tiny module so it's easy to swap providers
later without touching the rest of the RAG pipeline.
"""

from langchain_openai import OpenAIEmbeddings


def get_embeddings_model() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model="text-embedding-3-small")