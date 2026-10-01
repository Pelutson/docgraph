// Gemeinsamer Code für alle Seiten: Navigation, API-Aufrufe, Toasts, Fortschritt.

const $ = (sel) => document.querySelector(sel);

const PAGES = [
  ["index.html", "Dokumente"],
  ["graph.html", "Graph"],
  ["ki.html", "KI fragen"],
];

// Kopfzeile + Toast in jede Seite einbauen
function renderHeader() {
  const here = location.pathname.split("/").pop() || "index.html";
  const nav = PAGES.map(([href, label]) =>
    `<a href="${href}" class="${href === here ? "active" : ""}">${label}</a>`).join("");
  document.body.insertAdjacentHTML("afterbegin", `
    <header>
      <h1>docgraph</h1>
      <nav>${nav}</nav>
      <div id="progress" title="Welche Schritte antworten schon (kein 501 mehr)?"></div>
      <a href="/docs" target="_blank" class="meta">API-Doku</a>
    </header>`);
  document.body.insertAdjacentHTML("beforeend", '<div id="toast"></div>');
}

function toast(msg, kind = "") {
  const t = $("#toast");
  t.textContent = msg;
  t.className = "show " + kind;
  clearTimeout(t._timer);
  t._timer = setTimeout(() => (t.className = ""), 3500);
}

// fetch-Wrapper: wirft bei Fehlern und übersetzt 501 in "Noch nicht gebaut: Schritt X"
async function api(path, options = {}) {
  const res = await fetch(path, options);
  if (res.status === 204) return null;
  const body = await res.json().catch(() => null);
  if (!res.ok) {
    const detail = body && typeof body.detail === "string" ? body.detail : JSON.stringify(body?.detail ?? res.statusText);
    const err = new Error(res.status === 501 ? "Noch nicht gebaut – " + detail.replace(/^TODO:\s*/, "") : `${res.status}: ${detail}`);
    err.status = res.status;
    throw err;
  }
  return body;
}

function showError(e) {
  toast(e.message, e.status === 501 ? "todo" : "error");
}

const json = (data) => ({ headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

// Fortschritt: fragt harmlose Endpunkte ab. 501 = noch TODO, alles andere = gebaut.
// Schritt 3, 5 und 8 lassen sich so nicht prüfen -> dafür pytest.
async function loadProgress() {
  const probe = async (path, options) => (await fetch(path, options)).status !== 501;
  const checks = [
    ["2", () => probe("/api/documents/0")],
    ["4", () => probe("/api/search?q=x")],
    ["6", () => probe("/api/documents/0/neighbors")],
    ["7", () => probe("/api/ai/ask", { method: "POST", ...json({ question: "ping", document_ids: [] }) })],
  ];
  const el = $("#progress");
  for (const [step, check] of checks) {
    const ok = await check().catch(() => false);
    el.insertAdjacentHTML("beforeend", `<span class="chip ${ok ? "done" : "todo"}">Schritt ${step} ${ok ? "✓" : "…"}</span>`);
  }
}

renderHeader();
loadProgress();
