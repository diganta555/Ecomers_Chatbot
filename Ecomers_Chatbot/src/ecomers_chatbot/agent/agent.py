"""
The LangChain Agent.

Milestone 11 replaces all the manual "if intent == ORDER_STATUS: call
this tool" routing from Milestones 6-10 with a real agent: we give the
model a list of tools and a system prompt, and it decides FOR ITSELF
which tool (if any) to call, based on the customer's message.

We still keep intent detection (Milestone 5) around separately - not to
route anymore, but because Milestone 13's structured final response
wants an "intent" field alongside the agent's action.
"""

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, ToolMessage
from ecomers_chatbot.tools.order_tools import get_order_status

from ecomers_chatbot.tools.refund_tools import process_refund
from ecomers_chatbot.tools.cancellation_tools import cancel_order
from ecomers_chatbot.tools.product_tools import get_product_information
from ecomers_chatbot.tools.Support_tools import escalate_to_human
from ecomers_chatbot.tools.policy_tools import  answer_policy_question


AGENT_SYSTEM_INSTRUCTION = """You are a professional customer support
agent for an e-commerce company. You have tools for checking order
status, processing refunds, cancelling orders, looking up product
information, answering policy/FAQ questions, and escalating to a
human agent.
 
Rules you must always follow:
- NEVER invent order status, refund status, cancellation status,
  product facts, or company policy. Always call the matching tool and
  base your answer only on its result.
- Use answer_policy_question for questions about refund/shipping/
  cancellation/return policy or general FAQs (e.g. "how long do
  refunds take", "can I change my address"), instead of guessing from
  general knowledge.
- If a tool result starts with NOT_FOUND, NOT_ELIGIBLE, or
  ALREADY_REFUNDED, clearly explain that to the customer - do not
  pretend the action succeeded.
- If the customer explicitly asks for a human, or their request is
  outside what your tools can do, call escalate_to_human with a short
  reason.
- If you need an order ID or product name and don't have one yet, ask
  the customer for it instead of guessing or calling a tool with
  missing information.
- For general questions or small talk that don't need a tool, just
  reply normally.
"""
 
TOOLS = [
    get_order_status,
    process_refund,
    cancel_order,
    get_product_information,
    escalate_to_human,
    answer_policy_question,
]
 
 
def build_agent_executor(model):
    """
    Builds the agent using LangChain's current create_agent() API
    (langchain>=1.0). Under the hood this is a compiled LangGraph
    graph: it takes {"messages": [...]} and loops (call model -> run
    any tool calls -> call model again) until the model replies with
    no more tool calls, then returns the full updated messages list.
    """
    return create_agent(
        model=model,
        tools=TOOLS,
        system_prompt=AGENT_SYSTEM_INSTRUCTION,
    )
 
 
def build_final_response(user_message, intent_result, result_messages):
    """
    Turns the agent's raw message list into the spec's structured
    FinalResponse shape (Milestone 13).
 
    result_messages is agent_result["messages"]: the input messages we
    sent PLUS everything the agent generated this turn (any
    ToolMessages, then the final AIMessage). Since our chat_history
    never stores ToolMessages itself, any ToolMessage present here is
    guaranteed to be from THIS turn.
    """
    from ecomers_chatbot.agent.state import FinalResponse
 
    tool_messages = [m for m in result_messages if isinstance(m, ToolMessage)]
    final_reply_text = result_messages[-1].content
 
    action = None
    tool_used = False
    success = True
    escalate = intent_result.intent == "HUMAN_SUPPORT"
 
    if tool_messages:
        tool_used = True
        last_tool_message = tool_messages[-1]
        action = last_tool_message.name
 
        content = last_tool_message.content
        if isinstance(content, str) and content.startswith(
            ("NOT_FOUND", "NOT_ELIGIBLE", "ALREADY_REFUNDED")
        ):
            success = False
 
        if action == "escalate_to_human":
            escalate = True
 
    return FinalResponse(
        intent=intent_result.intent,
        action=action,
        order_id=intent_result.order_id,
        product_name=intent_result.product_name,
        tool_used=tool_used,
        success=success,
        response=final_reply_text,
        escalate=escalate,
    )
 