import csv
import time

from fastapi import FastAPI
from pathlib import Path
from contextlib import asynccontextmanager

from typesense.exceptions import ServiceUnavailable

from . import typesense_utils as ts_utils
from .. import llm, constants
from semantic_search.db.session import _setup_database

from typing import Dict, List


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    _setup_database()
    _wait_for_typesense()

    for attempt in range(1, 21):
        try:
            ts_utils.generate_collection()
            break
        except (ServiceUnavailable, Exception):
            if attempt == 20:
                raise
            time.sleep(10)

    yield


def extract_consultant_data(
    csv_path: Path,
) -> List[Dict]:
    
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f=f)
        data = []
        for row in reader:
            data.append(row)

    return data


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