from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.config import settings
from app.embeddings import EmbeddingModel
from app.qdrant_store import QdrantVectorStore
from qdrant_client.http import models as rest

DATA_PATH = Path(__file__).parent / "data" / "runbooks.json"

app = FastAPI(title="Lab 03.1 - Vector Similarity Search API", version="1.0.0")

embedder = EmbeddingModel(settings.embed_model)
store = QdrantVectorStore(settings.qdrant_url, settings.qdrant_collection)


class IngestResponse(BaseModel):
    collection: str
    inserted: int


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: int = Field(default=5, ge=1, le=20)
    score_threshold: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    service: Optional[str] = None
    severity: Optional[str] = None


class SearchHit(BaseModel):
    id: Any
    score: float
    title: str
    service: str
    severity: str
    content: str


class SearchResponse(BaseModel):
    query: str
    top_k: int
    hits: List[SearchHit]


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest", response_model=IngestResponse)
def ingest() -> IngestResponse:
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="runbooks.json not found")

    runbooks: List[Dict[str, Any]] = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    texts = [f"{rb['title']}\n{rb['content']}" for rb in runbooks]

    vectors = embedder.embed_texts(texts)
    vector_size = len(vectors[0])
    store.ensure_collection(vector_size)

    points: List[rest.PointStruct] = []
    for idx, (rb, v) in enumerate(zip(runbooks, vectors), start=1):
        payload = {
            "title": rb["title"],
            "service": rb["service"],
            "severity": rb["severity"],
            "content": rb["content"],
        }
        points.append(
            rest.PointStruct(
                id=idx,
                vector=v,
                payload={**payload, "doc_id": rb["id"]},
            )
        )

    store.upsert_points(points)
    return IngestResponse(collection=settings.qdrant_collection, inserted=len(points))


@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest) -> SearchResponse:
    qvec = embedder.embed_one(req.query)

    conditions: List[rest.FieldCondition] = []
    if req.service:
        conditions.append(
            rest.FieldCondition(
                key="service", match=rest.MatchValue(value=req.service)
            )
        )
    if req.severity:
        conditions.append(
            rest.FieldCondition(
                key="severity", match=rest.MatchValue(value=req.severity)
            )
        )

    filter_ = rest.Filter(must=conditions) if conditions else None

    results = store.search(
        query_vector=qvec,
        limit=req.top_k,
        score_threshold=req.score_threshold,
        filter_=filter_,
    )

    hits: List[SearchHit] = []
    for r in results:
        p = r["payload"]
        hits.append(
            SearchHit(
                id=r["id"],
                score=float(r["score"]),
                title=str(p.get("title", "")),
                service=str(p.get("service", "")),
                severity=str(p.get("severity", "")),
                content=str(p.get("content", "")),
            )
        )

    return SearchResponse(query=req.query, top_k=req.top_k, hits=hits)
