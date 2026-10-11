"""Geschäftslogik für Dokumente (wie @Service in Spring).
create() und list_all() sind fertig als Vorlage - den Rest baust du nach dem Muster.
"""
from sqlmodel import Session, select,or_

from docgraph.models import Category, Document, DocumentCreate, DocumentLink


class DocumentService:
    def __init__(self, session: Session):
        self.session = session

    # --- fertig (Vorlage) ---------------------------------------------------

    def create(self, data: DocumentCreate, source_filename: str | None = None) -> Document:
        doc = Document.model_validate(data, update={"source_filename": source_filename})
        self.session.add(doc)
        self.session.commit()
        self.session.refresh(doc)  # holt die von der DB vergebene id
        return doc

    def list_all(self) -> list[Document]:
        return list(self.session.exec(select(Document)).all())


    def get(self, doc_id: int) -> Document | None:
        return self.session.get(Document,doc_id)

    def get_many(self, doc_ids: list[int]) -> list[Document]:
        stmt = select(Document).where(Document.id.in_(doc_ids))
        return  list(self.session.exec(stmt).all())
   

    def delete(self, doc_id: int) -> bool:
        
        doc = self.get(doc_id)
        if doc is None:
            return False
        
        stmt = select(DocumentLink).where(or_(DocumentLink.source_id == doc_id, DocumentLink.target_id == doc_id)) #Baut eine SQL Bedingung
        
        links = self.session.exec(stmt).all()
        
        for link in links:
            self.session.delete(link)
            
        self.session.delete(doc)
        self.session.commit()
        return True
       

    # --- Schritt 5: Kategorien ----------------------------------------------

    def add_category(self, doc_id: int, category_name: str) -> Document:
        # TODO(Schritt 5): Kategorie per Name suchen oder neu anlegen,
        #   dann an doc.categories anhängen und committen.
        raise NotImplementedError("Schritt 5: add_category")

    # --- Schritt 6: Graph ---------------------------------------------------

    def link(self, source_id: int, target_id: int, label: str | None = None) -> DocumentLink:
        # TODO(Schritt 6): Beide Docs müssen existieren, kein Self-Link, kein Duplikat.
        raise NotImplementedError("Schritt 6: link")

    def neighbors(self, doc_id: int) -> list[Document]:
        # TODO(Schritt 6): alle Docs, die mit doc_id verbunden sind (beide Richtungen).
        raise NotImplementedError("Schritt 6: neighbors")
