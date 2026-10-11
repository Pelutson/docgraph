"""Volltextsuche."""
from sqlmodel import Session,col, or_,select

from docgraph.models import Document


def search(session: Session, query: str) -> list[Document]:
    
    muster  = f"%{query}%"
    bedingung1 = col(Document.content).ilike(muster)
    bedingung2 = col(Document.title).ilike(muster)    
    return list(session.exec(select(Document).where(or_(bedingung1,bedingung2))).all())


