"""
AI Customer Support Agent
Milestone 14: Streamlit UI (+ Milestone 15: Error Handling)

Goal (per project spec):
- A usable chat interface: message history, a text input, a send
  action, and status/error displays.
- Run with: streamlit run app.py

Note: Streamlit reruns this whole script on every interaction, so all
state (chat history) lives in st.session_state, and the expensive
model/agent setup is cached with @st.cache_resource so it only runs
once per session instead of on every message.

Milestone 15: most error handling now lives in agent/pipeline.py's
get_response() (empty input, intent-detection failures, agent/API
failures) so it's shared by both this UI and cli.py. The try/except
below is a final safety net for anything unexpected that slips past
that - it should rarely trigger.
"""

import streamlit as st
from dotenv import load_dotenv

# Load OPENAI_API_KEY BEFORE importing anything that might build an
# OpenAI client - some modules construct their model at import time,
# so this must come first or you'll get a confusing "api_key must be
# set" error buried in a long stack trace.
load_dotenv()

from langchain_core.messages import HumanMessage, AIMessage
from ecomers_chatbot.agent.pipeline import build_pipeline, get_response

st.set_page_config(page_title="AI Customer Support", page_icon="🎧")


@st.cache_resource(show_spinner=False)
def get_pipeline():
    """Built once per session, not on every rerun - this is the expensive part."""
    return build_pipeline()


def render_status(final_response) -> None:
    """
    Small status line under each agent reply, per the spec's
    'useful status/error displays' requirement. Milestone 15 note:
    success=False can now happen even with tool_used=False (e.g. an
    intent-detection or agent-level failure caught in pipeline.py),
    so that case needs its own error branch too.
    """
    if final_response.escalate:
        st.warning(f"🎫 Escalated to a human agent (intent: {final_response.intent})")
    elif not final_response.success and final_response.tool_used:
        st.error(f"⚠️ {final_response.action} could not complete this request")
    elif not final_response.success:
        st.error("⚠️ Something went wrong processing this request")
    elif final_response.tool_used:
        st.caption(f"✅ used tool: `{final_response.action}`")
    else:
        st.caption(f"intent: {final_response.intent}")


def main():
    st.title("🎧 AI Customer Support Agent")
    st.caption("Ask about an order, a refund, a cancellation, a product, or our policies.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history: list[HumanMessage | AIMessage] = []
    if "display_log" not in st.session_state:
        # (role, text, final_response|None) - final_response only for assistant turns
        st.session_state.display_log = []

    # Render past turns
    for role, text, final_response in st.session_state.display_log:
        with st.chat_message(role):
            st.markdown(text)
            if final_response is not None:
                render_status(final_response)

    user_input = st.chat_input("Type your message...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.display_log.append(("user", user_input, None))

        try:
            intent_chain, agent_executor = get_pipeline()

            with st.spinner("Thinking..."):
                final_response = get_response(
                    intent_chain,
                    agent_executor,
                    st.session_state.chat_history,
                    user_input,
                )

            st.session_state.chat_history.append(HumanMessage(content=user_input))
            st.session_state.chat_history.append(AIMessage(content=final_response.response))

            with st.chat_message("assistant"):
                st.markdown(final_response.response)
                render_status(final_response)

            st.session_state.display_log.append(("assistant", final_response.response, final_response))

        except Exception as exc:
            error_text = f"Something went wrong while processing your request: {exc}"
            with st.chat_message("assistant"):
                st.error(error_text)
            st.session_state.display_log.append(("assistant", error_text, None))

    with st.sidebar:
        st.subheader("Session")
        if st.button("🗑️ Clear conversation"):
            st.session_state.chat_history = []
            st.session_state.display_log = []
            st.rerun()


if __name__ == "__main__":
    main()