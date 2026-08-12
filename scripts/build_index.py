#!/usr/bin/env python3
"""Construit le site statique Droit Vivant pour GitHub Pages.

Source unique de design : ce script.
- charte partagee clair/sombre auto -> site/assets/style.css
- brief.md / source.md rendus en pages HTML stylees (Markdown -> HTML, stdlib seule)
- les .md bruts restent disponibles (utile pour NotebookLM)
- les infographies sont "re-skinnees" au build (CSS inline retire, charte appliquee)
- index redessine
Aucune dependance externe.

PLUSIEURS MODULES PAR JOUR
--------------------------
Un dossier archive/AAAA-MM-JJ/ peut contenir plusieurs modules. Ils sont
distingues par un SLUG, c'est-a-dire tout ce qui suit la date dans le nom de
fichier. Les trois fichiers d'un meme module doivent porter le meme slug :

    archive/2026-08-12/infographie-droit-2026-08-12.html          -> slug ""
    archive/2026-08-12/brief-2026-08-12.md                        -> slug ""
    archive/2026-08-12/source-notebooklm-2026-08-12.md            -> slug ""

    archive/2026-08-12/infographie-droit-2026-08-12-cyber.html    -> slug "cyber"
    archive/2026-08-12/brief-2026-08-12-cyber.md                  -> slug "cyber"
    archive/2026-08-12/source-notebooklm-2026-08-12-cyber.md      -> slug "cyber"

Le module sans slug est affiche en premier, les autres par ordre alphabetique.
L'ancien schema (un seul module par jour, sans slug) reste valide tel quel.
"""
import html, re, shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "archive"
SITE = ROOT / "site"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# --------------------------------------------------------------------------- #
#  Charte graphique partagee (clair / sombre auto)                            #
#  NB design : pas de bordure coloree gauche/haut sur les cartes (tell IA      #
#  generique). Differenciation uniquement par fond teinte + couleur de texte. #
#  Radius restreint (8px), pas de box-shadow flottante.                       #
# --------------------------------------------------------------------------- #
STYLE = """
:root{
  color-scheme: light dark;
  --bg:#ffffff; --surface:#f6f7f9; --surface-2:#eceff4;
  --text:#1b2430; --muted:#5c6675; --border:#e2e6ec;
  --accent:#1f5fcc; --accent-ink:#13408c;
  --warn-bg:#fff8ea; --warn-border:#e6c374; --warn-ink:#8a5a00;
  --mark: rgba(31,95,204,.14);
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#0f141b; --surface:#161d27; --surface-2:#1c2533;
    --text:#e7ecf3; --muted:#9aa6b5; --border:#27313f;
    --accent:#6aa6ff; --accent-ink:#a8c8ff;
    --warn-bg:#221d11; --warn-border:#574722; --warn-ink:#e6c177;
    --mark: rgba(106,166,255,.18);
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--sans);
  font-size:17px;line-height:1.7;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}

.topbar{border-bottom:1px solid var(--border);background:var(--bg)}
.topbar .inner{max-width:780px;margin:0 auto;padding:16px 22px;display:flex;
  align-items:center;justify-content:space-between;gap:14px}
.brand{font-family:var(--serif);font-weight:700;font-size:18px;color:var(--text);letter-spacing:-.01em}
.brand span{color:var(--accent)}
.topbar nav a{font-size:14px;color:var(--muted)}
.topbar nav a:hover{color:var(--accent)}

.page,.wrap{max-width:780px;margin:0 auto;padding:34px 22px 72px}

.kicker{display:inline-block;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;
  color:var(--accent-ink);font-weight:700;background:var(--surface-2);border:1px solid var(--border);
  padding:5px 12px;border-radius:999px;margin-bottom:18px}

h1{font-family:var(--serif);font-weight:700;font-size:2.05rem;line-height:1.22;
  margin:0 0 12px;letter-spacing:-.015em}
h2{font-family:var(--serif);font-weight:700;font-size:1.32rem;margin:1.9em 0 .5em;letter-spacing:-.01em}
h3{font-size:1.05rem;margin:1.5em 0 .4em}
p{margin:0 0 1.05em}

.principle{background:var(--surface);border:1px solid var(--border);
  border-radius:8px;padding:18px 22px;font-size:1.07rem;margin:26px 0}
.principle strong{color:var(--accent-ink)}

.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:24px 0}
@media(max-width:640px){.grid{grid-template-columns:1fr}}
.card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:20px 22px}
.card h2{font-family:var(--sans);font-size:.74rem;text-transform:uppercase;letter-spacing:.08em;
  color:var(--muted);margin:0 0 12px;font-weight:700}
.card.full{grid-column:1/-1}

.ref{font-size:.97rem}
.ref ul{margin:8px 0 0;padding-left:18px}
.ref li{margin-bottom:7px}
code{background:var(--surface-2);border:1px solid var(--border);border-radius:5px;
  padding:1px 6px;font-size:.85em;color:var(--accent-ink);font-family:var(--mono)}

.case b,.case strong{color:var(--text);background:linear-gradient(transparent 62%,var(--mark) 0);padding:0 1px}

.why{background:var(--warn-bg);border:1px solid var(--warn-border);
  border-radius:8px;padding:18px 22px;margin:26px 0}
.why h2{font-family:var(--sans);color:var(--warn-ink);font-size:.74rem;text-transform:uppercase;
  letter-spacing:.08em;margin:0 0 8px;font-weight:700}

.glossary dt{font-weight:700;color:var(--accent-ink);margin-top:12px}
.glossary dd{margin:2px 0 0;color:var(--muted)}

footer{margin-top:44px;padding-top:18px;border-top:1px solid var(--border);color:var(--muted);font-size:.85rem}

/* ---- index ---- */
.lede{color:var(--muted);font-size:1.02rem;margin:0 0 30px;max-width:62ch}
.entries{display:flex;flex-direction:column;gap:14px}
.entry{background:var(--surface);border:1px solid var(--border);border-radius:8px;
  padding:18px 22px}
.entry .date{font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}
.entry .date .slug{text-transform:uppercase;letter-spacing:.06em;font-size:11px;font-weight:700}
.entry h2{font-family:var(--serif);font-size:1.18rem;margin:3px 0 0;line-height:1.3;letter-spacing:-.01em}
.entry h2 a{color:var(--text)}
.entry h2 a:hover{color:var(--accent)}
.links{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.btn{font-size:13px;padding:7px 14px;border-radius:6px;text-decoration:none;
  background:var(--bg);color:var(--text);border:1px solid var(--border);transition:border-color .15s}
.btn:hover{border-color:var(--accent);text-decoration:none}
.btn.primary{background:var(--accent);color:#fff;border-color:var(--accent);font-weight:600}
@media (prefers-color-scheme: dark){.btn.primary{color:#0b1320}}
.btn.ghost{color:var(--muted);font-size:12px}

/* ---- pages MD rendues ---- */
.doc .meta{color:var(--muted);font-size:.9rem;margin:-2px 0 1.8em}
.doc ul{padding-left:22px;margin:0 0 1.05em}
.doc li{margin-bottom:.4em}
.doc h2{font-size:1.22rem}
.doc a{word-break:break-word}
""".strip()

# --------------------------------------------------------------------------- #
#  Mini-rendu Markdown (sous-ensemble maitrise, stdlib seule)                  #
# --------------------------------------------------------------------------- #
def md_inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r'(?<![">=])(https?://[^\s<)]+)',
               lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s

def md_to_html(text):
    out, para, items = [], [], []
    def flush_p():
        if para:
            out.append("<p>" + md_inline(" ".join(para).strip()) + "</p>"); para.clear()
    def flush_l():
        if items:
            out.append("<ul>" + "".join("<li>" + md_inline(x) + "</li>" for x in items) + "</ul>")
            items.clear()
    for raw in text.replace("\r\n", "\n").split("\n"):
        line = raw.rstrip()
        if not line.strip():
            flush_p(); flush_l(); continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            flush_p(); flush_l(); lvl = len(m.group(1))
            out.append(f"<h{lvl}>" + md_inline(m.group(2).strip()) + f"</h{lvl}>"); continue
        m = re.match(r"^[-*]\s+(.*)$", line)
        if m:
            flush_p(); items.append(m.group(1).strip()); continue
        flush_l(); para.append(line.strip())
    flush_p(); flush_l()
    return "\n".join(out)

def md_title(text):
    m = re.search(r"^#\s+(.*)$", text, re.M)
    if not m:
        return ""
    return re.sub(r"\*\*|`", "", m.group(1)).strip()

# --------------------------------------------------------------------------- #
#  Gabarits                                                                   #
# --------------------------------------------------------------------------- #
def topbar(prefix, nav_label="Toutes les entrées", nav_href=None):
    href = nav_href if nav_href is not None else prefix + "index.html"
    return (f'<header class="topbar"><div class="inner">'
            f'<a class="brand" href="{prefix}index.html">Droit <span>Vivant</span></a>'
            f'<nav><a href="{href}">&larr; {html.escape(nav_label)}</a></nav>'
            f'</div></header>')

def shell(title, body, prefix):
    return (f'<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f'<title>{html.escape(title)}</title>'
            f'<link rel="stylesheet" href="{prefix}assets/style.css"></head><body>'
            f'{topbar(prefix)}{body}</body></html>')

DISCLAIMER = ("Contenu pédagogique ; ne constitue pas un conseil juridique personnalisé. "
              "Droit Vivant — veille sur le droit qui se construit.")

def render_md_page(md_text, kicker, prefix, raw_md_name=None, raw_label=None):
    title = md_title(md_text) or kicker
    meta = ""
    if raw_md_name:
        meta = (f'<p class="meta"><a href="{raw_md_name}">&#8595; '
                f'{html.escape(raw_label or "Version .md brute")}</a></p>')
    body = (f'<main class="page"><span class="kicker">{html.escape(kicker)}</span>'
            f'<article class="doc">{meta}{md_to_html(md_text)}</article>'
            f'<footer>{DISCLAIMER}</footer></main>')
    return shell(title, body, prefix)

def reskin_infographie(t):
    """Retire le CSS inline et applique la charte partagee + barre de navigation."""
    t = re.sub(r"<style[^>]*>.*?</style>", "", t, flags=re.S | re.I)
    link = '<link rel="stylesheet" href="../../assets/style.css">'
    if "assets/style.css" not in t:
        if re.search(r"</head>", t, re.I):
            t = re.sub(r"</head>", link + "\n</head>", t, count=1, flags=re.I)
        else:
            t = link + t
    if re.search(r"<body[^>]*>", t, re.I):
        t = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + topbar("../../"),
                   t, count=1, flags=re.I)
    return t

# --------------------------------------------------------------------------- #
#  Collecte : un dossier de date peut contenir PLUSIEURS modules               #
# --------------------------------------------------------------------------- #
def parse_name(name):
    """Renvoie (kind, slug) pour un fichier de module, sinon None.

    kind : "infographie" | "brief" | "source"
    slug : ce qui suit la date dans le nom de fichier ("" pour le module de base)
    """
    low = name.lower()
    if low.endswith(".html") and low.startswith("infographie"):
        kind = "infographie"
    elif low.endswith(".md") and low.startswith("brief"):
        kind = "brief"
    elif low.endswith(".md") and low.startswith("source"):
        kind = "source"
    else:
        return None
    stem = name.rsplit(".", 1)[0]
    m = re.search(r"\d{4}-\d{2}-\d{2}(.*)$", stem)
    slug = (m.group(1) if m else "").strip("-_ ").lower()
    return kind, slug

def rel(p):
    return None if not p else "archive/" + str(p.relative_to(ARCHIVE)).replace("\\", "/")

def title_of(p):
    if not p:
        return ""
    t = p.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S | re.I)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    m = re.search(r"<title[^>]*>(.*?)</title>", t, re.S | re.I)
    return m.group(1).strip() if m else ""

def slug_sort_key(slug):
    """Module sans slug d'abord, puis ordre alphabetique."""
    return (1, slug) if slug else (0, "")

def collect():
    """Renvoie la liste a plat des modules, du plus recent au plus ancien."""
    modules = []
    if not ARCHIVE.exists():
        return modules
    for d in sorted(ARCHIVE.iterdir(), reverse=True):
        if not d.is_dir() or not DATE_RE.match(d.name):
            continue
        buckets = {}
        leftovers = []
        for f in sorted(d.iterdir()):
            if not f.is_file():
                continue
            parsed = parse_name(f.name)
            if not parsed:
                if f.suffix.lower() == ".html":
                    leftovers.append(f)
                continue
            kind, slug = parsed
            buckets.setdefault(slug, {}).setdefault(kind, f)
        # Repli : une infographie au nom non conventionnel devient le module de base.
        if leftovers and not any(b.get("infographie") for b in buckets.values()):
            buckets.setdefault("", {})["infographie"] = leftovers[0]
        for slug in sorted(buckets, key=slug_sort_key):
            b = buckets[slug]
            info, brief, source = b.get("infographie"), b.get("brief"), b.get("source")
            if not (info or brief or source):
                continue
            title = title_of(info)
            if not title and brief:
                title = md_title(brief.read_text(encoding="utf-8", errors="ignore"))
            modules.append({
                "date": d.name,
                "slug": slug,
                "multi": False,          # renseigne juste apres
                "title": title or d.name,
                "infographie": rel(info),
                "brief": rel(brief),
                "source": rel(source),
            })
        if len(buckets) > 1:
            for m in modules:
                if m["date"] == d.name:
                    m["multi"] = True
    return modules

# --------------------------------------------------------------------------- #
#  Index                                                                      #
# --------------------------------------------------------------------------- #
def index_entry(x):
    links = []
    if x["infographie"]:
        links.append(f'<a class="btn primary" href="{x["infographie"]}">Infographie</a>')
    if x["brief"]:
        links.append(f'<a class="btn" href="{x["brief"][:-3]}.html">Brief</a>')
    if x["source"]:
        links.append(f'<a class="btn" href="{x["source"][:-3]}.html">Source NotebookLM</a>')
        links.append(f'<a class="btn ghost" href="{x["source"]}">.md brut</a>')
    stamp = html.escape(x["date"])
    if x["multi"]:
        label = x["slug"].replace("-", " ") if x["slug"] else "module principal"
        stamp += f' · <span class="slug">{html.escape(label)}</span>'
    target = x["infographie"]
    if not target and x["brief"]:
        target = x["brief"][:-3] + ".html"
    return (f'<article class="entry"><div class="date">{stamp}</div>'
            f'<h2><a href="{target or "#"}">{html.escape(x["title"])}</a></h2>'
            f'<div class="links">{"".join(links)}</div></article>')

def build_index(modules):
    entries = "\n".join(index_entry(m) for m in modules) or "<p>Aucune entrée pour le moment.</p>"
    n_days = len({m["date"] for m in modules})
    body = (f'<main class="page"><h1>Droit Vivant</h1>'
            f'<p class="lede">Veille quotidienne sur le droit qui se construit — numérique, '
            f'libertés, IA, cybersécurité, jurisprudence française, européenne et CEDH. '
            f'Chaque entrée : une infographie, un brief court et une source longue pour podcast.</p>'
            f'<section class="entries">{entries}</section>'
            f'<footer>{len(modules)} module(s) sur {n_days} jour(s) · '
            f'mise à jour {date.today().isoformat()} · {DISCLAIMER}</footer>'
            f'</main>')
    return ("<!DOCTYPE html><html lang=\"fr\"><head><meta charset=\"UTF-8\">"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
            "<title>Droit Vivant — veille juridique</title>"
            "<link rel=\"stylesheet\" href=\"assets/style.css\"></head><body>"
            + topbar("", nav_label="Accueil", nav_href="index.html") + body + "</body></html>")

# --------------------------------------------------------------------------- #
#  Build                                                                      #
# --------------------------------------------------------------------------- #
def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)
    if ARCHIVE.exists():
        shutil.copytree(ARCHIVE, SITE / "archive")

    (SITE / "assets").mkdir(parents=True, exist_ok=True)
    (SITE / "assets" / "style.css").write_text(STYLE, encoding="utf-8")

    modules = collect()
    for x in modules:
        if x["infographie"]:
            p = SITE / x["infographie"]
            p.write_text(reskin_infographie(p.read_text(encoding="utf-8", errors="ignore")),
                         encoding="utf-8")
        if x["brief"]:
            p = SITE / x["brief"]
            (p.parent / (p.stem + ".html")).write_text(
                render_md_page(p.read_text(encoding="utf-8", errors="ignore"),
                               "Brief", "../../"), encoding="utf-8")
        if x["source"]:
            p = SITE / x["source"]
            (p.parent / (p.stem + ".html")).write_text(
                render_md_page(p.read_text(encoding="utf-8", errors="ignore"),
                               "Source NotebookLM", "../../",
                               raw_md_name=p.name,
                               raw_label="Version .md brute (pour NotebookLM)"),
                encoding="utf-8")

    (SITE / "index.html").write_text(build_index(modules), encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    n_days = len({m["date"] for m in modules})
    print(f"{len(modules)} module(s) sur {n_days} jour(s) construits.")

if __name__ == "__main__":
    main()
