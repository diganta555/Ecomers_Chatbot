"""
Terminal chat loop - same pipeline as the Streamlit app in app.py, just
without a UI. Handy for quick testing without launching a browser.
Run: python cli.py
"""

import json
from dotenv import load_dotenv

# Load OPENAI_API_KEY BEFORE importing anything that might build an
# OpenAI client at import time.
load_dotenv()

from langchain_core.messages import HumanMessage, AIMessage
from ecomers_chatbot.agent.pipeline import build_pipeline, get_response


def main():
    intent_chain, agent_executor = build_pipeline()
    chat_history: list[HumanMessage | AIMessage] = []

    print("=== AI Customer Support Agent (CLI) ===")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Agent: Thanks for reaching out. Goodbye!")
            break
        if not user_input:
            continue

        final_response = get_response(intent_chain, agent_executor, chat_history, user_input)

        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=final_response.response))

        print(json.dumps(final_response.model_dump(), indent=2))
        print(f"Agent: {final_response.response}\n")


if __name__ == "__main__":
    main()