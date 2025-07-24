from pydantic import BaseModel

class ChatRequest(BaseModel):
    pergunta: str
    session_id: str
