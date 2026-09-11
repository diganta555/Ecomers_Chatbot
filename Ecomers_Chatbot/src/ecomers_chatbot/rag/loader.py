"""
Document loader for the knowledge base.

Loads every .txt file from knowledge/ into LangChain Document objects.
(If you swap in real .pdf files later, add PyPDFLoader here per file
and merge the results - the rest of the RAG pipeline doesn't change.)
"""

from pathlib import Path
from langchain_core.documents import Document

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"


def load_knowledge_documents() -> list[Document]:
    """Reads every .txt file in knowledge/ into a Document with source metadata."""
    documents = []

    for file_path in sorted(KNOWLEDGE_DIR.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8")
        documents.append(
            Document(
                page_content=text,
                metadata={"source": file_path.name},
            )
        )

    return documents