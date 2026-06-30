"""
app/embeddings/__init__.py
"""
from app.embeddings.embedding_service import get_embedding, get_batch_embeddings
from app.embeddings.vector_store import VectorStore

__all__ = ["get_embedding", "get_batch_embeddings", "VectorStore"]
