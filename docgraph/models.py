"""Datenmodell. table=True -> DB-Tabelle (wie @Entity). Ohne -> reines API-Schema (DTO)."""
from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


class Sensitivity(str, Enum):
    PUBLIC = "public"    # darf an die Cloud-KI
    PRIVATE = "private"  # NUR lokale KI


# --- Tabellen --------------------------------------------------------------

class DocumentCategoryLink(SQLModel, table=True):
    """n:m-Zwischentabelle Dokument <-> Kategorie."""
    document_id: int | None = Field(default=None, foreign_key="document.id", primary_key=True)
    category_id: int | None = Field(default=None, foreign_key="category.id", primary_key=True)


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    documents: list["Document"] = Relationship(
        back_populates="categories", link_model=DocumentCategoryLink
    )


class Document(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str = ""
    # Default ist PRIVATE: lieber aus Versehen zu vorsichtig als ein Leak.
    sensitivity: Sensitivity = Sensitivity.PRIVATE
    source_filename: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    categories: list[Category] = Relationship(
        back_populates="documents", link_model=DocumentCategoryLink
    )


class DocumentLink(SQLModel, table=True):
    """Eine Kante im Graph: source -> target (gerichtet)."""
    id: int | None = Field(default=None, primary_key=True)
    source_id: int = Field(foreign_key="document.id", index=True)
    target_id: int = Field(foreign_key="document.id", index=True)
    label: str | None = None  # z.B. "baut auf", "widerspricht"


# --- API-Schemas (Request/Response) -----------------------------------------

class DocumentCreate(SQLModel):
    title: str
    content: str = ""
    sensitivity: Sensitivity = Sensitivity.PRIVATE


class DocumentRead(SQLModel):
    id: int
    title: str
    content: str
    sensitivity: Sensitivity
    source_filename: str | None
    created_at: datetime


class LinkCreate(SQLModel):
    target_id: int
    label: str | None = None
