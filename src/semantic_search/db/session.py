from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from semantic_search import config
from .models import Base

psql_db_url = (
    f"postgresql:/"
    f"/{config.POSTGRES_USER}"
    f":{config.POSTGRES_PASSWORD}"
    f"@{config.POSTGRES_HOST}"
    f":{config.POSTGRES_PORT}"
    f"/{config.POSTGRES_DB}"
)

engine = create_engine(psql_db_url)
SessionLocal = sessionmaker(bind=engine)


def _setup_database() -> None:
    Base.metadata.create_all(bind=engine)