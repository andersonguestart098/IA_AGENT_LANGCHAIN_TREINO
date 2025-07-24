# Aqui você já tem prisma, então pode usar ele.
# Para simplificar vou usar um dicionário, mas substituímos pelo Prisma.

memory_store = {}

async def get_history(session_id: str):
    return memory_store.get(session_id, [])

async def save_message(session_id: str, pergunta: str, resposta: str):
    if session_id not in memory_store:
        memory_store[session_id] = []
    memory_store[session_id].append({"q": pergunta, "a": resposta})
