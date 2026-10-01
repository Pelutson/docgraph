"""Einstiegspunkt (wie die @SpringBootApplication-Klasse).
Starten:  uvicorn docgraph.main:app --reload
UI:       http://localhost:8000/       <- static/index.html
Doku:     http://localhost:8000/docs   <- interaktive API, ersetzt curl zum Testen
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from docgraph.api import ai, documents, search
from docgraph.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Tabellen anlegen beim Start
    yield


app = FastAPI(title="docgraph", lifespan=lifespan)
app.include_router(documents.router)
app.include_router(search.router)
app.include_router(ai.router)


@app.exception_handler(NotImplementedError)
async def not_implemented(_: Request, exc: NotImplementedError):
    # Damit offene TODOs als 501 statt als kryptischer 500er auftauchen.
    return JSONResponse(status_code=501, content={"detail": f"TODO: {exc}"})


@app.get("/health")
def health():
    return {"status": "ok"}


# Oberfläche unter "/" ausliefern. MUSS als Letztes kommen, sonst schluckt
# der Mount die API-Routen (Reihenfolge = Priorität, wie Servlet-Mappings).
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
