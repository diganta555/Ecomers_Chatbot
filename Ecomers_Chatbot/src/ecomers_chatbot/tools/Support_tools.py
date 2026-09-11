"""
Human escalation tool.
 
Milestone 10: creates a support ticket when a customer explicitly asks
for a human, or when their issue is beyond what the bot is allowed to
handle. Returns a real ticket ID so the handoff feels concrete rather
than "someone will get back to you" vagueness.
"""
 
import itertools
from langchain_core.tools import tool
 
# Simple in-memory ticket counter, starting at the spec's example (5001).
_ticket_counter = itertools.count(5001)
 
 
@tool
def escalate_to_human(reason: str) -> str:
    """
    Escalate the current conversation to a human support agent, given a
    short reason (e.g. 'customer explicitly requested a human', or
    'refund dispute beyond bot authority'). Creates a support ticket and
    returns its ID and status. Always use this tool when a customer asks
    for a human, or when a request is outside the bot's allowed actions
    (order status, refunds, cancellations, product info).
    """
    ticket_id = f"TKT-{next(_ticket_counter)}"
    return f"SUCCESS: ticket_id={ticket_id}, status=created, reason='{reason}'"