from __future__ import annotations

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        # normalize_embeddings improves cosine similarity behavior
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        if not isinstance(vectors, np.ndarray):
            vectors = np.asarray(vectors)
        return vectors.astype("float32").tolist()

    def embed_one(self, text: str) -> List[float]:
        return self.embed_texts([text])[0]