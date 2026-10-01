from fastapi import APIRouter, Depends
from pydantic import BaseModel

from docgraph.ai.gateway import AiAnswer, AiGateway
from docgraph.api.deps import get_ai_gateway, get_document_service
from docgraph.services.documents import DocumentService

router = APIRouter(prefix="/api/ai", tags=["ai"])


class AskBody(BaseModel):
    question: str
    document_ids: list[int] = []
    use_cloud: bool = False


@router.post("/ask")
def ask(
    body: AskBody,
    svc: DocumentService = Depends(get_document_service),
    gateway: AiGateway = Depends(get_ai_gateway),
) -> AiAnswer:
    docs = svc.get_many(body.document_ids)
    return gateway.ask(body.question, docs, use_cloud=body.use_cloud)
