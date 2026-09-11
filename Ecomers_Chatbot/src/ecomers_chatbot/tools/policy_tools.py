"""
Policy/FAQ tool - wraps the RAG pipeline (retriever + grounded prompt)
as a single tool the agent can call.

Flow: question -> retriever -> relevant chunks -> prompt -> LLM ->
grounded answer. Matches the architecture diagram in the spec.

NOTE: the model/chain are built LAZILY (on first use, cached after
that) rather than at import time. Building ChatOpenAI() at module
import time is fragile - if this module gets imported before
load_dotenv() has run (easy to do accidentally once you have several
files importing each other), OPENAI_API_KEY isn't in the environment
yet and you get a confusing OpenAIError deep in a stack trace.
"""

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

from ecomers_chatbot.rag.retriever import get_retriever
from ecomers_chatbot.prompts.rag_prompt import build_rag_prompt

_rag_chain = None


def _get_rag_chain():
    global _rag_chain
    if _rag_chain is None:
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        _rag_chain = build_rag_prompt() | model
    return _rag_chain


@tool
def answer_policy_question(question: str) -> str:
    """
    Answer a question about company policy (refunds, shipping,
    cancellations, returns) or a general FAQ, by retrieving relevant
    passages from the knowledge base and grounding the answer in them.
    Use this tool for policy/FAQ questions instead of general knowledge -
    e.g. 'how long do refunds take', 'can I change my shipping address',
    'what's your return window'.
    """
    retriever = get_retriever(k=3)
    retrieved_docs = retriever.invoke(question)

    if not retrieved_docs:
        return "NOT_FOUND: No relevant policy information was found for this question."

    context = "\n\n".join(
        f"[{doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc in retrieved_docs
    )

    response = _get_rag_chain().invoke({"context": context, "question": question})
    return f"FOUND: {response.content}"