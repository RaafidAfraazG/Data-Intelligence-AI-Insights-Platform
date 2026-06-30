"""
app/embeddings/vector_store.py
================================
ChromaDB vector store wrapper.

ChromaDB runs embedded (like SQLite) — no separate server process needed.
All data is persisted to the `chroma_db/` directory at the project root.

Collections:
  - "products"  — one document per product
  - "reviews"   — one document per review

Usage:
    store = VectorStore("products")
    store.insert(id="42", text="Gaming Laptop RTX 4070", embedding=[...], metadata={...})
    results = store.search(query_embedding=[...], n_results=5)
"""

import logging
from typing import Any

from app.config.settings import settings
from app.config.constants import CHROMA_PRODUCTS_COLLECTION, CHROMA_REVIEWS_COLLECTION

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Thin wrapper around a ChromaDB collection.
    Provides insert, update (upsert), delete, and similarity search.
    """

    def __init__(self, collection_name: str) -> None:
        """
        Parameters
        ----------
        collection_name : str
            The ChromaDB collection to use. Typically 'products' or 'reviews'.
        """
        self.collection_name = collection_name
        self._client = None
        self._collection = None

    def _get_collection(self):
        """Lazy-initialise the ChromaDB client and collection."""
        if self._collection is None:
            try:
                import chromadb

                self._client = chromadb.PersistentClient(path=settings.CHROMA_DIR)
                self._collection = self._client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"},  # Use cosine similarity
                )
                logger.info(
                    "ChromaDB collection '%s' ready (path=%s).",
                    self.collection_name,
                    settings.CHROMA_DIR,
                )
            except ImportError:
                logger.error("chromadb is not installed. Run: pip install chromadb")
            except Exception as exc:
                logger.error("Failed to initialise ChromaDB: %s", exc)
        return self._collection

    # ── Write Operations ──────────────────────────────────────────────────────

    def insert(
        self,
        doc_id: str,
        text: str,
        embedding: list[float],
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """
        Add a new document to the collection.

        Parameters
        ----------
        doc_id : str      — unique identifier (e.g. str(product.id))
        text : str        — the original text (stored for retrieval)
        embedding : list  — pre-computed embedding vector
        metadata : dict   — extra fields (name, category, price, etc.)

        Returns True on success.
        """
        collection = self._get_collection()
        if collection is None or not embedding:
            return False

        try:
            collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[metadata or {}],
            )
            return True
        except Exception as exc:
            logger.error("ChromaDB insert failed for id=%s: %s", doc_id, exc)
            return False

    def update(
        self,
        doc_id: str,
        text: str,
        embedding: list[float],
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """
        Upsert (insert or replace) a document.
        Safe to call even if the document doesn't exist yet.
        """
        collection = self._get_collection()
        if collection is None or not embedding:
            return False

        try:
            collection.upsert(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[metadata or {}],
            )
            return True
        except Exception as exc:
            logger.error("ChromaDB upsert failed for id=%s: %s", doc_id, exc)
            return False

    def delete(self, doc_id: str) -> bool:
        """Remove a document from the collection by ID."""
        collection = self._get_collection()
        if collection is None:
            return False

        try:
            collection.delete(ids=[doc_id])
            return True
        except Exception as exc:
            logger.error("ChromaDB delete failed for id=%s: %s", doc_id, exc)
            return False

    # ── Read / Search ─────────────────────────────────────────────────────────

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 10,
        where: dict | None = None,
    ) -> list[dict[str, Any]]:
        """
        Find the most similar documents to a query embedding.

        Parameters
        ----------
        query_embedding : list[float]  — embedding of the search query
        n_results : int                — how many results to return
        where : dict | None            — optional metadata filter

        Returns
        -------
        list[dict]
            Each dict: { id, text, metadata, distance }
            Sorted by similarity (closest first).
        """
        collection = self._get_collection()
        if collection is None or not query_embedding:
            return []

        try:
            kwargs: dict = {
                "query_embeddings": [query_embedding],
                "n_results": min(n_results, collection.count() or 1),
                "include": ["documents", "metadatas", "distances"],
            }
            if where:
                kwargs["where"] = where

            result = collection.query(**kwargs)

            items = []
            for i, doc_id in enumerate(result["ids"][0]):
                items.append({
                    "id": doc_id,
                    "text": result["documents"][0][i],
                    "metadata": result["metadatas"][0][i],
                    "distance": round(result["distances"][0][i], 4),
                })
            return items

        except Exception as exc:
            logger.error("ChromaDB search failed: %s", exc)
            return []

    def count(self) -> int:
        """Return the number of documents in the collection."""
        collection = self._get_collection()
        if collection is None:
            return 0
        try:
            return collection.count()
        except Exception:
            return 0


# ── Convenience instances ─────────────────────────────────────────────────────
# Import these instead of constructing VectorStore every time.
product_store = VectorStore(CHROMA_PRODUCTS_COLLECTION)
review_store = VectorStore(CHROMA_REVIEWS_COLLECTION)
