"""Platzhalter-Provider. Kein echtes LLM - nur um die Architektur zu beweisen.
Später durch OllamaProvider (Schritt 9) und CloudProvider (Schritt 10) ersetzen.
"""
from docgraph.ai.base import AiProvider, AiRequest
from docgraph.models import Sensitivity


class LocalStubProvider(AiProvider):
    name = "local-stub"
    allowed = frozenset({Sensitivity.PUBLIC, Sensitivity.PRIVATE})

    def ask(self, request: AiRequest) -> str:
        titles = [d.title for d in request.context_docs]
        return f"[local-stub] Frage: {request.question!r} | Kontext: {titles}"


class CloudStubProvider(AiProvider):
    name = "cloud-stub"
    allowed = frozenset({Sensitivity.PUBLIC})

    def ask(self, request: AiRequest) -> str:
        # TODO(Schritt 8): Zweite Sicherung ("defense in depth").
        #   Auch wenn das Gateway filtert: Wenn hier trotzdem ein PRIVATE-Dokument
        #   ankommt, sofort eine Exception werfen statt es zu verarbeiten.
        titles = [d.title for d in request.context_docs]
        return f"[cloud-stub] Frage: {request.question!r} | Kontext: {titles}"
