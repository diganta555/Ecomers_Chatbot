"""
Order status tool.

Milestone 15's "no hallucination" rule starts here: this function is the
ONLY thing allowed to state an order's real status. The LLM is only ever
allowed to explain this tool's output, never invent its own.
"""

from ecomers_chatbot.data.orders import get_order
from langchain_core.tools import tool


@tool
def get_order_status(order_id: str) -> str:
    """
    Look up the real status of a customer's order by its order ID
    (e.g. 'ORD-1001'). Returns a plain-text fact string describing the
    order, or a clear not-found message if the order doesn't exist.
    Always use this tool for order status questions instead of guessing.
    """
    order = get_order(order_id)

    if order is None:
        return f"NOT_FOUND: No order exists with ID '{order_id}'."

    return (
        f"FOUND: Order {order_id.strip().upper()} - "
        f"product: {order['product']}, "
        f"status: {order['status']}, "
        f"expected/delivery date: {order['expected_or_delivery_date']}."
    )