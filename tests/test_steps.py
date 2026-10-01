"""Deine Checkpoints. Ein Schritt ist fertig, wenn seine Tests grün sind:
    pytest -k schritt2      (nur Schritt 2)
    pytest                  (alles)
"""
from docgraph.ai.base import AiRequest
from docgraph.ai.gateway import AiGateway
from docgraph.ai.stubs import CloudStubProvider, LocalStubProvider
from docgraph.models import Document, Sensitivity
from docgraph.services.extraction import extract_text


def _make(client, title, content="", sensitivity="private"):
    r = client.post("/api/documents", json={"title": title, "content": content, "sensitivity": sensitivity})
    assert r.status_code == 201
    return r.json()


# --- Schritt 1: läuft schon ---------------------------------------------------

def test_schritt1_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_schritt1_create_and_list(client):
    _make(client, "Notiz A")
    titles = [d["title"] for d in client.get("/api/documents").json()]
    assert titles == ["Notiz A"]


def test_schritt1_default_is_private(client):
    r = client.post("/api/documents", json={"title": "x"})
    assert r.json()["sensitivity"] == "private"


# --- Schritt 2: get / delete ---------------------------------------------------

def test_schritt2_get(client):
    doc = _make(client, "Hallo")
    assert client.get(f"/api/documents/{doc['id']}").json()["title"] == "Hallo"
    assert client.get("/api/documents/9999").status_code == 404


def test_schritt2_delete(client):
    doc = _make(client, "weg damit")
    assert client.delete(f"/api/documents/{doc['id']}").status_code == 204
    assert client.get(f"/api/documents/{doc['id']}").status_code == 404
    assert client.delete("/api/documents/9999").status_code == 404


# --- Schritt 3: Upload ----------------------------------------------------------

def test_schritt3_upload_txt(client):
    r = client.post("/api/documents/upload", files={"file": ("n.txt", b"Inhalt 123", "text/plain")})
    assert r.status_code == 201
    assert r.json()["content"] == "Inhalt 123"


def test_schritt3_pdf():
    from io import BytesIO
    from pypdf import PdfWriter
    buf = BytesIO()
    w = PdfWriter()
    w.add_blank_page(width=200, height=200)
    w.write(buf)
    assert isinstance(extract_text("leer.pdf", buf.getvalue()), str)


# --- Schritt 4: Suche ---------------------------------------------------------

def test_schritt4_search(client):
    _make(client, "Spring Boot", "Java Kram")
    _make(client, "FastAPI", "Python Kram")
    hits = client.get("/api/search", params={"q": "python"}).json()
    assert [h["title"] for h in hits] == ["FastAPI"]


# --- Schritt 5: Kategorien ------------------------------------------------------

def test_schritt5_category(client, session):
    doc = _make(client, "Doc")
    assert client.post(f"/api/documents/{doc['id']}/categories/uni").status_code == 200
    client.post(f"/api/documents/{doc['id']}/categories/uni")  # zweimal -> keine Duplikate
    d = session.get(Document, doc["id"])
    assert [c.name for c in d.categories] == ["uni"]


# --- Schritt 6: Graph --------------------------------------------------------

def test_schritt6_links(client):
    a, b, c = _make(client, "A"), _make(client, "B"), _make(client, "C")
    assert client.post(f"/api/documents/{a['id']}/links", json={"target_id": b["id"]}).status_code == 201
    client.post(f"/api/documents/{c['id']}/links", json={"target_id": a["id"]})
    names = sorted(d["title"] for d in client.get(f"/api/documents/{a['id']}/neighbors").json())
    assert names == ["B", "C"]


# --- Schritt 7: Privacy-Gateway (das Wichtigste!) -----------------------------

def _docs():
    return [
        Document(id=1, title="Tagebuch", sensitivity=Sensitivity.PRIVATE),
        Document(id=2, title="Wikipedia-Notiz", sensitivity=Sensitivity.PUBLIC),
    ]


def test_schritt7_cloud_never_sees_private():
    gw = AiGateway(LocalStubProvider(), CloudStubProvider())
    ans = gw.ask("Frage", _docs(), use_cloud=True)
    assert ans.provider == "cloud-stub"
    assert ans.used_document_ids == [2]
    assert ans.withheld_count == 1
    assert "Tagebuch" not in ans.answer


def test_schritt7_local_sees_everything():
    gw = AiGateway(LocalStubProvider(), CloudStubProvider())
    ans = gw.ask("Frage", _docs(), use_cloud=False)
    assert sorted(ans.used_document_ids) == [1, 2]
    assert ans.withheld_count == 0


# --- Schritt 8: Doppelsicherung im Cloud-Provider ------------------------------

def test_schritt8_cloud_provider_refuses_private():
    import pytest
    with pytest.raises(Exception):
        CloudStubProvider().ask(AiRequest("Frage", [_docs()[0]]))
