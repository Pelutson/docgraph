from fastapi import APIRouter, Depends
from sqlmodel import Session

from docgraph.db import get_session
from docgraph.models import DocumentRead
from docgraph.services.search import search

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("", response_model=list[DocumentRead])
def search_documents(q: str, session: Session = Depends(get_session)):
    return search(session, q)
