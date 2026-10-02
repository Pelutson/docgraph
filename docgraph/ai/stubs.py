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
        self.check_allowed(request) #Hier wird geprüft, ob der Provider auf die Sensitivitätsstufen der Dokumente zugreifen darf.
        titles = [d.title for d in request.context_docs]
        return f"[cloud-stub] Frage: {request.question!r} | Kontext: {titles}"
    
       
        