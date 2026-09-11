"""
Splits loaded documents into smaller chunks for embedding/retrieval.

Our policy docs are short, so chunk_size is generous - the goal is
each chunk stays a coherent, self-contained idea (a numbered policy
point), not that we minimize token count.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " "],
    )
    return splitter.split_documents(documents)