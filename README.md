# docgraph (Python)

Local-first Wissenstool: Dokumente, Kategorien, Graph-Verknüpfungen, zwei KIs mit harter Privacy-Trennung.

## Setup (macOS, zsh)

```zsh
cd docgraph
python3 -m venv .venv
source .venv/bin/activate          # bei jedem neuen Terminal!
pip install -e ".[dev]"
```

**Checkpoint:** `pytest` → `4 passed, 9 failed`. Die roten sind deine Aufgaben.

## Starten

```zsh
uvicorn docgraph.main:app --reload
```

Dann http://localhost:8000/docs öffnen. Dort kannst du jeden Endpunkt direkt im Browser ausprobieren (statt curl).
Offene TODOs antworten mit `501 TODO: Schritt X`.

## Struktur

```
docgraph/
├── main.py              App + Router einhängen          (≈ @SpringBootApplication)
├── config.py            Einstellungen aus Env-Variablen  (≈ application.properties)
├── db.py                Engine + Session pro Request
├── models.py            Tabellen + API-Schemas           (≈ @Entity + DTOs)
├── api/                 HTTP-Endpunkte                   (≈ @RestController)
│   ├── deps.py          Dependency Injection             (≈ @Autowired)
│   ├── documents.py
│   ├── search.py
│   └── ai.py
├── services/            Logik                            (≈ @Service)
│   ├── documents.py     ← meiste TODOs
│   ├── extraction.py    ersetzt Apache Tika
│   └── search.py
└── ai/
    ├── base.py          AiProvider (abstrakte Klasse)
    ├── stubs.py         Platzhalter lokal/cloud
    └── gateway.py       ← erzwingt die Privacy-Trennung
```

**Regel:** Controller → Service → DB. Und KI-Aufrufe laufen *nur* über `AiGateway`, nie direkt an einen Provider.

## Fahrplan

| # | Ziel | Datei | Checkpoint |
|---|------|-------|-----------|
| 1 | Setup, App läuft | – (fertig) | `pytest -k schritt1` |
| 2 | Dokument holen/löschen | `services/documents.py` | `pytest -k schritt2` |
| 3 | PDF-Upload | `services/extraction.py` | `pytest -k schritt3` |
| 4 | Volltextsuche | `services/search.py` | `pytest -k schritt4` |
| 5 | Kategorien | `services/documents.py` | `pytest -k schritt5` |
| 6 | Graph-Verknüpfungen | `services/documents.py` | `pytest -k schritt6` |
| 7 | **Privacy-Gateway** | `ai/gateway.py` | `pytest -k schritt7` |
| 8 | Doppelsicherung Cloud | `ai/stubs.py` | `pytest -k schritt8` |
| 9 | Echtes Ollama | neu: `ai/ollama.py` (+ `deps.py` umstellen) | eigener Test |
| 10 | Echte Cloud-KI | neu: `ai/cloud.py` | eigener Test |

Danach: Frontend (die API bleibt gleich), semantische Suche mit Embeddings, Graph-Visualisierung.

Tipp: Jede Stelle zum Bearbeiten ist mit `TODO(Schritt X)` markiert → in VS Code `Cmd+Shift+F` nach `TODO(Schritt` suchen.
