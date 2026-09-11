"""
Prompt used to classify a customer message into one of the required
intents. Kept separate from support_prompt.py because it has a
different job: classification, not conversation.
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


INTENT_SYSTEM_INSTRUCTION = """You are an intent classification system for a
customer support agent. Given the conversation so far and the customer's
latest message, classify it into exactly one of these intents:
 
- GENERAL_QUERY: general questions, greetings, small talk, anything that
  doesn't fit the categories below.
- ORDER_STATUS: asking where an order is, its shipping/delivery status.
- REFUND_REQUEST: asking for a refund or money back.
- ORDER_CANCELLATION: asking to cancel an order.
- PRODUCT_QUERY: asking about a product's price, stock, specs, warranty.
- HUMAN_SUPPORT: explicitly asking for a human agent, or clearly frustrated
  / stuck beyond what a bot should handle.
 
Also extract an order_id if one is mentioned in this message or earlier in
the conversation (format like 'ORD-1001'). If none is known, leave it null.
 
Also extract a product_name if one is mentioned in this message or earlier
in the conversation (e.g. 'MacBook Air M3', 'Sony headphones'). If none is
known, leave it null.
"""
 
def build_intent_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", INTENT_SYSTEM_INSTRUCTION),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{query}"),
    ])
 