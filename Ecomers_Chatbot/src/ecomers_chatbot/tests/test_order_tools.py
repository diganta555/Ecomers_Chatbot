"""
Tests for get_order_status - Milestone 16 test table rows:
'Order' and 'Invalid order'.
"""

from ecomers_chatbot.tools.order_tools import get_order_status


def test_valid_order_returns_found_with_correct_status():
    result = get_order_status.invoke("ORD-1001")
    assert result.startswith("FOUND")
    assert "Shipped" in result
    assert "iPhone 15" in result


def test_order_id_is_case_and_whitespace_insensitive():
    result = get_order_status.invoke("  ord-1001  ")
    assert result.startswith("FOUND")


def test_invalid_order_returns_not_found():
    result = get_order_status.invoke("ORD-9999")
    assert result.startswith("NOT_FOUND")
    assert "ORD-9999" in result


def test_invalid_order_never_invents_a_status():
    """The critical no-hallucination check from the spec."""
    result = get_order_status.invoke("ORD-9999")
    for fake_status in ("Shipped", "Delivered", "Processing", "Refunded"):
        assert fake_status not in result