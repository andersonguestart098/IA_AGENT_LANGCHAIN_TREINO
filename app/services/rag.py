from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from app.services.embeddings import embedding_model

qdrant_client = QdrantClient(url="http://localhost:6333")
vectorstore = QdrantVectorStore(
    client=qdrant_client,
    collection_name="cemear_knowledge_base",
    embedding=embedding_model,
)

async def search_docs(query: str, k: int = 5):
    docs = vectorstore.similarity_search(query=query, k=k)
    return docs
