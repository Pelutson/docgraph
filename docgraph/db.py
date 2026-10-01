"""Datenbank-Setup. Entspricht grob DataSource + JPA-Config in Spring."""
from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

from docgraph.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.sql_echo,
    connect_args={"check_same_thread": False},  # nötig für SQLite + FastAPI
)


def init_db() -> None:
    from docgraph import models  # noqa: F401  -> Import registriert die Tabellen
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """FastAPI-Dependency: eine Session pro Request."""
    with Session(engine) as session:
        yield session
