"""Der einzige Weg zur KI. Hier wird die Privacy-Trennung ERZWUNGEN.
Controller rufen nie direkt einen Provider auf, sondern immer das Gateway.
"""
from dataclasses import dataclass

from docgraph.ai.base import AiProvider, AiRequest
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

        allowed_docs = []
        for d in docs:
            if d.sensitivity in provider.allowed:
                allowed_docs.append(d)


        withheld = len(docs) - len(allowed_docs)

        text = provider.ask(AiRequest(question, allowed_docs))
        used_ids =[]
        for d in allowed_docs:
            used_ids.append(d.id)

        return AiAnswer(text, provider.name, used_ids, withheld)

       