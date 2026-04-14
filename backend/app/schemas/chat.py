from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_input: str
    history: list = []
    session_id: str = "default_user"

class ChatResponse(BaseModel):
    agent_name: str
    response: str