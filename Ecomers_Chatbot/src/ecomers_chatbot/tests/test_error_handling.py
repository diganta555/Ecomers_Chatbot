"""
Tests for Milestone 15's error handling in agent/pipeline.py.

The empty-input check happens BEFORE any LLM call, so we can pass
None for intent_chain/agent_executor here - they're never touched,
which means this test needs no API key and makes no network calls.
"""

from ecomers_chatbot.agent.pipeline import get_response


def test_empty_message_returns_a_fallback_without_calling_the_llm():
    result = get_response(
        intent_chain=None,
        agent_executor=None,
        chat_history=[],
        user_message="",
    )
    assert result.success is False
    assert result.tool_used is False
    assert "empty" in result.response.lower()


def test_whitespace_only_message_is_treated_as_empty():
    result = get_response(
        intent_chain=None,
        agent_executor=None,
        chat_history=[],
        user_message="   ",
    )
    assert result.success is False