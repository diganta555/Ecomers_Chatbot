"""
Shared structured-output schemas for the agent.

Milestone 5 introduces the first one: IntentResult. Using Pydantic +
with_structured_output() means the model MUST return one of the six
allowed intents (a typo like "ORDER_STATUS " or "order_status" is
rejected/coerced rather than silently breaking downstream code) and
order_id is either a real string or None - never missing, never guessed.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field

IntentLabel = Literal[
    "GENERAL_QUERY",
    "ORDER_STATUS",
    "REFUND_REQUEST",
    "ORDER_CANCELLATION",
    "PRODUCT_QUERY",
    "HUMAN_SUPPORT",
]


class IntentResult(BaseModel):
    """Structured classification of a single customer message."""

    intent: IntentLabel = Field(
        description="The single best-matching customer intent category."
    )
    order_id: Optional[str] = Field(
        default=None,
        description=(
            "The order ID mentioned in the message or earlier in the "
            "conversation, formatted like 'ORD-1001'. None if no order "
            "ID is known."
        ),
    )
    product_name: Optional[str] = Field(
        default=None,
        description=(
            "The product name mentioned in the message or earlier in "
            "the conversation (e.g. 'MacBook Air M3', 'Sony headphones'). "
            "None if no product is mentioned."
        ),
    )


class FinalResponse(BaseModel):
    """
    Structured internal response for a single turn, matching the
    spec's required shape (Milestone 13). This is what a real backend
    would log/return alongside the plain-text reply - useful for
    analytics, debugging, and the Streamlit UI's status display.
    """

    intent: IntentLabel
    action: Optional[str] = Field(
        default=None,
        description="Name of the tool that was called, if any (e.g. 'get_order_status').",
    )
    order_id: Optional[str] = None
    product_name: Optional[str] = None
    tool_used: bool = False
    success: bool = True
    response: str
    escalate: bool = False