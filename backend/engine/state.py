from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # concat new message into chat history
    messages: Annotated[List[BaseMessage], add_messages]

    # history summarization
    summary: str
    
    # Save the next agent's name
    next_node: str

    # which agent is undertaking the task
    active_agent: str