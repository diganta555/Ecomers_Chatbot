"""
Reusable support prompt template.
 
Milestone 3 goal: pull the prompt out of app.py into its own module so it
can be imported anywhere (the agent, tests, etc.) instead of being rebuilt
inline. This is also the first place we treat the prompt as something with
named *variables* ("chat_history", "query") rather than a hardcoded string.
"""


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

SYSTEM_INSTRUCTION="You are a professional customer support agent."

def build_support_prompt()-> ChatPromptTemplate:
    """
     Returns a ChatPromptTemplate with two variables that must be supplied
    at call time:
      - chat_history: list[BaseMessage]  (past turns, via MessagesPlaceholder)
      - query: str                       (the newest user message)
    """

    return ChatPromptTemplate.from_messages([
        ('system',SYSTEM_INSTRUCTION),
        MessagesPlaceholder(variable_name='chat_history'),
        ("human", "{query}"),
    ])