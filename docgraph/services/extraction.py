"""Text aus hochgeladenen Dateien holen (ersetzt Apache Tika aus dem Java-Plan)."""


def extract_text(filename: str, data: bytes) -> str:
    name = filename.lower()

    if name.endswith((".txt", ".md")):
        return data.decode("utf-8", errors="replace")

    if name.endswith(".pdf"):
        # TODO(Schritt 3): Mit pypdf den Text aller Seiten extrahieren.
        #   Tipp: from io import BytesIO; from pypdf import PdfReader
        #         PdfReader(BytesIO(data)).pages -> page.extract_text()
        raise NotImplementedError("Schritt 3: PDF-Extraktion")

    raise ValueError(f"Dateityp nicht unterstützt: {filename}")
