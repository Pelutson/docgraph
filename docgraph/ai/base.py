"""Das Herzstück der Privacy-Trennung. Entspricht dem AiProvider-Interface aus dem Java-Plan.

ABC = Abstract Base Class, quasi ein Java-Interface / C++-Klasse mit pure virtual.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from docgraph.models import Document, Sensitivity


@dataclass
class AiRequest:
    question: str
    context_docs: list[Document] = field(default_factory=list)


class AiProvider(ABC):
    name: str
    # Welche Sensitivitätsstufen dieser Provider sehen DARF.
    allowed: frozenset[Sensitivity]

    @abstractmethod
    def ask(self, request: AiRequest) -> str:
        """Frage + (bereits gefilterte) Kontext-Dokumente -> Antworttext."""
