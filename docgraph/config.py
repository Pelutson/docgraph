"""Zentrale Konfiguration. Werte kommen aus Umgebungsvariablen, sonst Defaults."""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DOCGRAPH_DB_URL", "sqlite:///./docgraph.db")
    sql_echo: bool = os.getenv("DOCGRAPH_SQL_ECHO", "0") == "1"  # SQL im Log anzeigen
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")
    cloud_api_key: str | None = os.getenv("CLOUD_AI_API_KEY")


settings = Settings()
