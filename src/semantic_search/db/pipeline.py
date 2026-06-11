from datetime import date

from sqlalchemy.orm import joinedload

from ..api import constants
from ..api.utils.typesense_utils import upsert_documents
from .models import Candidate
from .session import SessionLocal

from typing import Dict, List

def _format_date_range(
    start_date: date,
    end_date: date,
) -> str:
    s = str(start_date.year) if start_date else "?"
    e_yr = str(end_date.year) if end_date else "present"
    return f"[{s}-{e_yr}]"


def _format_education(
    education: List[str]
) -> List[str]:

    parts: List[str] = ["\nEducation:"]
    for edu in sorted(
        education,
        key=lambda e: e.start_date or date.min,
        reverse=True,
    ):
        tokens: List[str] = []

        if edu.degree:
            tokens.append(edu.degree)
        if edu.school:
            tokens.append(f"at {edu.school}")
        if edu.city:
            tokens.append(f"({edu.city})")
        if edu.start_date or edu.end_date:
            tokens.append(_format_date_range(edu.start_date, edu.end_date))
        line = "  - " + " ".join(tokens)
        if edu.comments:
            line += f"\n    {edu.comments}"
        parts.append(line)
    return parts


def _format_work_experience(
    work_experience: List[str]
) -> List[str]:

    parts: List[str] = ["\nWork Experience:"]
    for exp in sorted(
        work_experience,
        key=lambda e: e.start_date or date.min,
        reverse=True,
    ):
        tokens: List[str] = []

        if exp.title:
            tokens.append(exp.title)
        if exp.company_name:
            tokens.append(f"at {exp.company_name}")
        if exp.start_date or exp.end_date:
            tokens.append(_format_date_range(exp.start_date, exp.end_date))
        line = "  - " + " ".join(tokens)
        if exp.comments:
            line += f"\n    {exp.comments}"
        parts.append(line)
    return parts


def build_candidate_search_text(
    candidate: Candidate
) -> str:

    name: str = (
        f"{candidate.first_name or ''}"
        f" {candidate.last_name or ''}".strip()
    )
    parts: List[str] = [name]

    if candidate.status:
        parts.append(f"Status: {candidate.status}")
    if candidate.address_city:
        parts.append(f"Location: {candidate.address_city}")

    if candidate.category:
        parts.append(f"Category: {candidate.category}")
    if candidate.skill_id:
        parts.append(f"Skills: {candidate.skill_id}")

    if candidate.education:
        parts.extend(_format_education(candidate.education))

    if candidate.work_experience:
        parts.extend(_format_work_experience(candidate.work_experience))

    return "\n".join(parts)


def index_all_candidates() -> int:
    with SessionLocal() as session:
        candidates: List[Candidate] = (
            session.query(Candidate)
            .options(
                joinedload(Candidate.education),
                joinedload(Candidate.work_experience),
            )
            .all()
        )

        count = 0
        for candidate in candidates:
            name: str = f"{candidate.first_name or ''} {candidate.last_name or ''}".strip()
            search_text: str = build_candidate_search_text(candidate=candidate)

            doc: Dict = {
                "id": candidate.external_id,
                "search_text": search_text,
                "name": name,
                "status": candidate.status or "",
                "city": candidate.address_city or "",
                "category": candidate.category or "",
            }

            upsert_documents(
                doc=doc,
                schema=constants.CONSULTANT_SCHEMA["name"],
                client=constants.TS_CLIENT,
            )

            count += 1

    return count
