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
