from app.services.nlu import classify_intent, extract_slots
from app.services.rag import search_docs
from app.services.memory import get_history, save_message
from app.utils.observability import log_interaction
from langchain_mistralai import ChatMistralAI
import os

llm = ChatMistralAI(
    model="mistral-large-latest",
    api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0.3
)


async def process_message(request):
    pergunta = request.pergunta
    session_id = request.session_id

    # 1. Entendimento
    intencao = await classify_intent(pergunta)
    slots = await extract_slots(pergunta)
    history = await get_history(session_id)

    # 2. Busca (RAG)
    docs = await search_docs(pergunta)
    context = "\n".join([doc.page_content for doc in docs])

    # 3. Resposta com LLM
    resposta_prompt = f"""
Histórico: {history}
Documentos: {context}
Pergunta: {pergunta}

Responda de forma cordial e direta:
"""
    resposta = await llm.ainvoke(resposta_prompt)

    # 4. Salvar memória
    await save_message(session_id, pergunta, resposta.content)

    # 5. Observabilidade
    await log_interaction(pergunta, resposta.content, intencao, slots, docs)

    return {
        "intencao": intencao,
        "resposta": resposta.content,
        "fonte": list({doc.metadata.get("source", "desconhecido") for doc in docs}),
        "etapa": "MEIO",
        "slots": slots
    }
