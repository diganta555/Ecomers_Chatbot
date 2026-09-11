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
    "ORD-1005": {
        "customer": "Sneha",
        "product": "iPhone 15 Pro",
        "status": "Processing",
        "expected_or_delivery_date": "2026-09-18",
        "refund_eligible": True,
        "cancel_eligible": True,
    },
    "ORD-1006": {
        "customer": "Vikram",
        "product": "MacBook Pro 14",
        "status": "Shipped",
        "expected_or_delivery_date": "2026-09-14",
        "refund_eligible": True,
        "cancel_eligible": False,
    },
    "ORD-1007": {
        "customer": "Ananya",
        "product": "Dell XPS 13",
        "status": "Delivered",
        "expected_or_delivery_date": "2026-08-30",
        "refund_eligible": True,
        "cancel_eligible": False,
    },
    "ORD-1008": {
        "customer": "Karan",
        "product": "Lenovo ThinkPad X1 Carbon",
        "status": "Cancelled",
        "expected_or_delivery_date": None,
        "refund_eligible": False,
        "cancel_eligible": False,
    },
    "ORD-1009": {
        "customer": "Meera",
        "product": "Apple AirPods Pro",
        "status": "Processing",
        "expected_or_delivery_date": "2026-09-16",
        "refund_eligible": True,
        "cancel_eligible": True,
    },
    "ORD-1010": {
        "customer": "Rohan",
        "product": "Bose QuietComfort Earbuds",
        "status": "Shipped",
        "expected_or_delivery_date": "2026-09-12",
        "refund_eligible": True,
        "cancel_eligible": False,
    },
    "ORD-1011": {
        "customer": "Divya",
        "product": "iPad Air",
        "status": "Delivered",
        "expected_or_delivery_date": "2026-09-01",
        "refund_eligible": True,
        "cancel_eligible": False,
    },
    "ORD-1012": {
        "customer": "Aditya",
        "product": "Samsung Galaxy Tab S9",
        "status": "Refunded",
        "expected_or_delivery_date": None,
        "refund_eligible": False,
        "cancel_eligible": False,
    },
    "ORD-1013": {
        "customer": "Pooja",
        "product": "Apple Watch Series 9",
        "status": "Processing",
        "expected_or_delivery_date": "2026-09-20",
        "refund_eligible": True,
        "cancel_eligible": True,
    },
    "ORD-1014": {
        "customer": "Nikhil",
        "product": "Samsung Galaxy Watch 6",
        "status": "Shipped",
        "expected_or_delivery_date": "2026-09-17",
        "refund_eligible": True,
        "cancel_eligible": False,
    },
    "ORD-1015": {
        "customer": "Ishaan",
        "product": "Sony Alpha a6400",
        "status": "Delivered",
        "expected_or_delivery_date": "2026-08-25",
        "refund_eligible": True,
        "cancel_eligible": False,
    },
    "ORD-1016": {
        "customer": "Tanvi",
        "product": "GoPro HERO12",
        "status": "Cancelled",
        "expected_or_delivery_date": None,
        "refund_eligible": False,
        "cancel_eligible": False,
    },
    "ORD-1017": {
        "customer": "Siddharth",
        "product": "Sony PlayStation 5",
        "status": "Processing",
        "expected_or_delivery_date": "2026-09-22",
        "refund_eligible": True,
        "cancel_eligible": True,
    },
    "ORD-1018": {
        "customer": "Riya",
        "product": "Nintendo Switch OLED",
        "status": "Shipped",
        "expected_or_delivery_date": "2026-09-14",
        "refund_eligible": True,
        "cancel_eligible": False,
    },
    "ORD-1019": {
        "customer": "Aryan",
        "product": "LG C3 55-inch OLED TV",
        "status": "Delivered",
        "expected_or_delivery_date": "2026-08-20",
        "refund_eligible": True,
        "cancel_eligible": False,
    },
    "ORD-1020": {
        "customer": "Kavya",
        "product": "Amazon Echo Dot",
        "status": "Processing",
        "expected_or_delivery_date": "2026-09-13",
        "refund_eligible": True,
        "cancel_eligible": True,
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