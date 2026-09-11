"""
Shared agent pipeline.

Pulled out of app.py so both the CLI (cli.py, used in earlier
milestones for quick terminal testing) and the new Streamlit UI
(app.py) can build the model/agent ONCE and reuse the same
get_response() logic, instead of duplicating it.

Streamlit reruns the whole script on every interaction, so nothing
here relies on module-level mutable state (like the old global
chat_history) - chat_history is always passed in and a NEW list is
returned, and the caller (Streamlit session_state, or cli.py's local
variable) owns it.
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from ecomers_chatbot.prompts.Intent_prompt import build_intent_prompt
from ecomers_chatbot.agent.state import IntentResult, FinalResponse
from ecomers_chatbot.agent.agent import build_agent_executor, build_final_response


def build_pipeline():
    """
    Builds everything needed to answer messages: the model, the intent
    classification chain, and the tool-calling agent. Call this ONCE
    per process (Streamlit callers should wrap it in st.cache_resource).
    """
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    intent_prompt = build_intent_prompt()
    intent_chain = intent_prompt | model.with_structured_output(IntentResult)

    agent_executor = build_agent_executor(model)

    return intent_chain, agent_executor


def _fallback_response(reason: str, response_text: str) -> FinalResponse:
    """
    A safe FinalResponse to return when something upstream fails, so
    the app never crashes on a bad turn - it just tells the customer
    something went wrong and success=False shows up in logs/UI.
    """
    return FinalResponse(
        intent="GENERAL_QUERY",
        action=None,
        order_id=None,
        product_name=None,
        tool_used=False,
        success=False,
        response=response_text,
        escalate=False,
    )


def get_response(
    intent_chain,
    agent_executor,
    chat_history: list[HumanMessage | AIMessage],
    user_message: str,
) -> FinalResponse:
    """
    Runs one full turn: intent detection -> agent (which picks and
    calls tools as needed) -> structured FinalResponse. Does NOT
    mutate chat_history - the caller appends the new turn themselves
    once they have the result, keeping state ownership explicit.

    Milestone 15 - error handling: every external call that could fail
    (the API being down, malformed structured output, an unexpected
    tool exception) is caught here so the app degrades to a clear,
    friendly message instead of crashing or leaking a stack trace to
    the customer.

    NOTE: the current create_agent() API takes {"messages": [...]}
    (full message list, not a separate "input"/"chat_history" split)
    and returns {"messages": [...]} with the new turn's messages
    appended to whatever you sent in.
    """
    # --- Missing/empty input ---
    if not user_message or not user_message.strip():
        return _fallback_response(
            "empty_input",
            "It looks like your message was empty - could you type what you need help with?",
        )

    # --- Intent detection (structured output can fail: API errors,
    #     malformed/uncoercible JSON from the model, timeouts, etc.) ---
    try:
        intent_result: IntentResult = intent_chain.invoke({
            "chat_history": chat_history,
            "query": user_message,
        })
    except Exception:
        # We can't classify the message, but we can still try to help
        # generically - fall back to GENERAL_QUERY rather than failing
        # the whole turn.
        intent_result = IntentResult(intent="GENERAL_QUERY", order_id=None, product_name=None)

    # --- Agent execution (covers LLM/API failures and any unexpected
    #     exception raised inside a tool) ---
    try:
        input_messages = chat_history + [HumanMessage(content=user_message)]
        agent_result = agent_executor.invoke({"messages": input_messages})
        result_messages = agent_result["messages"]
    except Exception:
        return _fallback_response(
            "agent_failure",
            "Sorry, I ran into a problem while handling that request. "
            "Please try again in a moment, or ask to speak with a human.",
        )

    # --- Final response assembly (defensive: if the message shape is
    #     ever unexpected, don't crash the whole app over a display bug) ---
    try:
        return build_final_response(user_message, intent_result, result_messages)
    except Exception:
        return _fallback_response(
            "response_formatting_failure",
            "I found an answer but had trouble formatting the response. "
            "Please try rephrasing your question.",
        )