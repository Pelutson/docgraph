import httpx

from docgraph.ai.base import AiProvider, AiRequest, build_prompt
from docgraph.config import settings
from docgraph.models import Sensitivity


class OllamaProvider(AiProvider):
    name = "OllamaAIPublic"
    allowed = frozenset({Sensitivity.PUBLIC,Sensitivity.PRIVATE})
    
    
    def ask(self, request: AiRequest) -> str:
        
        self.check_allowed(request) # Guckt ob Privat oder Pulbic ist

        # 2. + 3. Prompt bauen und an Ollama schicken
        response = httpx.post(
            f"{settings.ollama_url}/api/chat",
            json={
                "model": settings.ollama_model,
                "messages": [
                    {"role": "system", "content": "Beantworte Fragen anhand der Dokumente. Antworte auf Deutsch."},
                    {"role": "user", "content": build_prompt(request)} 
                ],
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status() # So wie eine Exception

        # 4. Antworttext herausholen
        return response.json()["message"]["content"]