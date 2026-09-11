"""
Prompt for answering a policy/FAQ question using ONLY retrieved chunks.
Separate from support_prompt.py and intent_prompt.py because its job
is narrowly "ground this answer in these specific passages."
"""

from langchain_core.prompts import ChatPromptTemplate

RAG_SYSTEM_INSTRUCTION = """You are a customer support agent answering
a policy or FAQ question using ONLY the retrieved context below. If the
context doesn't contain the answer, say you don't have that information
and suggest the customer contact support directly - do not guess or use
outside knowledge.

Retrieved context:
{context}
"""


def build_rag_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", RAG_SYSTEM_INSTRUCTION),
        ("human", "{question}"),
    ])