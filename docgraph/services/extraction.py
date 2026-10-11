"""Text aus hochgeladenen Dateien holen (ersetzt Apache Tika aus dem Java-Plan)."""
from io import BytesIO
from pypdf import PdfReader

def extract_text(filename: str, data: bytes) -> str:
    name = filename.lower()

    if name.endswith((".txt", ".md")):
        return data.decode("utf-8", errors="replace")

    if name.endswith(".pdf"):
        reader = PdfReader(BytesIO(data))
        texte = [seite.extract_text() for seite in reader.pages]
        return "\n".join(texte)
       

    raise ValueError(f"Dateityp nicht unterstützt: {filename}")
