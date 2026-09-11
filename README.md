# AI Customer Support Agent

A LangChain-based customer support agent, built incrementally milestone by milestone.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then paste your real OpenAI API key into .env
```

## Run

```bash
streamlit run app.py        # Streamlit chat UI (main deliverable)
python cli.py                # terminal version, same pipeline, for quick testing
```

## Progress

- [x] Milestone 1 — Basic LangChain Chatbot (`app.py`)
- [x] Milestone 2 — Conversation History (`app.py`)
- [x] Milestone 3 — ChatPromptTemplate (`prompts/support_prompt.py`)
- [x] Milestone 4 — LCEL Chain (`app.py`)
- [x] Milestone 5 — Intent Detection (`agent/state.py`, `prompts/intent_prompt.py`)
- [x] Milestone 6 — Order Status Tool (`data/orders.py`, `tools/order_tools.py`)
- [x] Milestone 7 — Refund Tool (`tools/refund_tools.py`)
- [x] Milestone 8 — Cancellation Tool (`tools/cancellation_tools.py`)
- [x] Milestone 9 — Product Tool (`data/products.py`, `tools/product_tools.py`)
- [x] Milestone 10 — Human Escalation (`tools/support_tools.py`)
- [x] Milestone 11 — LangChain Agent (`agent/agent.py`)
- [x] Milestone 12 — RAG Knowledge Base (`knowledge/*.txt`, `rag/`, `tools/policy_tools.py`)
- [x] Milestone 13 — Structured Final Response (`agent/state.py`, `agent/agent.py`)
- [x] Milestone 14 — Streamlit UI (`app.py`, `agent/pipeline.py`, `cli.py`)
- [ ] Milestone 15 — Error Handling
- [ ] Milestone 16 — Testing

## Note on the knowledge base

The spec names the policy files as `.pdf`. This build uses `.txt` files
of the same names/content instead - same RAG pipeline, no extra PDF
dependency needed for local setup. To use real PDFs, swap `PyPDFLoader`
into `rag/loader.py` for each file in `knowledge/` and drop the `.txt`
files in favor of `.pdf` ones.