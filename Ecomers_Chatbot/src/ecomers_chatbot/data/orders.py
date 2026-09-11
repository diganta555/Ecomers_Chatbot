"""
Mock order database.

This is the single source of truth for order data in the whole project.
Milestone 15 note: nowhere else should order facts be invented - every
tool and prompt must route through get_order() below.
"""

ORDERS = {
    "ORD-1001": {
        "customer": "Rahul",
        "product": "iPhone 15",
        "status": "Shipped",
        "expected_or_delivery_date": "2026-09-13",
        "refund_eligible": True,
        "cancel_eligible": False,
    },
    "ORD-1002": {
        "customer": "Amit",
        "product": "MacBook Air M3",
        "status": "Processing",
        "expected_or_delivery_date": "2026-09-15",
        "refund_eligible": True,
        "cancel_eligible": True,
    },
    "ORD-1003": {
        "customer": "Priya",
        "product": "Samsung Galaxy S25",
        "status": "Delivered",
        "expected_or_delivery_date": "2026-09-08",
        "refund_eligible": True,
        "cancel_eligible": False,
    },
    "ORD-1004": {
        "customer": "Arjun",
        "product": "Sony Headphones",
        "status": "Refunded",
        "expected_or_delivery_date": None,
        "refund_eligible": False,
        "cancel_eligible": False,
    },
}


def get_order(order_id: str) -> dict | None:
    """
    Returns the order record for order_id, or None if it doesn't exist.
    This is the ONLY place that reads order data - tools call this
    instead of touching ORDERS directly, so there's one source of truth.
    """
    if not order_id:
        return None
    return ORDERS.get(order_id.strip().upper())