"""Volltextsuche."""
from sqlmodel import Session

from docgraph.models import Document


def search(session: Session, query: str) -> list[Document]:
    # TODO(Schritt 4): Docs finden, deren title ODER content den Begriff enthält
    #   (case-insensitive). Tipp: from sqlmodel import col, or_, select
    #   col(Document.content).ilike(f"%{query}%")
    #   Später (optional): SQLite FTS5 oder semantische Suche mit Embeddings.
    raise NotImplementedError("Schritt 4: Suche")
