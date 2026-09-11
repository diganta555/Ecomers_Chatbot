from langchain_core.tools import tool
from ecomers_chatbot.data.orders import get_order, ORDERS


@tool
def process_refund(order_id:str)->str:
    """
    Attempt to process a refund for the given order ID (e.g. 'ORD-1001').
    Checks that the order exists, is refund-eligible, and has not already
    been refunded, before "processing" it. Returns a plain-text result.
    Always use this tool for refund requests instead of guessing.
    """
    key= order_id.strip().upper() if order_id else ""
    order=get_order(key)


    if order is None:
        return F"NOT_FOUND: No order exist with ID'{order_id}'. Cannot process a refund "
    
    if order["status"] == "Refunded":
        return f"ALREADY_REFUNDED: Order {key} has already been refunded. No further action needed."
 
    if not order["refund_eligible"]:
        return (
            f"NOT_ELIGIBLE: Order {key} (status: {order['status']}) "
            "is not eligible for a refund under current policy."
        )

 # Simulate processing the refund: update the mock record.
    ORDERS[key]["status"] = "Refunded"
    ORDERS[key]["refund_eligible"] = False
    ORDERS[key]["cancel_eligible"] = False
 
    return f"SUCCESS: Refund processed for order {key} ({order['product']})."
 


