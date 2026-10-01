"""REST-Endpunkte für Dokumente (wie @RestController)."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from docgraph.api.deps import get_document_service
from docgraph.models import DocumentCreate, DocumentRead, LinkCreate, Sensitivity
from docgraph.services.documents import DocumentService
from docgraph.services.extraction import extract_text

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("", response_model=list[DocumentRead])
def list_documents(svc: DocumentService = Depends(get_document_service)):
    return svc.list_all()


@router.post("", response_model=DocumentRead, status_code=201)
def create_document(data: DocumentCreate, svc: DocumentService = Depends(get_document_service)):
    return svc.create(data)


@router.get("/{doc_id}", response_model=DocumentRead)
def get_document(doc_id: int, svc: DocumentService = Depends(get_document_service)):
    doc = svc.get(doc_id)
    if doc is None:
        raise HTTPException(404, "Dokument nicht gefunden")
    return doc


@router.delete("/{doc_id}", status_code=204)
def delete_document(doc_id: int, svc: DocumentService = Depends(get_document_service)):
    if not svc.delete(doc_id):
        raise HTTPException(404, "Dokument nicht gefunden")


@router.post("/upload", response_model=DocumentRead, status_code=201)
async def upload_document(
    file: UploadFile,
    sensitivity: Sensitivity = Sensitivity.PRIVATE,
    svc: DocumentService = Depends(get_document_service),
):
    data = await file.read()
    try:
        text = extract_text(file.filename or "", data)
    except ValueError as e:
        raise HTTPException(415, str(e))
    doc = DocumentCreate(title=file.filename or "Unbenannt", content=text, sensitivity=sensitivity)
    return svc.create(doc, source_filename=file.filename)


@router.post("/{doc_id}/categories/{name}", response_model=DocumentRead)
def add_category(doc_id: int, name: str, svc: DocumentService = Depends(get_document_service)):
    return svc.add_category(doc_id, name)


@router.post("/{doc_id}/links", status_code=201)
def link_documents(doc_id: int, body: LinkCreate, svc: DocumentService = Depends(get_document_service)):
    return svc.link(doc_id, body.target_id, body.label)


@router.get("/{doc_id}/neighbors", response_model=list[DocumentRead])
def neighbors(doc_id: int, svc: DocumentService = Depends(get_document_service)):
    return svc.neighbors(doc_id)
