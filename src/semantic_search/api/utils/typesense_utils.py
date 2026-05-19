from . import main_utils as m_utils
from .. import constants

from pathlib import Path

import typesense.exceptions
from typesense import Client

from typing import Dict, List

def create_api_key(
    client: Client = constants.TS_CLIENT,
) -> Dict:

    key = client.keys.create({
        "description": "Admin key.",
        "actions": ["*"],
        "collections": ["*"]
    })

    return key


def create_collection(
    schema: Dict,
    client: Client,
) -> None:
    client.collections.create(schema=schema)
    return None


def delete_collection(
    schema: str,
    client: Client,
) -> None:
    client.collections[schema].delete()


def upsert_documents(
    doc: Dict,
    schema: str,
    client: Client,
) -> None:
    
    client.collections[schema].documents.upsert(
        document=doc
    )

    return None


def setup_typesense_collections(
    data: List[Dict],
) -> None:

    for entry in data:
        search_text: str = (
            f"{entry['candidate']} is a {entry['function_name']} "
            f"in {entry['function_group']}, based in {entry['residence']}. "
            f"Age: {entry['age']}."
        )

        doc = {
            "id": entry["cv"],
            "search_text": search_text,
            "status": entry["status"],
        }

        upsert_documents(
            doc=doc,
            schema=constants.CONSULTANT_SCHEMA["name"],
            client=constants.TS_CLIENT,
        )

    return None


def generate_collection(
    client: Client = constants.TS_CLIENT,
) -> None:
    """Create the Typesense collection, or patch new fields into an existing one."""
    try:
        create_collection(schema=constants.CONSULTANT_SCHEMA, client=client)
    except typesense.exceptions.ObjectAlreadyExists:
        # Collection exists — attempt to add any new facet fields.
        existing = client.collections[constants.CONSULTANT_SCHEMA["name"]].retrieve()
        existing_names = {f["name"] for f in existing.get("fields", [])}
        new_fields = [
            f for f in constants.SCHEMA_PATCH_FIELDS
            if f["name"] not in existing_names
        ]
        if new_fields:
            client.collections[constants.CONSULTANT_SCHEMA["name"]].update(
                {"fields": new_fields}
            )