# 🎧 AI Customer Support Agent

An end-to-end AI customer support agent built with **LangChain** — it checks real (mock) order data before answering, calls the right tool automatically based on customer intent, answers policy questions from real documents via **RAG**, and escalates to a human ticket when it should, instead of guessing.

**🔗 Live demo:** https://ecomerschatbot-bm7tnodqnetu2njpqpzyu5.streamlit.app/
**📖 How to test it:** see [TESTING.md](TESTING.md) for example prompts

---

## What it does

- 💬 **Remembers conversation history** — mention your order ID once, ask follow-ups without repeating it
- 🧠 **Classifies customer intent** into structured categories (order status, refund, cancellation, product query, human support, general)
- 📦 **Checks real order status** against a mock database — never invents a status
- 💸 **Processes refunds** with real eligibility checks (existence, already-refunded, policy rules)
- ❌ **Cancels orders** — only allowed while an order is still `Processing`
- 🛍️ **Answers product questions** (price, stock, warranty) from a 20+ item mock catalog
- 📄 **Answers policy/FAQ questions** via RAG over real PDF documents (refund, shipping, cancellation, return policy, FAQ)
- 🎫 **Escalates to a human** and creates a real support ticket when asked or when a request is beyond its tools
- 🤖 Uses a real **LangChain agent** (`create_agent`) that decides which tool to call — no manual `if/elif` routing
- ✅ Returns a **structured internal response** (`intent`, `action`, `success`, `escalate`, etc.) alongside every reply, not just plain text
- 🛡️ **Never hallucinates transactional facts** — every order/refund/cancellation/product claim is grounded in a tool call, not the model's imagination
- 🧯 Graceful **error handling** — empty input, API failures, and malformed output all degrade to a clear message instead of crashing
- 🧪 **24 automated tests** covering tool logic, data lookups, schemas, and error handling — no API key required to run them
- 📊 Optional **LangSmith tracing** for full observability into every chain/agent/tool call

## Architecture

```
CUSTOMER
   │
   ▼
Streamlit UI (app.py)
   │
   ▼
Intent Detection (structured output)
   │
   ▼
LangChain Agent ──┬── get_order_status
                   ├── process_refund
                   ├── cancel_order
                   ├── get_product_information
                   ├── escalate_to_human
                   └── answer_policy_question ── RAG Retriever ── Knowledge Base (PDFs)
   │
   ▼
Structured Response { intent, action, success, escalate, response }
   │
   ▼
CUSTOMER
```

## How it works

Every message goes through the same pipeline: **classify intent → let the agent decide which tool (if any) to call → ground the reply in the tool's real output → return a structured response.** The agent never answers a factual/transactional question from memory — it always calls a tool first.

### Example 1: "Where is ORD-1001?"

1. **Intent detection** classifies this as `ORDER_STATUS` and extracts `order_id: "ORD-1001"`.
2. **The agent** sees the intent needs order data, so it calls the `get_order_status` tool with `"ORD-1001"`.
3. **The tool** looks up the mock database and returns a plain-text fact:
   `FOUND: Order ORD-1001 - product: iPhone 15, status: Shipped, expected/delivery date: 2026-09-13.`
4. **The model** turns that fact into a natural reply — it's only allowed to explain the tool's result, not add anything to it:
   > "Your iPhone 15 (order ORD-1001) has shipped and is expected to arrive by September 13, 2026!"
5. **The structured response** returned alongside that reply looks like:
   ```json
   {
     "intent": "ORDER_STATUS",
     "action": "get_order_status",
     "order_id": "ORD-1001",
     "tool_used": true,
     "success": true,
     "response": "Your iPhone 15 (order ORD-1001) has shipped...",
     "escalate": false
   }
   ```

If you instead ask about an order that doesn't exist (`ORD-9999`), the tool returns `NOT_FOUND: ...` and the model is instructed to relay that clearly — it never invents a status to fill the gap. That's the core design principle of this whole project: **the tool is the source of truth, the LLM is just the translator.**

### Example 2: "How long do refunds take?"

1. **Intent detection** classifies this as a policy question (not a transactional one, so no order ID is expected).
2. **The agent** recognizes this needs the knowledge base, not order data, and calls the `answer_policy_question` tool.
3. **The RAG pipeline** inside that tool: embeds the question → searches the vector store built from the policy PDFs → retrieves the top 3 most relevant chunks (in this case, from `refund_policy.pdf`).
4. **The model** answers using only those retrieved chunks as context:
   > "Refunds are typically processed automatically and confirmed right away if your order is eligible. If a physical item needs to be returned first, refunds are issued within 5-7 business days after it's received and inspected."
5. If the question can't be matched to anything in the knowledge base, the tool returns `NOT_FOUND` and the model tells the customer it doesn't have that information — instead of guessing from general knowledge about how refunds "usually" work.

## Tech stack

- **LangChain 1.0+** (`create_agent`, LCEL, structured output)
- **OpenAI** (`gpt-4o-mini` for chat, `text-embedding-3-small` for RAG)
- **Streamlit** for the chat UI
- **Pydantic** for structured schemas (intent classification, final response)
- **In-memory vector store** (`langchain_core.vectorstores.InMemoryVectorStore`) for RAG — no external vector DB needed
- **pytest** for the automated test suite
- **LangSmith** (optional) for tracing/observability

## Project structure

```
ecomers_chatbot/
├── main.py / app.py          # Streamlit entry point
├── cli.py                    # terminal version for quick testing
├── agent/
│   ├── agent.py               # builds the LangChain agent + its tools
│   ├── pipeline.py            # shared logic: intent detection + agent + error handling
│   └── state.py                # Pydantic schemas: IntentResult, FinalResponse
├── prompts/
│   ├── support_prompt.py
│   ├── intent_prompt.py
│   └── rag_prompt.py
├── tools/
│   ├── order_tools.py
│   ├── refund_tools.py
│   ├── cancellation_tools.py
│   ├── product_tools.py
│   ├── support_tools.py
│   └── policy_tools.py
├── data/
│   ├── orders.py               # mock order database (20 orders)
│   └── products.py             # mock product catalog (20+ products)
├── rag/
│   ├── loader.py
│   ├── splitter.py
│   ├── embeddings.py
│   ├── vectorstore.py
│   └── retriever.py
├── knowledge/                  # policy PDFs used for RAG
│   ├── refund_policy.pdf
│   ├── shipping_policy.pdf
│   ├── cancellation_policy.pdf
│   ├── return_policy.pdf
│   └── faq.pdf
└── tests/                       # 24 automated tests, no API key needed
```

## Getting started

### Prerequisites
- Python 3.12+
- An OpenAI API key

### Setup

```bash
git clone https://github.com/diganta555/Ecomers_Chatbot.git
cd Ecomers_Chatbot

# using uv
uv sync

# or plain pip
pip install -r requirements.txt
```

Create a `.env` file (see `.env.example`) and add your key:
```
OPENAI_API_KEY=sk-...

# optional: LangSmith tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__...
LANGCHAIN_PROJECT=ai-customer-support
```

### Run it

```bash
streamlit run app.py     # chat UI
python cli.py              # terminal version
```

### Run the tests

```bash
pytest -v
```
All 24 tests pass without needing an API key — they test tool logic, mock data, and schemas directly, not live LLM calls.

## Deployment

This project is deployed on **Streamlit Community Cloud**. To deploy your own copy: push to GitHub, create an app at [share.streamlit.io](https://share.streamlit.io) pointing at your repo, and add your secrets (`OPENAI_API_KEY`, and optionally the LangSmith variables) under Advanced Settings.

## Honest limitations

This is a **fully working prototype/MVP**, not a production system:
- Order/product data is an in-memory mock database — it resets on every restart, no real database behind it
- No authentication — anyone with the link can act on any order ID
- No persistence for chat history between sessions
- No rate limiting, structured logging, or monitoring/alerting
- Built on mock data by design — no real payment or inventory system

It's a solid demo of the full LangChain toolkit (memory, structured output, tool calling, agents, RAG, error handling, testing) — not something to point real customers or real money at yet.

## License

Add your preferred license here (e.g. MIT).
