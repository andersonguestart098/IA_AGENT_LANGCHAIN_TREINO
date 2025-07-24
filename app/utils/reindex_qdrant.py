import os
import json
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_community.vectorstores import Qdrant
from langchain_core.documents import Document
from app.services.embeddings import embedding_model

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = "cemear_knowledge_base"

# Carrega documentos originais
with open("base_cemear.json", "r", encoding="utf-8") as f:
    docs = json.load(f)

# Conecta ao Qdrant
client = QdrantClient(url=QDRANT_URL)

# Cria nova coleção (768 dims)
client.recreate_collection(
    collection_name=QDRANT_COLLECTION,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)

# Prepara documentos
documents = [Document(page_content=d["conteudo"], metadata=d) for d in docs]

# Upload para Qdrant
Qdrant.from_documents(
    documents=documents,
    embedding=embedding_model,
    url=QDRANT_URL,
    collection_name=QDRANT_COLLECTION,
)

print(f"Reindexação concluída: {len(documents)} documentos inseridos.")
