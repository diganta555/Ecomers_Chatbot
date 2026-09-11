"""
Tests for the raw data-layer lookups (no LLM, no tools involved) -
these are the single source of truth every tool depends on.
"""

from ecomers_chatbot.data.orders import get_order
from ecomers_chatbot.data.products import find_product


def test_get_order_returns_record_for_known_id():
    order = get_order("ORD-1001")
    assert order is not None
    assert order["product"] == "iPhone 15"


def test_get_order_is_case_insensitive():
    assert get_order("ord-1001") == get_order("ORD-1001")


def test_get_order_returns_none_for_unknown_id():
    assert get_order("ORD-9999") is None


def test_get_order_returns_none_for_empty_input():
    assert get_order("") is None
    assert get_order(None) is None


def test_find_product_exact_match():
    product = find_product("MacBook Air M3")
    assert product is not None
    assert product["price"] == 999


def test_find_product_partial_match():
    product = find_product("iphone")
    assert product is not None
    assert product["name"] == "iPhone 15"


def test_find_product_returns_none_for_unknown_product():
    assert find_product("Nokia 3310") is None


def test_find_product_returns_none_for_empty_input():
    assert find_product("") is None