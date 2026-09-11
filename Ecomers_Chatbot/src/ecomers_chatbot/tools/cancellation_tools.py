from langchain_core.tools import tool
from ecomers_chatbot.data.orders import get_order, ORDERS 
@tool
def cancel_order(order_id: str) -> str:
    """
    Attempt to cancel the given order ID (e.g. 'ORD-1002'). Only orders
    with status 'Processing' can be cancelled. Returns a plain-text
    result. Always use this tool for cancellation requests instead of
    guessing whether an order can be cancelled.
    """
    key = order_id.strip().upper() if order_id else ""
    order = get_order(key)
 
    if order is None:
        return f"NOT_FOUND: No order exists with ID '{order_id}'. Cannot cancel."
 
    if order["status"] != "Processing":
        return (
            f"NOT_ELIGIBLE: Order {key} has status '{order['status']}' and "
            "can no longer be cancelled. Only orders still in Processing "
            "are eligible for cancellation."
        )
 
    # Simulate cancelling the order.
    ORDERS[key]["status"] = "Cancelled"
    ORDERS[key]["refund_eligible"] = False
    ORDERS[key]["cancel_eligible"] = False
 
    return f"SUCCESS: Order {key} ({order['product']}) has been cancelled."
 