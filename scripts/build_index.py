#!/usr/bin/env python3
"""Construit le site statique Droit Vivant pour GitHub Pages.

Source unique de design : ce script.
- charte partagee clair/sombre auto -> site/assets/style.css
- brief.md / source.md rendus en pages HTML stylees (Markdown -> HTML, stdlib seule)
- les .md bruts restent disponibles (utile pour NotebookLM)
- les infographies sont "re-skinnees" au build (CSS inline retire, charte appliquee)
- index redessine : cartes hierarchisees, recherche client, chronologie mensuelle
Aucune dependance externe (stdlib seule au build, aucun CDN cote client).

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

MOTS-CLES (tags)
----------------
Trois sources cumulatives, toutes optionnelles, du plus precis au plus degrade :

  1. ligne explicite du brief :  **Mots-cles :** #rgpd #cjue #action-de-groupe
     (les deux ecritures sont acceptees : `**Mots-cles :** #a #b` et
      `**Mots-cles : #a #b**`, cette derniere calquee sur la ligne Theme)
  2. ligne `**Theme : ...**` du brief, segmentee puis slugifiee
  3. categorie du `.kicker` de l'infographie (`Droit Vivant - <categorie> - <date>`)

Aucun module d'archive n'a besoin d'etre retouche : le niveau 3 sert de filet.
"""
import calendar, html, json, re, shutil, unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "archive"
SITE = ROOT / "site"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

MOIS = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre")
MOIS_COURT = ("janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.",
              "août", "sept.", "oct.", "nov.", "déc.")

TAGS_VISIBLES = 12      # taille du nuage avant repli dans <details>
TAGS_PAR_CARTE = 3
EXCERPT_MAX = 220

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
[hidden]{display:none !important}

.topbar{border-bottom:1px solid var(--border);background:var(--bg)}
.topbar .inner{max-width:780px;margin:0 auto;padding:16px 22px;display:flex;
  align-items:center;justify-content:space-between;gap:14px}
.brand{font-family:var(--serif);font-weight:700;font-size:18px;color:var(--text);letter-spacing:-.01em}
.brand span{color:var(--accent)}
.topbar nav a{font-size:14px;color:var(--muted)}
.topbar nav a:hover{color:var(--accent)}

.page,.wrap{max-width:780px;margin:0 auto;padding:34px 22px 72px}

.kicker,.wrap .tag{display:inline-block;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;
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

/* ---- replis : classes heritees des toutes premieres infographies ---- */
.ref,.refs{font-size:.97rem}
.refs ul{margin:8px 0 0;padding-left:18px}
.refs li{margin-bottom:7px}
.wrap dl{margin:0}
.wrap dl dt{font-weight:700;color:var(--accent-ink);margin-top:12px}
.wrap dl dd{margin:2px 0 0;color:var(--muted)}
.gloss-grid{display:grid;gap:12px;margin-top:4px}
.term b{display:block;color:var(--accent-ink)}
.term span{display:block;color:var(--muted)}
.pills{display:flex;flex-wrap:wrap;gap:7px;margin:20px 0}
.pill{display:inline-flex;align-items:center;font-size:.85rem;line-height:1.35;
  padding:5px 12px;border-radius:999px;border:1px solid var(--border);background:var(--surface)}
.pill.yes{color:var(--accent-ink)}
.pill.no{color:var(--muted)}
.verdict{display:inline-block;margin-top:10px;font-size:.82rem;color:var(--muted);
  border:1px solid var(--border);border-radius:999px;padding:3px 11px;background:var(--bg)}
.wrap .sub{color:var(--muted);font-size:1.04rem;margin:-2px 0 4px}
.wrap .date{color:var(--muted);font-size:.92rem;margin:-2px 0 6px}

/* ---- index : en-tete ---- */
.lede{color:var(--muted);font-size:1.02rem;margin:0 0 26px;max-width:62ch}

/* ---- index : barre de recherche ---- */
.toolbar{margin:0 0 18px}
.search{display:flex;gap:8px;align-items:stretch}
.search__field{position:relative;flex:1;display:flex}
.search input[type=search]{width:100%;font:inherit;font-size:15px;color:var(--text);
  background:var(--surface);border:1px solid var(--border);border-radius:8px;
  padding:11px 38px 11px 14px;appearance:none;-webkit-appearance:none}
.search input[type=search]::-webkit-search-cancel-button{display:none}
.search input[type=search]::placeholder{color:var(--muted)}
.search input[type=search]:focus{border-color:var(--accent);outline:none;
  box-shadow:0 0 0 2px var(--mark)}
.search__clear{position:absolute;right:6px;top:50%;transform:translateY(-50%);
  background:none;border:0;color:var(--muted);font:inherit;font-size:19px;line-height:1;
  padding:4px 8px;cursor:pointer;border-radius:6px}
.search__clear:hover{color:var(--text)}
.search__opts{display:flex;align-items:center;gap:7px;margin:9px 0 0;
  font-size:13px;color:var(--muted);flex-wrap:wrap}
.search__opts input{accent-color:var(--accent);margin:0}
.search__opts label{display:inline-flex;align-items:center;gap:7px;cursor:pointer}
.hint{color:var(--muted);font-size:12.5px}
.hint code{font-size:.9em;padding:0 4px}
.nojs{background:var(--warn-bg);border:1px solid var(--warn-border);color:var(--warn-ink);
  border-radius:8px;padding:10px 14px;font-size:13.5px;margin:10px 0 0}

/* ---- index : nuage de tags ---- */
.tags{margin:0 0 18px}
.tags__list{display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0;list-style:none}
.tags .tag{display:inline-flex;align-items:baseline;gap:5px;font-size:12.5px;line-height:1;
  padding:6px 10px;border-radius:999px;border:1px solid var(--border);
  background:var(--surface);color:var(--muted);white-space:nowrap}
.tags .tag:hover{border-color:var(--accent);color:var(--accent);text-decoration:none}
.tag__n{font-size:11px;font-variant-numeric:tabular-nums;opacity:.7}
.tags .tag.is-active{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
@media (prefers-color-scheme: dark){.tags .tag.is-active{color:#0b1320}}
.tags .tag.is-active .tag__n{opacity:.85}
.tags details{margin-top:8px}
.tags summary{font-size:12.5px;color:var(--muted);cursor:pointer;width:fit-content}
.tags summary:hover{color:var(--accent)}
.tags details .tags__list{margin-top:8px}

/* ---- index : navigation par mois ---- */
.monthnav{display:flex;gap:6px;overflow-x:auto;padding:2px 0 8px;margin:0 0 6px;
  scrollbar-width:thin}
.monthnav a{flex:0 0 auto;font-size:12.5px;padding:5px 10px;border-radius:6px;
  border:1px solid var(--border);background:var(--bg);color:var(--muted);white-space:nowrap;
  font-variant-numeric:tabular-nums}
.monthnav a:hover{border-color:var(--accent);color:var(--accent);text-decoration:none}
.monthnav a.is-empty{opacity:.35}
.monthnav b{font-weight:600;color:var(--text)}
.monthnav a.is-empty b{color:var(--muted)}

/* ---- index : compteur + etat vide ---- */
.status{display:flex;align-items:baseline;justify-content:space-between;gap:12px;
  flex-wrap:wrap;border-top:1px solid var(--border);padding-top:12px;margin:0 0 6px;
  font-size:13px;color:var(--muted)}
.status__n{font-variant-numeric:tabular-nums}
.status__reset{font-size:13px}
.empty{background:var(--surface);border:1px solid var(--border);border-radius:8px;
  padding:22px;margin:18px 0;text-align:center;color:var(--muted)}
.empty b{color:var(--text);font-weight:600}

/* ---- index : chronologie ---- */
.year{font-family:var(--sans);font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--muted);font-weight:700;margin:34px 0 0;padding-bottom:6px;
  border-bottom:1px solid var(--border);font-variant-numeric:tabular-nums}
.month{margin:0 0 10px}
.month__head{position:sticky;top:0;z-index:3;background:var(--bg);margin:0;
  padding:12px 0 8px;display:flex;align-items:baseline;justify-content:space-between;gap:10px;
  font-family:var(--sans);font-size:.95rem;font-weight:700;letter-spacing:0}
.month__name{text-transform:capitalize}
.month__count{font-size:12px;font-weight:400;color:var(--muted);font-variant-numeric:tabular-nums}
.strip{display:grid;grid-template-columns:repeat(31,1fr);gap:3px;list-style:none;
  margin:0 0 16px;padding:0}
.strip li{aspect-ratio:1/1;min-height:7px}
.strip__c{display:block;width:100%;height:100%;border-radius:2px;
  border:1px solid var(--border);background:transparent}
.strip__c--on{border-color:transparent;background:var(--accent);opacity:.45}
.strip__c--multi{opacity:1}
a.strip__c:hover{opacity:1;outline:1px solid var(--accent);outline-offset:1px}
.strip__c.is-off{opacity:.12}
.strip__c--out{visibility:hidden}

.entries{display:flex;flex-direction:column;gap:12px;margin:0 0 26px}

/* ---- index : carte ---- */
.entry{position:relative;background:var(--surface);border:1px solid var(--border);
  border-radius:8px;padding:16px 20px 14px;scroll-margin-top:74px}
.month{scroll-margin-top:8px}
.entry:hover{border-color:var(--muted)}
@supports selector(:has(*)){
  .entry:has(.entry__open:focus-visible){outline:2px solid var(--accent);outline-offset:2px}
  .entry .entry__open:focus-visible{outline:none}
}
.entry__meta{display:flex;align-items:center;flex-wrap:wrap;gap:8px;
  font-size:12.5px;color:var(--muted);margin:0 0 6px}
.entry__meta time{font-variant-numeric:tabular-nums;font-weight:600;color:var(--text)}
.entry__cat{color:var(--muted)}
.entry__sep{opacity:.5}
.entry__slug{text-transform:uppercase;letter-spacing:.06em;font-size:10.5px;font-weight:700;
  color:var(--accent-ink);background:var(--surface-2);border:1px solid var(--border);
  border-radius:999px;padding:2px 8px}
.entry__title{font-family:var(--serif);font-size:1.16rem;font-weight:700;line-height:1.34;
  letter-spacing:-.01em;margin:0;color:var(--text);text-wrap:balance;
  display:-webkit-box;-webkit-line-clamp:6;-webkit-box-orient:vertical;overflow:hidden}
/* les accroches font 8 a 42 mots : le clamp est un garde-fou, pas un recadrage.
   En colonne etroite il faut plus de lignes pour ne pas amputer la chute. */
@media (max-width:560px){.entry__title{-webkit-line-clamp:10;font-size:1.1rem}}
.entry__tags{display:flex;flex-wrap:wrap;gap:4px 10px;margin:9px 0 0;padding:0;list-style:none;
  position:relative;z-index:1;line-height:1.4}
.entry__tags li{display:flex;line-height:1.4}
.entry__tag{font-size:11.5px;color:var(--muted);background:none;border:0;padding:0;
  font-family:inherit;cursor:pointer;line-height:1.4}
.entry__tag:hover{color:var(--accent);text-decoration:underline}
.entry__actions{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:13px 0 0}
.btn{font-size:13px;padding:7px 14px;border-radius:6px;text-decoration:none;
  background:var(--bg);color:var(--text);border:1px solid var(--border);transition:border-color .15s}
.btn:hover{border-color:var(--accent);text-decoration:none}
.btn.primary{background:var(--accent);color:#fff;border-color:var(--accent);font-weight:600}
@media (prefers-color-scheme: dark){.btn.primary{color:#0b1320}}
.btn.ghost{color:var(--muted);font-size:12px}
.entry__open::after{content:"";position:absolute;inset:0;border-radius:8px}
.entry__actions > :not(.entry__open){position:relative;z-index:1}
.res{margin-left:auto;font-size:12.5px}
.res>summary{list-style:none;cursor:pointer;color:var(--muted);padding:7px 2px;
  display:inline-flex;align-items:center;gap:5px}
.res>summary::-webkit-details-marker{display:none}
.res>summary::after{content:"›";display:inline-block;transition:transform .15s;font-size:14px}
.res[open]>summary::after{transform:rotate(90deg)}
.res>summary:hover{color:var(--accent)}
.res__body{display:flex;flex-direction:column;align-items:flex-start;gap:2px;
  padding:8px 0 2px}
.res__body a{color:var(--muted);font-size:12.5px}
.res__body a:hover{color:var(--accent)}
@media (max-width:520px){
  .res{margin-left:0}
  .entry__actions{gap:6px}
  .btn{padding:7px 12px}
}

/* ---- pages MD rendues ---- */
.doc .meta{color:var(--muted);font-size:.9rem;margin:-2px 0 1.8em}
.doc ul{padding-left:22px;margin:0 0 1.05em}
.doc li{margin-bottom:.4em}
.doc h2{font-size:1.22rem}
.doc a{word-break:break-word}
""".strip()

# --------------------------------------------------------------------------- #
#  Normalisation (indispensable en francais : accents replies, minuscules)     #
# --------------------------------------------------------------------------- #
def fold(s):
    """Minuscules + diacritiques replies : « données » -> « donnees »."""
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower()

def slugify(s):
    s = fold(s).replace("'", " ").replace("’", " ")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def squash(s):
    return re.sub(r"\s+", " ", s or "").strip()

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

def md_plain(text):
    """Markdown -> texte nu (pour extraits et index plein texte)."""
    t = text.replace("\r\n", "\n")
    t = re.sub(r"^\s{0,3}#{1,6}\s+", " ", t, flags=re.M)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"[*_`>#\[\]]", " ", t)
    t = re.sub(r"^\s*[-–—]\s+", " ", t, flags=re.M)
    return squash(t)

# --------------------------------------------------------------------------- #
#  Extraction des mots-cles                                                    #
# --------------------------------------------------------------------------- #
# Separateurs de segments dans une ligne « Theme » ou une categorie de kicker.
TAG_SPLIT = re.compile(r"[·—–‒/,;:()\[\]«»\"]|\s-\s|\bet\b|&|\+")
# Mots vides a rogner aux bords d'un segment avant slugification.
TAG_EDGE = ("de la ", "de l' ", "de l'", "des ", "du ", "de ", "d'", "la ", "le ",
            "les ", "l'", "aux ", "au ", "en ", "un ", "une ")
TAG_STOP = {"", "et", "ou", "de", "du", "des", "la", "le", "les", "un", "une",
            "en", "au", "aux", "d", "l", "sur", "pour", "par", "dans"}
TAG_MAX_MOTS = 4

def _clean_part(part):
    part = part.strip(" . …'’\"")
    low = fold(part)
    for pref in TAG_EDGE:
        if low.startswith(pref):
            part = part[len(pref):].lstrip(); low = fold(part); break
    return part.strip(" .'’")

def tags_from_text(text):
    """Segmente un libelle libre (Theme, categorie) en tags exploitables."""
    found = []
    for part in TAG_SPLIT.split(text or ""):
        part = _clean_part(part)
        if not part:
            continue
        if len([w for w in part.split() if w]) > TAG_MAX_MOTS:
            continue
        s = slugify(part)
        # rejette les fragments d'enumeration (« articles 28, 33 et 34 ») et le bruit
        if (not s or s in TAG_STOP or len(s) < 2
                or s[0].isdigit() or re.fullmatch(r"articles?-\d+", s)):
            continue
        if s not in found:
            found.append(s)
    return found

KEYWORDS_RE = re.compile(
    r"^\s*\*\*\s*mots-cles\s*:\s*\*{0,2}\s*(.+?)\s*\*{0,2}\s*$", re.M)
THEME_RE = re.compile(
    r"^\s*\*\*\s*theme\s*:\s*\*{0,2}\s*(.+?)\s*\*{0,2}\s*$", re.M)

def _line_value(regex, md_text):
    """Cherche la ligne dans une copie repliee, renvoie le texte d'origine."""
    lines = (md_text or "").replace("\r\n", "\n").split("\n")
    for raw in lines:
        m = regex.match(fold(raw))
        if m:
            # meme position dans la ligne d'origine (fold preserve la longueur)
            return raw[m.start(1):m.end(1)].strip("* ").strip()
    return ""

def explicit_keywords(md_text):
    """Ligne `**Mots-cles :** #a #b` -> ['a','b'] (optionnelle)."""
    raw = _line_value(KEYWORDS_RE, md_text)
    if not raw:
        return []
    out = []
    for m in re.finditer(r"#([a-z0-9\-]+)", fold(raw)):
        t = m.group(1).strip("-")
        if t and t not in out:
            out.append(t)
    if out:
        return out
    # tolerance : mots-cles ecrits sans dieses, separes par des virgules
    return tags_from_text(raw)

def theme_of(md_text):
    return _line_value(THEME_RE, md_text)

def kicker_of(html_text):
    m = re.search(r'class="[^"]*\bkicker\b[^"]*"[^>]*>(.*?)</', html_text or "", re.S | re.I)
    if not m:
        return ""
    return squash(html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))))

def short_category(label):
    """Libelle court pour la carte : le domaine, sans le sous-titre qui suit un
    tiret cadratin (« Donnees personnelles — violation de donnees, droit a
    reparation… » -> « Donnees personnelles »). Le texte complet reste indexe."""
    parts = [p.strip() for p in re.split(r"[—–]", label or "")]
    head = parts[0].strip(" ·,;:") if parts else ""
    return head or squash(label)

def kicker_category(kicker):
    """`Droit Vivant · <categorie> · <date>` -> segments de categorie."""
    segs = [s.strip() for s in (kicker or "").split("·") if s.strip()]
    if segs and slugify(segs[0]) == "droit-vivant":
        segs = segs[1:]
    return [s for s in segs if not re.search(r"\b(19|20)\d{2}\b", s)]

def excerpt_of(md_text):
    """Premier paragraphe utile du brief, tronque proprement."""
    body = []
    for raw in (md_text or "").replace("\r\n", "\n").split("\n"):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        low = fold(line)
        if low.startswith("**theme") or low.startswith("**mots-cles"):
            continue
        body.append(line)
        break
    txt = md_plain(" ".join(body))
    if len(txt) <= EXCERPT_MAX:
        return txt
    cut = txt[:EXCERPT_MAX].rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:.’'") + "…"

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
    return ensure_wrap(t)

def ensure_wrap(t):
    """Les toutes premieres infographies n'ont pas de conteneur .wrap : sans lui,
    le contenu colle au bord de la fenetre. On en ajoute un si besoin (aucune
    classe n'est renommee, le contrat reste intact)."""
    if re.search(r'class="[^"]*\b(?:wrap|page)\b', t, re.I):
        return t
    head = re.search(r"</header>", t, re.I)
    tail = re.search(r"</body>", t, re.I)
    if not head or not tail or tail.start() <= head.end():
        return t
    return (t[:head.end()] + '\n<div class="wrap">'
            + t[head.end():tail.start()] + '</div>\n' + t[tail.start():])

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

def read(p):
    return p.read_text(encoding="utf-8", errors="ignore") if p else ""

def title_of(p):
    if not p:
        return ""
    t = read(p)
    m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S | re.I)
    if m:
        return squash(html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))))
    m = re.search(r"<title[^>]*>(.*?)</title>", t, re.S | re.I)
    return squash(html.unescape(m.group(1))) if m else ""

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
            brief_txt = read(brief)
            title = title_of(info)
            if not title and brief_txt:
                title = md_title(brief_txt)

            # --- categorie et mots-cles : trois niveaux cumulatifs, tous optionnels
            kicker = kicker_of(read(info))
            cat_segs = kicker_category(kicker)
            theme = theme_of(brief_txt)
            category_full = " · ".join(cat_segs)
            if not category_full and theme:
                category_full = theme
            category = short_category(category_full)
            tags = []
            for t in (explicit_keywords(brief_txt)
                      + tags_from_text(theme)
                      + tags_from_text(" · ".join(cat_segs))):
                if t and t not in tags:
                    tags.append(t)

            modules.append({
                "date": d.name,
                "slug": slug,
                "multi": False,          # renseigne juste apres
                "title": title or d.name,
                "infographie": rel(info),
                "brief": rel(brief),
                "source": rel(source),
                "category": squash(category),
                "category_full": squash(category_full),
                "tags": tags,
                "excerpt": excerpt_of(brief_txt),
                "_brief_path": brief,
                "_source_path": source,
            })
        if len(buckets) > 1:
            for m in modules:
                if m["date"] == d.name:
                    m["multi"] = True
    return modules

# --------------------------------------------------------------------------- #
#  Index : helpers de presentation                                             #
# --------------------------------------------------------------------------- #
def module_id(x):
    return x["date"] + ("-" + x["slug"] if x["slug"] else "")

def module_url(x):
    """Cible principale : l'infographie, a defaut le brief, a defaut la source."""
    if x["infographie"]:
        return x["infographie"]
    for k in ("brief", "source"):
        if x[k]:
            return x[k][:-3] + ".html"
    return ""

def fr_day(iso):
    y, m, d = (int(v) for v in iso.split("-"))
    return ("1er" if d == 1 else str(d)) + " " + MOIS[m - 1]

def fr_month(ym):
    y, m = (int(v) for v in ym.split("-"))
    return f"{MOIS[m - 1]} {y}"

def plural(n, one, many=None):
    return f"{n} {one if n <= 1 else (many or one + 's')}"

def entry_card(x):
    mid = module_id(x)
    url = module_url(x)
    label = html.escape(x["title"], quote=True)
    meta = [f'<time datetime="{x["date"]}">{fr_day(x["date"])}</time>']
    if x["category"]:
        meta.append('<span class="entry__sep">·</span>'
                    f'<span class="entry__cat">{html.escape(x["category"])}</span>')
    if x["multi"]:
        lab = x["slug"].replace("-", " ") if x["slug"] else "module principal"
        meta.append(f'<span class="entry__slug">{html.escape(lab)}</span>')

    tags = "".join(
        f'<li><button type="button" class="entry__tag" data-tag="{html.escape(t, quote=True)}">'
        f'#{html.escape(t)}</button></li>'
        for t in x["tags"][:TAGS_PAR_CARTE])
    tags = f'<ul class="entry__tags">{tags}</ul>' if tags else ""

    actions = []
    if x["infographie"]:
        actions.append(f'<a class="btn primary entry__open" href="{x["infographie"]}" '
                       f'aria-label="Infographie — {label}">Infographie</a>')
    if x["brief"]:
        cls = "btn" if x["infographie"] else "btn primary entry__open"
        actions.append(f'<a class="{cls}" href="{x["brief"][:-3]}.html" '
                       f'aria-label="Brief — {label}">Brief</a>')
    res = []
    if x["source"]:
        res.append(f'<a href="{x["source"][:-3]}.html">Source NotebookLM (page)</a>')
        res.append(f'<a href="{x["source"]}" download>Fichier source pour NotebookLM (.md)</a>')
    if x["brief"]:
        res.append(f'<a href="{x["brief"]}" download>Texte du brief (.md)</a>')
    if res:
        actions.append('<details class="res"><summary>Ressources</summary>'
                       f'<div class="res__body">{"".join(res)}</div></details>')

    return (f'<article class="entry" id="e-{mid}" data-id="{mid}" data-day="{x["date"]}">'
            f'<div class="entry__meta">{"".join(meta)}</div>'
            f'<h4 class="entry__title">{html.escape(x["title"])}</h4>'
            f'{tags}'
            f'<div class="entry__actions">{"".join(actions)}</div>'
            f'</article>')

def month_strip(ym, by_day):
    """Bande calendaire : un carre par jour du mois, rempli s'il y a un module."""
    y, m = (int(v) for v in ym.split("-"))
    ndays = calendar.monthrange(y, m)[1]
    cells = []
    for d in range(1, 32):
        if d > ndays:
            cells.append('<li><span class="strip__c strip__c--out" aria-hidden="true"></span></li>')
            continue
        iso = f"{ym}-{d:02d}"
        mods = by_day.get(iso, [])
        if not mods:
            cells.append(f'<li><span class="strip__c" data-day="{iso}" '
                         f'title="{fr_day(iso)} — aucune publication"></span></li>')
            continue
        cls = "strip__c strip__c--on" + (" strip__c--multi" if len(mods) > 1 else "")
        lab = f'{fr_day(iso)} {y} — {plural(len(mods), "module")}'
        cells.append(f'<li><a class="{cls}" data-day="{iso}" href="#e-{module_id(mods[0])}" '
                     f'title="{html.escape(lab, quote=True)}" '
                     f'aria-label="{html.escape(lab, quote=True)}"></a></li>')
    return (f'<ol class="strip" aria-label="Cadence de publication — {fr_month(ym)}">'
            + "".join(cells) + "</ol>")

def tag_chip(tag, n, extra=""):
    return (f'<li><a class="tag{extra}" href="?tag={tag}" data-tag="{tag}">'
            f'#{html.escape(tag)}<span class="tag__n">{n}</span></a></li>')

# --------------------------------------------------------------------------- #
#  Index : script de recherche (inline, aucune dependance)                     #
# --------------------------------------------------------------------------- #
SEARCH_JS = r"""
(function () {
  var root = document.getElementById('dv');
  if (!root) return;
  var data = {};
  try { data = JSON.parse(document.getElementById('dv-data').textContent); } catch (e) { return; }

  var input    = document.getElementById('q');
  var clearBtn = document.getElementById('q-clear');
  var ftBox    = document.getElementById('ft');
  var ftNote   = document.getElementById('ft-note');
  var count    = document.getElementById('count');
  var reset    = document.getElementById('reset');
  var empty    = document.getElementById('empty');
  var emptyQ   = document.getElementById('empty-q');
  var cards    = Array.prototype.slice.call(root.querySelectorAll('.entry'));
  var months   = Array.prototype.slice.call(root.querySelectorAll('.month'));
  var years    = Array.prototype.slice.call(root.querySelectorAll('.year'));
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.monthnav a'));
  var tagLinks = Array.prototype.slice.call(document.querySelectorAll('.tag[data-tag]'));

  var fullText = null;      // chargé paresseusement
  var ftState  = 'idle';    // idle | loading | ready | error
  var active   = [];        // tags actifs
  var query    = '';        // texte libre (déjà replié)

  function fold(s) {
    return (s || '').normalize('NFD').replace(/\p{Mn}/gu, '').toLowerCase();
  }

  /* ---- lecture / écriture de l'état dans l'URL ---- */
  function readURL() {
    var p = new URLSearchParams(location.search);
    var t = (p.get('tag') || '').split(',').map(function (s) { return s.trim(); })
              .filter(Boolean);
    active = t;
    input.value = p.get('q') || '';
    if (p.get('ft') === '1' && ftBox) { ftBox.checked = true; loadFullText(); }
  }
  function writeURL(push) {
    var p = new URLSearchParams();
    var q = input.value.trim();
    if (q) p.set('q', q);
    if (active.length) p.set('tag', active.join(','));
    if (ftBox && ftBox.checked) p.set('ft', '1');
    var s = p.toString();
    var url = location.pathname + (s ? '?' + s : '') + location.hash;
    try { history[push ? 'pushState' : 'replaceState'](null, '', url); } catch (e) {}
  }

  /* ---- texte intégral, chargé à la demande ---- */
  function ftFailed() {
    ftState = 'error';
    note('Texte intégral indisponible (page ouverte hors serveur web ?). ' +
         'La recherche porte sur les titres, mots-clés et résumés.');
  }
  function loadFullText() {
    if (ftState === 'loading' || ftState === 'ready') return;
    if (typeof fetch !== 'function') { ftFailed(); return; }
    ftState = 'loading';
    note('Chargement du texte intégral…');
    try {
      fetch('search-fulltext.json')
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (j) { fullText = j; ftState = 'ready'; note(''); apply(false); })
        .catch(function () { ftFailed(); apply(false); });
    } catch (e) { ftFailed(); }
  }
  function note(msg) {
    if (!ftNote) return;
    ftNote.textContent = msg;
    ftNote.hidden = !msg;
  }

  /* ---- correspondance ---- */
  function hay(id) {
    var rec = data[id];
    if (!rec) return '';
    var h = rec.h || '';
    if (ftBox && ftBox.checked && ftState === 'ready' && fullText && fullText[id]) {
      h += ' ' + fullText[id];
    }
    return h;
  }
  function matches(id, tags) {
    var rec = data[id];
    if (!rec) return false;
    for (var i = 0; i < tags.length; i++) {
      if ((rec.g || []).indexOf(tags[i]) === -1) return false;
    }
    if (!query) return true;
    var h = hay(id);
    var words = query.split(/\s+/).filter(Boolean);
    for (var j = 0; j < words.length; j++) {
      if (h.indexOf(words[j]) === -1) return false;
    }
    return true;
  }

  /* ---- application du filtre ---- */
  function apply(push) {
    var raw = input.value;
    var free = [];
    var typed = [];
    raw.split(/\s+/).forEach(function (tok) {
      if (!tok) return;
      if (tok.charAt(0) === '#' && tok.length > 1) {
        typed.push(fold(tok.slice(1)).replace(/[^a-z0-9-]+/g, '-').replace(/^-|-$/g, ''));
      } else { free.push(fold(tok)); }
    });
    /* les # saisis s'ajoutent aux tags cliqués, sans les écraser :
       `active` reste l'état des puces du nuage, `typed` vit dans le champ. */
    var all = active.slice();
    typed.forEach(function (t) { if (t && all.indexOf(t) === -1) all.push(t); });
    query = free.join(' ');

    var n = 0, perMonth = {}, perDay = {};
    cards.forEach(function (card) {
      var ok = matches(card.getAttribute('data-id'), all);
      card.hidden = !ok;
      if (ok) {
        n++;
        var d = card.getAttribute('data-day');
        perDay[d] = (perDay[d] || 0) + 1;
        var ym = d.slice(0, 7);
        perMonth[ym] = (perMonth[ym] || 0) + 1;
      }
    });

    months.forEach(function (sec) {
      var ym = sec.getAttribute('data-month');
      var c = perMonth[ym] || 0;
      sec.hidden = c === 0;
      var badge = sec.querySelector('.month__count');
      if (badge) {
        badge.textContent = c + (c > 1 ? ' modules' : ' module');
      }
      Array.prototype.forEach.call(sec.querySelectorAll('.strip__c'), function (cell) {
        var d = cell.getAttribute('data-day');
        if (!d) return;
        cell.classList.toggle('is-off', !perDay[d]);
      });
    });
    years.forEach(function (h) {
      var y = h.getAttribute('data-year'), any = false;
      months.forEach(function (sec) {
        if (sec.getAttribute('data-month').slice(0, 4) === y && !sec.hidden) any = true;
      });
      h.hidden = !any;
    });
    navLinks.forEach(function (a) {
      a.classList.toggle('is-empty', !perMonth[a.getAttribute('data-month')]);
    });
    tagLinks.forEach(function (a) {
      a.classList.toggle('is-active', active.indexOf(a.getAttribute('data-tag')) !== -1);
      a.setAttribute('aria-pressed', active.indexOf(a.getAttribute('data-tag')) !== -1);
    });

    var filtering = !!(query || active.length || typed.length);
    count.textContent = n + (n > 1 ? ' modules' : ' module')
      + (filtering ? ' sur ' + cards.length : '');
    reset.hidden = !filtering;
    empty.hidden = n !== 0;
    if (n === 0) {
      emptyQ.textContent = [raw.trim(), active.map(function (t) { return '#' + t; }).join(' ')]
        .filter(Boolean).join(' ');
    }
    clearBtn.hidden = !raw;
    writeURL(!!push);
  }

  /* ---- interactions ---- */
  input.addEventListener('input', function () { apply(false); });
  input.form.addEventListener('submit', function (e) { e.preventDefault(); apply(true); });
  clearBtn.addEventListener('click', function () {
    input.value = ''; active = []; apply(true); input.focus();
  });
  reset.addEventListener('click', function (e) {
    e.preventDefault(); input.value = ''; active = []; apply(true);
  });
  if (ftBox) {
    ftBox.addEventListener('change', function () {
      if (ftBox.checked) { loadFullText(); } else { note(''); }
      apply(true);
    });
  }
  function toggleTag(tag, push) {
    var i = active.indexOf(tag);
    if (i === -1) { active.push(tag); } else { active.splice(i, 1); }
    apply(push !== false);
  }
  tagLinks.forEach(function (a) {
    a.setAttribute('role', 'button');
    a.addEventListener('click', function (e) {
      e.preventDefault(); toggleTag(a.getAttribute('data-tag'));
    });
    a.addEventListener('keydown', function (e) {
      if (e.key === ' ' || e.key === 'Spacebar') {
        e.preventDefault(); toggleTag(a.getAttribute('data-tag'));
      }
    });
  });
  root.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.entry__tag');
    if (!b) return;
    e.preventDefault();
    toggleTag(b.getAttribute('data-tag'));
    var top = document.querySelector('.toolbar');
    if (top && top.scrollIntoView) {
      try { top.scrollIntoView({ block: 'start', behavior: 'smooth' }); }
      catch (err) { top.scrollIntoView(); }
    }
  });
  window.addEventListener('popstate', function () { readURL(); apply(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
      e.preventDefault(); input.focus(); input.select();
    }
    if (e.key === 'Escape' && document.activeElement === input) {
      input.value = ''; active = []; apply(true);
    }
  });

  readURL();
  apply(false);
})();
"""

# --------------------------------------------------------------------------- #
#  Index                                                                      #
# --------------------------------------------------------------------------- #
def build_index(modules, tag_counts):
    by_month, by_day = {}, {}
    for m in modules:
        by_month.setdefault(m["date"][:7], []).append(m)
        by_day.setdefault(m["date"], []).append(m)

    # --- chronologie : mois du plus recent au plus ancien, separateur d'annee
    sections, seen_years = [], set()
    for ym in sorted(by_month, reverse=True):
        year = ym[:4]
        if year not in seen_years:
            seen_years.add(year)
            sections.append(f'<h2 class="year" data-year="{year}">{year}</h2>')
        mods = by_month[ym]
        cards = "".join(entry_card(m) for m in mods)
        sections.append(
            f'<section class="month" id="m-{ym}" data-month="{ym}" '
            f'aria-labelledby="h-{ym}">'
            f'<h3 class="month__head" id="h-{ym}">'
            f'<span class="month__name">{fr_month(ym)}</span>'
            f'<span class="month__count">{plural(len(mods), "module")}</span></h3>'
            f'{month_strip(ym, by_day)}'
            f'<div class="entries">{cards}</div></section>')
    timeline = "\n".join(sections) or "<p>Aucune entrée pour le moment.</p>"

    # --- navigation par mois
    nav = "".join(
        f'<a href="#m-{ym}" data-month="{ym}">'
        f'<b>{MOIS_COURT[int(ym[5:7]) - 1]}</b> {ym[2:4]}</a>'
        for ym in sorted(by_month, reverse=True))

    # --- nuage de tags, tries par frequence puis alphabetiquement
    ordered = sorted(tag_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    head = "".join(tag_chip(t, n) for t, n in ordered[:TAGS_VISIBLES])
    rest = ordered[TAGS_VISIBLES:]
    more = ""
    if rest:
        more = ('<details><summary>' + plural(len(rest), "autre mot-clé", "autres mots-clés")
                + '</summary><ul class="tags__list">'
                + "".join(tag_chip(t, n) for t, n in rest) + "</ul></details>")
    tags_block = (f'<section class="tags" aria-label="Mots-clés">'
                  f'<ul class="tags__list">{head}</ul>{more}</section>') if ordered else ""

    # --- index de recherche embarque : id -> {haystack replie, tags}
    data = {module_id(m): {
        "h": fold(" ".join([m["title"], " ".join(m["tags"]).replace("-", " "),
                            " ".join(m["tags"]), m["category_full"],
                            m["excerpt"], m["date"]])),
        "g": m["tags"],
    } for m in modules}

    n_days = len({m["date"] for m in modules})
    body = (
        '<main class="page">'
        '<h1>Droit Vivant</h1>'
        '<p class="lede">Veille quotidienne sur le droit qui se construit — numérique, '
        'libertés, IA, cybersécurité, jurisprudence française, européenne et CEDH. '
        'Chaque entrée : une infographie, un brief court et une source longue pour podcast.</p>'

        '<div class="toolbar">'
        '<form class="search" role="search" action="index.html" method="get">'
        '<span class="search__field">'
        '<input type="search" id="q" name="q" autocomplete="off" spellcheck="false" '
        'aria-label="Rechercher un module par mot-clé ou #tag" '
        'placeholder="Rechercher : rgpd, cjue, #donnees-personnelles…">'
        '<button type="button" class="search__clear" id="q-clear" hidden '
        'aria-label="Effacer la recherche">&times;</button>'
        '</span></form>'
        '<p class="search__opts">'
        '<label><input type="checkbox" id="ft"> Chercher dans le texte intégral</label>'
        '<span class="hint">· <code>#tag</code> filtre, le reste cherche dans '
        'titres, mots-clés et résumés · <code>/</code> pour cibler le champ</span>'
        '</p>'
        '<p class="hint" id="ft-note" hidden></p>'
        '<noscript><p class="nojs">La recherche et le filtrage par mots-clés nécessitent '
        'JavaScript. La chronologie complète reste consultable ci-dessous.</p></noscript>'
        '</div>'

        f'{tags_block}'
        f'<nav class="monthnav" aria-label="Aller à un mois">{nav}</nav>'

        '<div class="status">'
        f'<span class="status__n" id="count" aria-live="polite">'
        f'{plural(len(modules), "module")} sur {plural(n_days, "jour")}</span>'
        '<a class="status__reset" id="reset" href="index.html" hidden>Réinitialiser</a>'
        '</div>'
        '<p class="empty" id="empty" hidden>Aucun module ne correspond à '
        '<b id="empty-q"></b>.<br>Essayez un mot-clé plus court, retirez un '
        '<code>#tag</code>, ou activez la recherche dans le texte intégral.</p>'

        f'<div id="dv" class="timeline">{timeline}</div>'
        f'<footer>{plural(len(modules), "module")} sur {plural(n_days, "jour")} · '
        f'mise à jour {date.today().isoformat()} · {DISCLAIMER}</footer>'
        '</main>'
        '<script type="application/json" id="dv-data">'
        + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        + '</script>'
        f'<script>{SEARCH_JS}</script>')

    return ('<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<title>Droit Vivant — veille juridique</title>'
            '<meta name="description" content="Veille quotidienne sur le droit du numérique, '
            'les libertés, l\'IA et la cybersécurité : infographie, brief et source longue.">'
            '<link rel="stylesheet" href="assets/style.css"></head><body>'
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
    light, full, tag_counts = [], {}, {}
    for x in modules:
        if x["infographie"]:
            p = SITE / x["infographie"]
            p.write_text(reskin_infographie(read(p)), encoding="utf-8")
        if x["brief"]:
            p = SITE / x["brief"]
            (p.parent / (p.stem + ".html")).write_text(
                render_md_page(read(p), "Brief", "../../",
                               raw_md_name=p.name,
                               raw_label="Version .md brute"), encoding="utf-8")
        if x["source"]:
            p = SITE / x["source"]
            (p.parent / (p.stem + ".html")).write_text(
                render_md_page(read(p), "Source NotebookLM", "../../",
                               raw_md_name=p.name,
                               raw_label="Version .md brute (pour NotebookLM)"),
                encoding="utf-8")

        for t in x["tags"]:
            tag_counts[t] = tag_counts.get(t, 0) + 1

        mid = module_id(x)
        light.append({
            "id": mid,
            "date": x["date"],
            "slug": x["slug"],
            "title": x["title"],
            "url": module_url(x),
            "category": x["category"],
            "tags": x["tags"],
            "excerpt": x["excerpt"],
        })
        full[mid] = fold(md_plain(read(x["_brief_path"]) + "\n" + read(x["_source_path"])))

    (SITE / "search-index.json").write_text(
        json.dumps(light, ensure_ascii=False, indent=None, separators=(",", ":")),
        encoding="utf-8")
    (SITE / "search-fulltext.json").write_text(
        json.dumps(full, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    (SITE / "index.html").write_text(build_index(modules, tag_counts), encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    n_days = len({m["date"] for m in modules})
    print(f"{len(modules)} module(s) sur {n_days} jour(s) construits, "
          f"{len(tag_counts)} mot(s)-cle(s).")

if __name__ == "__main__":
    main()
