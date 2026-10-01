"""Geschäftslogik für Dokumente (wie @Service in Spring).
create() und list_all() sind fertig als Vorlage - den Rest baust du nach dem Muster.
"""
from sqlmodel import Session, select

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

    # --- Schritt 2 ----------------------------------------------------------

    def get(self, doc_id: int) -> Document | None:
        # TODO(Schritt 2): Tipp -> self.session.get(Klasse, id)
        raise NotImplementedError("Schritt 2: get")

    def get_many(self, doc_ids: list[int]) -> list[Document]:
        # TODO(Schritt 2): mehrere auf einmal; Tipp -> select(...).where(Document.id.in_(...))
        raise NotImplementedError("Schritt 2: get_many")

    def delete(self, doc_id: int) -> bool:
        # TODO(Schritt 2): True wenn gelöscht, False wenn nicht gefunden.
        #   Überleg dir: Was passiert mit DocumentLinks, die auf das Doc zeigen?
        raise NotImplementedError("Schritt 2: delete")

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
