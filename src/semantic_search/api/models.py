from pydantic import BaseModel

from typing import List, Dict, Literal


class ChatRequest(BaseModel):
    history: List[Dict]
    inject_info: bool = False
    rerank: bool = False


class RerankResult(BaseModel):
    ranked_ids: List[str]


class LLMJudgeFormat(BaseModel):
    ordinal_rank: Literal["poor", "insufficient", "sufficient", "good", "excellent"]