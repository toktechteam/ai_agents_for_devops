from __future__ import annotations

from typing import Any, Dict, List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest


class QdrantVectorStore:
    def __init__(self, url: str, collection: str):
        self.client = QdrantClient(url=url)
        self.collection = collection

    def ensure_collection(self, vector_size: int) -> None:
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection for c in collections)

        if exists:
            info = self.client.get_collection(self.collection)
            existing_size = info.config.params.vectors.size  # type: ignore
            if existing_size != vector_size:
                raise ValueError(
                    f"Collection '{self.collection}' exists with vector size {existing_size}, "
                    f"but model produces {vector_size}. Use a new collection name."
                )
            return

        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=rest.VectorParams(
                size=vector_size,
                distance=rest.Distance.COSINE,
            ),
        )

    def upsert_points(self, points: List[rest.PointStruct]) -> None:
        self.client.upsert(collection_name=self.collection, points=points)

    def search(
        self,
        query_vector: List[float],
        limit: int = 5,
        score_threshold: Optional[float] = None,
        filter_: Optional[rest.Filter] = None,
    ) -> List[Dict[str, Any]]:
        hits = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=filter_,
            with_payload=True,
        )
        out: List[Dict[str, Any]] = []
        for h in hits:
            out.append(
                {
                    "id": h.id,
                    "score": h.score,
                    "payload": h.payload or {},
                }
            )
        return out