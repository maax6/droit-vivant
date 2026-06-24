#!/usr/bin/env python3
"""Construit le site statique (index + copie de archive/) pour GitHub Pages. Stdlib seule."""
import html, re, shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "archive"
SITE = ROOT / "site"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def find(d, *pats):
    for p in pats:
        h = sorted(d.glob(p))
        if h: return h[0]
    return None

def rel(p):
    return None if not p else "archive/" + str(p.relative_to(ARCHIVE)).replace("\\", "/")

def title_of(p):
    if not p: return ""
    t = p.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S | re.I)
    if m: return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    m = re.search(r"<title[^>]*>(.*?)</title>", t, re.S | re.I)
    return m.group(1).strip() if m else p.parent.name

def collect():
    days = []
    if not ARCHIVE.exists(): return days
    for d in sorted(ARCHIVE.iterdir(), reverse=True):
        if not d.is_dir() or not DATE_RE.match(d.name): continue
        info = find(d, "infographie*.html", "*.html")
        days.append({"date": d.name, "title": title_of(info) or d.name,
                     "infographie": rel(info), "brief": rel(find(d, "brief*.md")),
                     "source": rel(find(d, "source-notebooklm*.md", "source*.md"))})
    return days

def card(x):
    links = []
    if x["infographie"]: links.append(f'<a class="btn primary" href="{x["infographie"]}">Infographie</a>')
    if x["brief"]: links.append(f'<a class="btn" href="{x["brief"]}">Brief</a>')
    if x["source"]: links.append(f'<a class="btn" href="{x["source"]}">Source NotebookLM</a>')
    return f'<article class="card"><div class="date">{html.escape(x["date"])}</div><h2>{html.escape(x["title"])}</h2><div class="links">{"".join(links)}</div></article>'

def build(days):
    cards = "\n".join(card(d) for d in days) or '<p>Aucune entree.</p>'
    return f'''<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Droit Vivant — veille juridique</title><style>
:root{{--bg:#0f1424;--card:#1a2236;--accent:#4f8cff;--accent2:#ffb454;--txt:#e8ecf5;--muted:#9aa6c2;--line:#2c3858}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:system-ui,sans-serif;background:var(--bg);color:var(--txt);padding:32px;max-width:960px;margin:0 auto;line-height:1.5}}
h1{{font-size:28px}}.sub{{color:var(--muted);font-size:14px;margin-bottom:24px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px}}
.card .date{{color:var(--accent2);font-size:13px;font-weight:600}}.card h2{{font-size:16px;margin:6px 0 14px}}
.links{{display:flex;flex-wrap:wrap;gap:8px}}.btn{{font-size:13px;padding:6px 12px;border-radius:8px;text-decoration:none;background:#26304b;color:var(--txt);border:1px solid var(--line)}}
.btn.primary{{background:var(--accent);color:#06122e;font-weight:600}}</style></head><body>
<h1>Droit Vivant</h1><div class="sub">Veille sur le droit qui se construit — numerique, libertes, IA, jurisprudence · {len(days)} entree(s) · maj {date.today().isoformat()}</div>
<section class="grid">{cards}</section></body></html>'''

def main():
    if SITE.exists(): shutil.rmtree(SITE)
    SITE.mkdir(parents=True)
    if ARCHIVE.exists(): shutil.copytree(ARCHIVE, SITE / "archive")
    days = collect()
    (SITE / "index.html").write_text(build(days), encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    print(f"{len(days)} jour(s).")

if __name__ == "__main__":
    main()
