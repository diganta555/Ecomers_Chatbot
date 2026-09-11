"""
Tests for the structured-output schemas (Milestone 5 / 13). These
catch schema regressions early - e.g. if a required field is
accidentally removed, or an invalid intent value is allowed through.
"""

import pytest
from pydantic import ValidationError

from ecomers_chatbot.agent.state import IntentResult, FinalResponse


def test_intent_result_accepts_a_valid_intent():
    result = IntentResult(intent="ORDER_STATUS", order_id="ORD-1001")
    assert result.intent == "ORDER_STATUS"
    assert result.order_id == "ORD-1001"


def test_intent_result_defaults_order_id_and_product_name_to_none():
    result = IntentResult(intent="GENERAL_QUERY")
    assert result.order_id is None
    assert result.product_name is None


def test_intent_result_rejects_an_invalid_intent_label():
    with pytest.raises(ValidationError):
        IntentResult(intent="NOT_A_REAL_INTENT")


def test_final_response_matches_the_spec_shape():
    response = FinalResponse(
        intent="ORDER_STATUS",
        action="get_order_status",
        order_id="ORD-1001",
        tool_used=True,
        success=True,
        response="Your order has been shipped.",
        escalate=False,
    )
    dumped = response.model_dump()

    for field in ("intent", "action", "order_id", "tool_used", "success", "response", "escalate"):
        assert field in dumped