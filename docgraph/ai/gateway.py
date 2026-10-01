"""Der einzige Weg zur KI. Hier wird die Privacy-Trennung ERZWUNGEN.
Controller rufen nie direkt einen Provider auf, sondern immer das Gateway.
"""
from dataclasses import dataclass

from docgraph.ai.base import AiProvider
from docgraph.models import Document


@dataclass
class AiAnswer:
    answer: str
    provider: str
    used_document_ids: list[int]
    withheld_count: int  # wie viele Docs rausgefiltert wurden


class AiGateway:
    def __init__(self, local: AiProvider, cloud: AiProvider):
        self.local = local
        self.cloud = cloud

    def ask(self, question: str, docs: list[Document], use_cloud: bool) -> AiAnswer:
        provider = self.cloud if use_cloud else self.local

        # TODO(Schritt 7): Das ist der wichtigste Teil des Projekts.
        #   1. docs aufteilen: erlaubt = d.sensitivity in provider.allowed, Rest = verboten
        #   2. AiRequest NUR mit den erlaubten Docs bauen
        #   3. provider.ask(...) aufrufen
        #   4. AiAnswer zurückgeben (used_document_ids, withheld_count befüllen)
        #   Checkpoint: pytest -k schritt7
        raise NotImplementedError("Schritt 7: Privacy-Filter im AiGateway")
