import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
import typesense.exceptions

from . import constants, llm, models
from .utils import typesense_utils as ts_utils
from ..db.session import setup_database
from ..db.pipeline import index_all_candidates
from ..data.seed import seed

from typing import Dict, List, Optional


def _wait_for_typesense(
    retries: int = 15,
    delay: float = 3.0
) -> None:

    for attempt in range(1, retries + 1):
        try:
            if constants.TS_CLIENT.operations.is_healthy():
                return
        except Exception:
            pass
        if attempt == retries:
            raise RuntimeError(
                f"Typesense did not become ready after {retries} attempts."
            )
        time.sleep(delay)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_database()
    _wait_for_typesense()

    for attempt in range(1, 21):
        try:
            ts_utils.generate_collection()
            break
        except (typesense.exceptions.ServiceUnavailable, Exception):
            if attempt == 20:
                raise
            time.sleep(10)

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Semantic search API — candidate discovery via RAG"}


@app.post("/seed")
async def seed_endpoint() -> Dict:
    seed()
    count = index_all_candidates()
    return {"seeded": True, "indexed": count}


@app.get("/search")
async def search_endpoint(
    user_prompt: str,
    status: Optional[str] = None,
    city: Optional[str] = None,
    category: Optional[str] = None,
    rerank: bool = False,
) -> Dict:

    search_params: Dict = {
        "q": user_prompt,
        "query_by": "search_text,embedding",
        "vector_query": f"embedding:([], alpha:{constants.HYBRID_ALPHA})",
        "prefix": False,
        "per_page": 15,
        "facet_by": "status,city,category",
    }

    filters: List[str] = []
    if status:
        filters.append(f"status:={status}")
    if city:
        filters.append(f"city:={city}")
    if category:
        filters.append(f"category:={category}")
    if filters:
        search_params["filter_by"] = " && ".join(filters)

    results: Dict = (
        constants.TS_CLIENT
        .collections[constants.CONSULTANT_SCHEMA["name"]]
        .documents.search(search_params)
    )

    hits: List[Dict] = []
    for hit in results["hits"]:
        doc: Dict = hit["document"]

        vector_distance: float = hit.get("vector_distance", 0.0)
        if vector_distance > constants.MAX_VECTOR_DISTANCE:
            continue

        hits.append({
            "id": doc["id"],
            "name": doc.get("name", ""),
            "search_text": doc["search_text"],
            "status": doc["status"],
            "city": doc.get("city", ""),
            "category": doc.get("category", ""),
            "vector_distance": round(vector_distance, 4),
        })

    if rerank and hits:
        hits = llm.rerank(
            query=user_prompt,
            hits=hits
        )

    facets: Dict = {}
    for facet in results.get("facet_counts", []):
        field = facet["field_name"]
        facets[field] = [
            {"value": c["value"], "count": c["count"]}
            for c in facet["counts"]
        ]

    return {
        "results": hits,
        "facets": facets
    }


@app.post("/chat")
async def chat_endpoint(body: models.ChatRequest) -> Dict:
    messages: List[Dict] = [constants.INITIAL_MESSAGES_STATE] + body.history
    candidates: List[Dict] = []

    if body.inject_info:
        user_query: str = str(body.history[-1]["content"])
        search_results: Dict = await search_endpoint(
            user_prompt=user_query,
            rerank=body.rerank,
        )
        candidates = search_results["results"]

        if candidates:
            candidates_text = "\n\n".join(
                f"[{hit['name']} | {hit['status']}]\n{hit['search_text']}"
                for hit in candidates
            )
            messages.append({
                "role": "user",
                "content": (
                    f"Here are the most relevant candidates retrieved from the database "
                    f"for the query above:\n\n{candidates_text}"
                ),
            })

    response: str = llm.call(messages=messages)

    return {
        "response": response,
        "candidates": candidates
    }
