from fastapi import FastAPI
from app.models.chat_request import ChatRequest
from app.models.chat_response import ChatResponse
from app.services.orchestrator import process_message

app = FastAPI()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return await process_message(request)

# --- Adicionando uvicorn para rodar diretamente ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
