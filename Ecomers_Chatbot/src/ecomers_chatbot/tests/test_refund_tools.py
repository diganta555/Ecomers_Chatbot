"""
Tests for process_refund - Milestone 16 test table rows:
'Refund' and 'Duplicate refund'.
"""

from ecomers_chatbot.tools.refund_tools import process_refund
from ecomers_chatbot.data.orders import ORDERS


def test_eligible_order_refund_succeeds():
    result = process_refund.invoke("ORD-1001")
    assert result.startswith("SUCCESS")
    assert ORDERS["ORD-1001"]["status"] == "Refunded"


def test_already_refunded_order_is_rejected():
    """ORD-1004 starts as already Refunded in the mock data."""
    result = process_refund.invoke("ORD-1004")
    assert result.startswith("ALREADY_REFUNDED")


def test_refunding_twice_in_a_row_is_rejected_the_second_time():
    first = process_refund.invoke("ORD-1002")
    second = process_refund.invoke("ORD-1002")
    assert first.startswith("SUCCESS")
    assert second.startswith("ALREADY_REFUNDED")


def test_nonexistent_order_cannot_be_refunded():
    result = process_refund.invoke("ORD-9999")
    assert result.startswith("NOT_FOUND")