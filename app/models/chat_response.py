from pydantic import BaseModel
from typing import List, Optional

class ChatResponse(BaseModel):
    intencao: str
    resposta: str
    fonte: List[str]
    etapa: str
    slots: dict
