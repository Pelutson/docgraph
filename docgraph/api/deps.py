"""Dependency Injection (ersetzt @Autowired). FastAPI ruft diese Funktionen pro Request."""
from fastapi import Depends
from sqlmodel import Session

from docgraph.ai.gateway import AiGateway
#from docgraph.ai.stubs import CloudStubProvider, LocalStubProvider
from docgraph.db import get_session
from docgraph.services.documents import DocumentService
from docgraph.ai.ollama import OllamaProvider


def get_document_service(session: Session = Depends(get_session)) -> DocumentService:
    return DocumentService(session)


_gateway = AiGateway(local=OllamaProvider(), cloud=OllamaProvider()) # cloud muss noch geaendert werden


def get_ai_gateway() -> AiGateway:
    # Schritt 9/10: hier die Stubs gegen echte Provider tauschen - sonst nirgends!
    return _gateway
