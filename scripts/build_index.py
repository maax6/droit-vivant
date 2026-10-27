#!/usr/bin/env python3
"""Construit le site statique Droit Vivant pour GitHub Pages.

Source unique de design : ce script.
- charte partagee clair/sombre auto -> site/assets/style.css
- brief.md / source.md rendus en pages HTML stylees (Markdown -> HTML, stdlib seule)
- les .md bruts restent disponibles (utile pour NotebookLM)
- les infographies sont "re-skinnees" au build (CSS inline retire, charte appliquee)
- une FICHE par module (fiches/<id>.html) : titre court, resume en 3 lignes,
  analyse complete repliable (le brief, inchange), sources
- index : fiches filtrables par theme, recherche client, chronologie mensuelle
- page « Comment c'est fait » (comment-cest-fait.html)
Aucune dependance externe (stdlib seule au build, aucun CDN cote client).

RESUMES
-------
Les resumes en 3 lignes vivent dans scripts/data/resumes.json (dans scripts/ pour
que la CI, qui ne surveille que archive/, scripts/ et .github/workflows/, se
declenche quand on les modifie). Cle = identifiant du module (AAAA-MM-JJ ou
AAAA-MM-JJ-slug) ; champs : titre_court, quoi, qui, change, theme. Tous
optionnels : un module sans resume s'affiche avec son titre d'origine et
l'analyse complete ouverte.

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
import html, json, re, shutil, sys, unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "archive"
SITE = ROOT / "site"
RESUMES = ROOT / "scripts" / "data" / "resumes.json"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

MOIS = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre")
MOIS_COURT = ("janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.",
              "août", "sept.", "oct.", "nov.", "déc.")
JOURS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")

# Themes des filtres de l'accueil : cle (slug) -> libelle affiche.
THEMES = {"ia": "IA", "cyber": "Cyber", "rgpd": "RGPD", "dsa": "DSA",
          "jurisprudence": "Jurisprudence", "autres": "Autres"}
THEME_DEFAUT = "autres"
# Les trois lignes de la fiche : (cle dans resumes.json, intitule affiche).
LIGNES = (("quoi", "Ce qui s’est passé"),
          ("qui", "Qui est concerné"),
          ("change", "Ce qui change"))
CHAMPS_RESUME = ("titre_court", "quoi", "qui", "change", "theme")
FICHES_DIR = "fiches"
ABOUT_PAGE = "comment-cest-fait.html"

TAGS_VISIBLES = 12      # taille du nuage avant repli dans <details>
TAGS_PAR_CARTE = 3
EXCERPT_MAX = 220
TAGS_MIN = 2            # occurrences minimales pour figurer dans le nuage

# Vocabulaire controle. Sans lui, la ligne « Theme » de chaque brief fabrique un
# tag neuf chaque jour : 141 tags pour 47 modules, dont 80 % employes une seule
# fois. Un tag utilise une fois n'est pas un filtre, c'est une etiquette.
TAG_ALIAS = {
    "cyber": "cybersecurite",
    "securite-informatique": "cybersecurite",
    "intelligence-artificielle": "ia",
    "droit-de-l-ia": "ia",
    "reglement-ia": "ai-act",
    "ue": "union-europeenne",
    "droit-de-l-union": "union-europeenne",
    "cour-de-justice": "cjue",
    "cour-de-justice-de-l-union-europeenne": "cjue",
    "videoprotection-algorithmique": "videosurveillance-algorithmique",
    "donnees-a-caractere-personnel": "donnees-personnelles",
    "protection-des-donnees": "donnees-personnelles",
    "regulation-des-plateformes": "dsa",
    "digital-services-act": "dsa",
    "digital-markets-act": "dma",
    "vie-privee-numerique": "vie-privee",
    "liberte-d-expression": "libertes",
}


def canon_tags(seq):
    """Replie les synonymes sur leur forme canonique, sans doublon."""
    out = []
    for t in seq:
        c = TAG_ALIAS.get(t, t)
        if c and c not in out:
            out.append(c)
    return out


def singles_label(singles):
    """Les tags a occurrence unique sont masques du nuage, pas de la recherche."""
    if not singles:
        return ""
    return (f" · {len(singles)} à occurrence unique, masqués mais"
            " toujours interrogeables au clavier")


def card_tags(x):
    """Sur la carte, on masque le tag qui ne fait que repeter la categorie."""
    cat = slugify(x.get("category", ""))
    out = [t for t in x["tags"] if t != cat]
    return (out or x["tags"])[:TAGS_PAR_CARTE]

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
.topbar nav{display:flex;gap:18px;flex-wrap:wrap}
.topbar nav a{font-size:14px;color:var(--muted);padding:4px 0;border-bottom:2px solid transparent}
.topbar nav a:hover{color:var(--accent);text-decoration:none}
.topbar nav a[aria-current=page]{color:var(--text);border-bottom-color:var(--accent)}
.skip{position:absolute;left:-9999px;top:0;background:var(--accent);color:#fff;
  padding:10px 16px;border-radius:0 0 8px 0;z-index:10;font-size:14px}
.skip:focus{left:0}
@media (prefers-color-scheme: dark){.skip{color:#0b1320}}
.sitefoot{margin:0;padding:0;border-top:1px solid var(--border);color:var(--muted);font-size:.85rem}
.sitefoot .inner{max-width:780px;margin:0 auto;padding:18px 22px 44px}
.sitefoot p{margin:0 0 .5em}

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

/* ---- index : filtres par theme ---- */
.themes{display:flex;flex-wrap:wrap;gap:6px;margin:14px 0 0}
.theme-btn{font:inherit;font-size:13.5px;line-height:1.2;padding:7px 13px;border-radius:999px;
  border:1px solid var(--border);background:var(--surface);color:var(--text);cursor:pointer;
  display:inline-flex;align-items:baseline;gap:7px}
.theme-btn:hover{border-color:var(--accent);color:var(--accent)}
.theme-btn .n{font-size:11.5px;color:var(--muted);font-variant-numeric:tabular-nums}
.theme-btn[aria-pressed=true]{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
.theme-btn[aria-pressed=true] .n{color:inherit;opacity:.9}
@media (prefers-color-scheme: dark){.theme-btn[aria-pressed=true]{color:#0b1320}}
.tagbox{margin:0 0 14px}
.tagbox>summary{font-size:13px;color:var(--muted);cursor:pointer;width:fit-content;padding:4px 0}
.tagbox>summary:hover{color:var(--accent)}
.tagbox .tags{margin:8px 0 0}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}

/* ---- index : chronologie ---- */
.section-title{font-family:var(--serif);font-size:1.3rem;margin:28px 0 2px}
.month{margin:0 0 10px;scroll-margin-top:8px}
.month__head{position:sticky;top:0;z-index:3;background:var(--bg);margin:0;
  padding:12px 0 8px;display:flex;align-items:baseline;justify-content:space-between;gap:10px;
  font-family:var(--sans);font-size:.95rem;font-weight:700;letter-spacing:0}
.month__name{text-transform:capitalize}
.month__count{font-size:12px;font-weight:400;color:var(--muted);font-variant-numeric:tabular-nums}
.entries{display:flex;flex-direction:column;gap:14px;margin:0 0 26px}

/* ---- fiche (carte d'accueil et page) ---- */
.entry{position:relative;background:var(--surface);border:1px solid var(--border);
  border-radius:8px;padding:18px 22px 16px;scroll-margin-top:74px}
.entry:hover{border-color:var(--muted)}
@supports selector(:has(*)){
  .entry:has(.entry__open:focus-visible){outline:2px solid var(--accent);outline-offset:2px}
  .entry .entry__open:focus-visible{outline:none}
}
.entry__meta,.fiche__meta{display:flex;align-items:center;flex-wrap:wrap;gap:8px;
  font-size:12.5px;color:var(--muted);margin:0 0 8px}
.entry__meta time,.fiche__meta time{font-variant-numeric:tabular-nums;font-weight:600;color:var(--text)}
.entry__slug{text-transform:uppercase;letter-spacing:.06em;font-size:10.5px;font-weight:700;
  color:var(--accent-ink);background:var(--surface-2);border:1px solid var(--border);
  border-radius:999px;padding:2px 8px}
.badge{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-weight:700;
  letter-spacing:.05em;text-transform:uppercase;color:var(--accent-ink);background:var(--surface-2);
  border:1px solid var(--border);border-radius:999px;padding:2px 10px}
.badge::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--dot,var(--muted))}
.badge--ia{--dot:#8e5bd1}.badge--cyber{--dot:#d1603d}.badge--rgpd{--dot:#2b8a6e}
.badge--dsa{--dot:#c28a00}.badge--jurisprudence{--dot:#3b7be0}.badge--autres{--dot:#7a8494}
.entry__title{font-family:var(--serif);font-size:1.2rem;font-weight:700;line-height:1.32;
  letter-spacing:-.01em;margin:0;color:var(--text);text-wrap:balance;
  display:-webkit-box;-webkit-line-clamp:5;-webkit-box-orient:vertical;overflow:hidden}
.trois{margin:12px 0 0;display:grid;gap:10px}
.trois>div{display:grid;grid-template-columns:9.5em 1fr;gap:3px 14px;align-items:baseline}
.trois dt{font-size:.72rem;text-transform:uppercase;letter-spacing:.07em;font-weight:700;color:var(--muted)}
.trois dd{margin:0;font-size:.98rem;line-height:1.55}
@media (max-width:560px){.trois>div{grid-template-columns:1fr;gap:1px}}
.entry__actions{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:14px 0 0}
.btn{font-size:13px;padding:7px 14px;border-radius:6px;text-decoration:none;
  background:var(--bg);color:var(--text);border:1px solid var(--border);transition:border-color .15s}
.btn:hover{border-color:var(--accent);text-decoration:none}
.btn.primary{background:var(--accent);color:#fff;border-color:var(--accent);font-weight:600}
@media (prefers-color-scheme: dark){.btn.primary{color:#0b1320}}
.entry__open::after{content:"";position:absolute;inset:0;border-radius:8px}
.entry__actions > :not(.entry__open){position:relative;z-index:1}
.res{margin-left:auto;font-size:12.5px}
.res>summary{list-style:none;cursor:pointer;color:var(--muted);padding:7px 2px;
  display:inline-flex;align-items:center;gap:5px}
.res>summary::-webkit-details-marker{display:none}
.res>summary::after{content:"›";display:inline-block;transition:transform .15s;font-size:14px}
.res[open]>summary::after{transform:rotate(90deg)}
.res>summary:hover{color:var(--accent)}
.res__body{display:flex;flex-direction:column;align-items:flex-start;gap:2px;padding:8px 0 2px}
.res__body a{color:var(--muted);font-size:12.5px}
.res__body a:hover{color:var(--accent)}
@media (max-width:520px){
  .res{margin-left:0}
  .entry__actions{gap:6px}
  .btn{padding:7px 12px}
}

/* ---- page fiche ---- */
.backlink{font-size:.88rem;margin:0 0 18px}
.fiche__meta{font-size:13px;gap:10px;margin:0 0 12px}
.fiche__full{color:var(--muted);font-size:.98rem;margin:0 0 4px}
.resume{background:var(--surface);border:1px solid var(--border);border-radius:8px;
  padding:20px 24px;margin:22px 0}
.resume .trois{margin:0;gap:14px}
.resume .trois dd{font-size:1.04rem}
.analyse{margin:26px 0;border:1px solid var(--border);border-radius:8px}
.analyse>summary{cursor:pointer;padding:14px 20px;font-weight:600;list-style:none;
  display:flex;justify-content:space-between;align-items:center;gap:12px}
.analyse>summary::-webkit-details-marker{display:none}
.analyse>summary::after{content:"+";font-size:1.4rem;line-height:1;color:var(--muted)}
.analyse[open]>summary::after{content:"\\2212"}
.analyse>summary:hover{color:var(--accent)}
.analyse[open]>summary{border-bottom:1px solid var(--border)}
.analyse__body{padding:16px 20px 4px}
.fiche h2{font-size:1.15rem;margin:1.6em 0 .5em}
.linkrow{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 1.2em}
.pager{display:flex;justify-content:space-between;gap:16px;margin:36px 0 0;
  padding-top:16px;border-top:1px solid var(--border);font-size:.92rem}
.pager a{display:block;max-width:48%}
.pager small{display:block;color:var(--muted);font-size:.75rem;text-transform:uppercase;letter-spacing:.07em}
.pager__next{margin-left:auto;text-align:right}
.fiche-tags{display:flex;flex-wrap:wrap;gap:6px;list-style:none;margin:0 0 1.4em;padding:0}
.fiche-tags a{display:inline-block;font-size:12.5px;color:var(--muted);border:1px solid var(--border);
  border-radius:999px;padding:3px 10px;background:var(--surface)}
.fiche-tags a:hover{color:var(--accent);border-color:var(--accent);text-decoration:none}

/* ---- pages MD rendues et page « Comment c'est fait » ---- */
.doc .meta{color:var(--muted);font-size:.9rem;margin:-2px 0 1.8em}
.doc ul,.doc ol{padding-left:22px;margin:0 0 1.05em}
.doc li{margin-bottom:.4em}
.doc h2{font-size:1.22rem}
.doc a{word-break:break-word}
.about .lede{max-width:none}
.about ol.steps{list-style:none;counter-reset:s;padding:0;margin:0 0 1.4em}
.about ol.steps li{counter-increment:s;position:relative;padding:12px 16px 12px 52px;margin:0 0 8px;
  background:var(--surface);border:1px solid var(--border);border-radius:8px}
.about ol.steps li::before{content:counter(s);position:absolute;left:16px;top:12px;width:24px;
  height:24px;border-radius:50%;background:var(--surface-2);border:1px solid var(--border);
  color:var(--accent-ink);font-weight:700;font-size:.85rem;display:flex;align-items:center;
  justify-content:center}
.about ol.steps strong{display:block}
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
NAV = (("index", "index.html", "Fiches"),
       ("about", ABOUT_PAGE, "Comment c’est fait"))

def topbar(prefix, current=None):
    links = "".join(
        f'<a href="{prefix}{href}"' + (' aria-current="page"' if key == current else "")
        + f'>{html.escape(label)}</a>'
        for key, href, label in NAV)
    return (f'<a class="skip" href="#main">Aller au contenu</a>'
            f'<header class="topbar"><div class="inner">'
            f'<a class="brand" href="{prefix}index.html">Droit <span>Vivant</span></a>'
            f'<nav aria-label="Navigation principale">{links}</nav>'
            f'</div></header>')

DISCLAIMER = ("Contenu pédagogique ; ne constitue pas un conseil juridique personnalisé. "
              "Droit Vivant — veille sur le droit qui se construit.")

def site_footer(prefix, feed=False):
    links = [f'<a href="{prefix}{ABOUT_PAGE}">Comment c’est fait</a>']
    if feed:
        links.append(f'<a href="{prefix}feed.xml">Flux Atom</a>')
    return (f'<footer class="sitefoot"><div class="inner">'
            f'<p>{DISCLAIMER}</p><p>{" · ".join(links)}</p></div></footer>')

def shell(title, body, prefix, current=None, desc="", footer=True, feed=False):
    meta = (f'<meta name="description" content="{html.escape(desc, quote=True)}">'
            if desc else "")
    return (f'<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f'<title>{html.escape(title)}</title>{meta}'
            f'<link rel="stylesheet" href="{prefix}assets/style.css"></head><body>'
            f'{topbar(prefix, current)}{body}'
            f'{site_footer(prefix, feed) if footer else ""}</body></html>')

def render_md_page(md_text, kicker, prefix, raw_md_name=None, raw_label=None):
    title = md_title(md_text) or kicker
    meta = ""
    if raw_md_name:
        meta = (f'<p class="meta"><a href="{raw_md_name}">&#8595; '
                f'{html.escape(raw_label or "Version .md brute")}</a></p>')
    body = (f'<main class="page" id="main"><span class="kicker">{html.escape(kicker)}</span>'
            f'<article class="doc">{meta}{md_to_html(md_text)}</article></main>')
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
    return promote_main(ensure_wrap(t))

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

def promote_main(t):
    """Le conteneur .wrap devient le repere <main> (cible du lien d'evitement).
    Sans effet si la structure n'est pas celle attendue (.wrap ferme juste
    avant </body>)."""
    m = re.search(r'<div class="wrap"', t)
    end = re.search(r"</div>(\s*)</body>", t, re.I)
    if not m or not end or end.start() < m.start():
        return t
    t = t[:end.start()] + "</main>" + t[end.start() + len("</div>"):]
    return (t[:m.start()] + '<main class="wrap" id="main"'
            + t[m.start() + len('<div class="wrap"'):])

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
                "tags": canon_tags(tags),
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
#  Resumes : scripts/data/resumes.json                                         #
# --------------------------------------------------------------------------- #
def load_resumes(path=RESUMES):
    """id de module -> {titre_court, quoi, qui, change, theme}.

    Tolerant : fichier absent, JSON invalide, entree ou champ mal forme -> on
    avertit (stderr) et on continue, la fiche s'affiche alors sans resume."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as e:
        print(f"AVERTISSEMENT : {path.name} illisible ({e}) ; aucune fiche resumee.",
              file=sys.stderr)
        return {}
    if not isinstance(raw, dict):
        print(f"AVERTISSEMENT : {path.name} doit etre un objet JSON ; ignore.",
              file=sys.stderr)
        return {}
    out = {}
    for key, val in raw.items():
        if isinstance(val, dict):
            out[str(key)] = {f: squash(val[f]) for f in CHAMPS_RESUME
                             if isinstance(val.get(f), str) and squash(val[f])}
    return out

def attach_resumes(modules, resumes):
    """Ajoute a chaque module : short (titre court), theme (cle de THEMES),
    lines (dict des lignes presentes). Rend la liste des modules sans les 3 lignes."""
    sans = []
    for x in modules:
        r = resumes.get(module_id(x), {})
        theme = slugify(r.get("theme", ""))
        x["short"] = r.get("titre_court") or x["title"]
        x["theme"] = theme if theme in THEMES else THEME_DEFAUT
        x["lines"] = {k: r[k] for k, _ in LIGNES if r.get(k)}
        if len(x["lines"]) < len(LIGNES):
            sans.append(module_id(x))
    return sans

# --------------------------------------------------------------------------- #
#  Helpers de presentation                                                     #
# --------------------------------------------------------------------------- #
def module_id(x):
    return x["date"] + ("-" + x["slug"] if x["slug"] else "")

def module_url(x):
    """Cible historique (flux Atom, index de recherche) : l'infographie, a defaut
    le brief, a defaut la source."""
    if x["infographie"]:
        return x["infographie"]
    for k in ("brief", "source"):
        if x[k]:
            return x[k][:-3] + ".html"
    return ""

def fiche_href(x, prefix=""):
    return f"{prefix}{FICHES_DIR}/{module_id(x)}.html"

def fr_day(iso):
    y, m, d = (int(v) for v in iso.split("-"))
    return ("1er" if d == 1 else str(d)) + " " + MOIS[m - 1]

def fr_long(iso):
    y, m, d = (int(v) for v in iso.split("-"))
    return f"{JOURS[date(y, m, d).weekday()]} {fr_day(iso)} {y}"

def fr_month(ym):
    y, m = (int(v) for v in ym.split("-"))
    return f"{MOIS[m - 1]} {y}"

def plural(n, one, many=None):
    return f"{n} {one if n <= 1 else (many or one + 's')}"

def theme_badge(key):
    return f'<span class="badge badge--{key}">{html.escape(THEMES[key])}</span>'

def slug_label(x):
    return x["slug"].replace("-", " ") if x["slug"] else "module principal"

def lines_html(x, cls="trois"):
    rows = "".join(f'<div><dt>{lab}</dt><dd>{html.escape(x["lines"][k])}</dd></div>'
                   for k, lab in LIGNES if k in x["lines"])
    return f'<dl class="{cls}">{rows}</dl>' if rows else ""

def split_brief(md):
    """Brief -> (corps sans titre ni sources, section Sources). Le contenu du
    corps n'est pas modifie : le H1 est repris en titre de page, la liste des
    sources est affichee a part en bas de fiche."""
    text = (md or "").replace("\r\n", "\n")
    m = re.search(r"^##\s+Sources?\b.*$", text, re.M | re.I)
    body, sources = (text[:m.start()], text[m.end():]) if m else (text, "")
    body = re.sub(r"^#\s+.*\n?", "", body, count=1, flags=re.M)
    return body.strip(), sources.strip()

# --------------------------------------------------------------------------- #
#  Accueil : une fiche par module                                              #
# --------------------------------------------------------------------------- #
def entry_card(x):
    mid = module_id(x)
    label = html.escape(x["short"], quote=True)
    meta = [f'<time datetime="{x["date"]}">{fr_day(x["date"])}</time>',
            theme_badge(x["theme"])]
    if x["multi"]:
        meta.append(f'<span class="entry__slug">{html.escape(slug_label(x))}</span>')

    actions = [f'<a class="btn primary entry__open" href="{fiche_href(x)}" '
               f'aria-label="Lire la fiche — {label}">Lire la fiche</a>']
    if x["infographie"]:
        actions.append(f'<a class="btn" href="{x["infographie"]}" '
                       f'aria-label="Infographie — {label}">Infographie</a>')
    res = []
    if x["brief"]:
        res.append(f'<a href="{x["brief"][:-3]}.html">Brief (page)</a>')
    if x["source"]:
        res.append(f'<a href="{x["source"][:-3]}.html">Source NotebookLM (page)</a>')
        res.append(f'<a href="{x["source"]}" download>Fichier source pour NotebookLM (.md)</a>')
    if x["brief"]:
        res.append(f'<a href="{x["brief"]}" download>Texte du brief (.md)</a>')
    if res:
        actions.append('<details class="res"><summary>Ressources</summary>'
                       f'<div class="res__body">{"".join(res)}</div></details>')

    return (f'<article class="entry" id="e-{mid}" data-id="{mid}" data-day="{x["date"]}" '
            f'data-theme="{x["theme"]}">'
            f'<div class="entry__meta">{"".join(meta)}</div>'
            f'<h4 class="entry__title">{html.escape(x["short"])}</h4>'
            f'{lines_html(x)}'
            f'<div class="entry__actions">{"".join(actions)}</div>'
            f'</article>')

def tag_chip(tag, n, extra=""):
    return (f'<li><a class="tag{extra}" href="?tag={tag}" data-tag="{tag}">'
            f'#{html.escape(tag)}<span class="tag__n">{n}</span></a></li>')

# --------------------------------------------------------------------------- #
#  Page fiche                                                                  #
# --------------------------------------------------------------------------- #
def render_fiche(x, i, modules):
    prefix = "../"
    body_md, src_md = split_brief(read(x["_brief_path"]))
    meta = [f'<time datetime="{x["date"]}">{fr_long(x["date"])}</time>',
            theme_badge(x["theme"])]
    if x["multi"]:
        meta.append(f'<span class="entry__slug">{html.escape(slug_label(x))}</span>')

    parts = [f'<p class="backlink"><a href="{prefix}index.html">&larr; Toutes les fiches</a></p>',
             f'<div class="fiche__meta">{"".join(meta)}</div>',
             f'<h1>{html.escape(x["short"])}</h1>']
    if x["short"] != x["title"]:
        parts.append(f'<p class="fiche__full"><span class="sr-only">Titre complet : </span>'
                     f'{html.escape(x["title"])}</p>')
    if x["lines"]:
        parts.append('<section class="resume" aria-label="En trois lignes">'
                     f'{lines_html(x)}</section>')

    if body_md:
        # sans resume, l'analyse est la seule matiere de la page : on la deplie
        opened = "" if x["lines"] else " open"
        parts.append(f'<details class="analyse"{opened}><summary>Lire l’analyse complète</summary>'
                     f'<div class="analyse__body doc">{md_to_html(body_md)}</div></details>')
    else:
        parts.append('<p>Ce module ne comporte pas de brief écrit.'
                     + (' L’infographie en donne la synthèse.' if x["infographie"] else "")
                     + '</p>')

    if src_md:
        parts.append('<section aria-labelledby="sources"><h2 id="sources">Sources</h2>'
                     f'<div class="doc">{md_to_html(src_md)}</div></section>')

    links = []
    if x["infographie"]:
        links.append(f'<a class="btn" href="{prefix}{x["infographie"]}">Infographie</a>')
    if x["source"]:
        links.append(f'<a class="btn" href="{prefix}{x["source"][:-3]}.html">Source NotebookLM</a>')
    if x["brief"]:
        links.append(f'<a class="btn" href="{prefix}{x["brief"]}" download>Brief (.md)</a>')
    if links:
        parts.append(f'<section aria-labelledby="plus"><h2 id="plus">Aller plus loin</h2>'
                     f'<div class="linkrow">{"".join(links)}</div></section>')

    if x["tags"]:
        chips = "".join(f'<li><a href="{prefix}index.html?tag={t}">#{html.escape(t)}</a></li>'
                        for t in x["tags"])
        parts.append(f'<nav aria-label="Mots-clés"><ul class="fiche-tags">{chips}</ul></nav>')

    newer = modules[i - 1] if i > 0 else None
    older = modules[i + 1] if i + 1 < len(modules) else None
    pager = ""
    if older:
        pager += (f'<a href="{sibling_href(older)}"><small>&larr; Fiche précédente</small>'
                  f'{html.escape(older["short"])}</a>')
    if newer:
        pager += (f'<a class="pager__next" href="{sibling_href(newer)}"><small>Fiche suivante &rarr;</small>'
                  f'{html.escape(newer["short"])}</a>')
    if pager:
        parts.append(f'<nav class="pager" aria-label="Autres fiches">{pager}</nav>')

    desc = x["lines"].get("quoi") or x["title"]
    body = f'<main class="page fiche" id="main"><article>{"".join(parts)}</article></main>'
    return shell(f'{x["short"]} — Droit Vivant', body, prefix, desc=desc)

def sibling_href(x):
    """Lien vers une autre fiche depuis une fiche (meme dossier)."""
    return f"{module_id(x)}.html"

# --------------------------------------------------------------------------- #
#  Index : script de recherche et de filtrage (inline, aucune dependance)      #
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
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.monthnav a'));
  var tagLinks = Array.prototype.slice.call(document.querySelectorAll('.tag[data-tag]'));
  var themeBtns = Array.prototype.slice.call(document.querySelectorAll('.theme-btn'));

  var fullText = null;      // chargé paresseusement
  var ftState  = 'idle';    // idle | loading | ready | error
  var active   = [];        // tags actifs
  var theme    = '';        // thème actif ('' = tous)
  var query    = '';        // texte libre (déjà replié)

  function fold(s) {
    return (s || '').normalize('NFD').replace(/\p{Mn}/gu, '').toLowerCase();
  }
  function themeLabel(key) {
    for (var i = 0; i < themeBtns.length; i++) {
      if (themeBtns[i].getAttribute('data-theme') === key) {
        return themeBtns[i].getAttribute('data-label') || key;
      }
    }
    return key;
  }

  /* ---- lecture / écriture de l'état dans l'URL ---- */
  function readURL() {
    var p = new URLSearchParams(location.search);
    var t = (p.get('tag') || '').split(',').map(function (s) { return s.trim(); })
              .filter(Boolean);
    active = t;
    theme = p.get('theme') || '';
    if (theme && !themeBtns.some(function (b) { return b.getAttribute('data-theme') === theme; })) {
      theme = '';
    }
    input.value = p.get('q') || '';
    if (p.get('ft') === '1' && ftBox) { ftBox.checked = true; loadFullText(); }
  }
  function writeURL(push) {
    var p = new URLSearchParams();
    var q = input.value.trim();
    if (q) p.set('q', q);
    if (theme) p.set('theme', theme);
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
    if (theme && rec.t !== theme) return false;
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

    var filtering = !!(query || theme || active.length || typed.length);
    var n = 0, perMonth = {};
    cards.forEach(function (card) {
      var ok = matches(card.getAttribute('data-id'), all);
      card.hidden = !ok;
      if (ok) {
        n++;
        var ym = card.getAttribute('data-day').slice(0, 7);
        perMonth[ym] = (perMonth[ym] || 0) + 1;
      }
    });

    months.forEach(function (sec) {
      var c = perMonth[sec.getAttribute('data-month')] || 0;
      sec.hidden = c === 0;
      var badge = sec.querySelector('.month__count');
      if (badge) { badge.textContent = c + (c > 1 ? ' fiches' : ' fiche'); }
    });
    navLinks.forEach(function (a) {
      a.classList.toggle('is-empty', !perMonth[a.getAttribute('data-month')]);
    });
    tagLinks.forEach(function (a) {
      var on = active.indexOf(a.getAttribute('data-tag')) !== -1;
      a.classList.toggle('is-active', on);
      a.setAttribute('aria-pressed', on);
    });
    themeBtns.forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-theme') === theme);
    });

    count.textContent = n + (n > 1 ? ' fiches' : ' fiche')
      + (filtering ? ' sur ' + cards.length : '');
    reset.hidden = !filtering;
    empty.hidden = n !== 0;
    if (n === 0) {
      emptyQ.textContent = [raw.trim(), theme ? themeLabel(theme) : '',
        active.map(function (t) { return '#' + t; }).join(' ')]
        .filter(Boolean).join(' ');
    }
    clearBtn.hidden = !raw;
    writeURL(!!push);
  }

  function clearAll() { input.value = ''; active = []; theme = ''; }

  /* ---- interactions ---- */
  input.addEventListener('input', function () { apply(false); });
  input.form.addEventListener('submit', function (e) { e.preventDefault(); apply(true); });
  clearBtn.addEventListener('click', function () { clearAll(); apply(true); input.focus(); });
  reset.addEventListener('click', function (e) { e.preventDefault(); clearAll(); apply(true); });
  if (ftBox) {
    ftBox.addEventListener('change', function () {
      if (ftBox.checked) { loadFullText(); } else { note(''); }
      apply(true);
    });
  }
  themeBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var t = b.getAttribute('data-theme');
      theme = (t && t === theme) ? '' : t;
      apply(true);
    });
  });
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

  window.addEventListener('popstate', function () { readURL(); apply(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
      e.preventDefault(); input.focus(); input.select();
    }
    if (e.key === 'Escape' && document.activeElement === input) {
      clearAll(); apply(true);
    }
  });

  readURL();
  apply(false);
})();
"""

# --------------------------------------------------------------------------- #
#  Flux Atom : une veille se lit dans un agregateur                            #
# --------------------------------------------------------------------------- #
SITE_URL = "https://droit-vivant.maxzer.fr/"
CUSTOM_DOMAIN = "droit-vivant.maxzer.fr"
FEED_MAX = 40


def build_feed(modules):
    """Flux Atom des derniers modules. Aucune dependance : chaines et html.escape.
    Les liens restent ceux des infographies : changer l'identifiant d'une entree
    la republierait aupres de tous les abonnes."""
    latest = modules[:FEED_MAX]
    stamp = (latest[0]["date"] if latest else date.today().isoformat()) + "T12:00:00Z"

    def esc(v):
        return html.escape(v or "", quote=True)

    out = ['<?xml version="1.0" encoding="utf-8"?>',
           '<feed xmlns="http://www.w3.org/2005/Atom">',
           "<title>Droit Vivant</title>",
           "<subtitle>Veille sur le droit du numérique, les libertés,"
           " l'IA et la cybersécurité.</subtitle>",
           f'<link rel="alternate" type="text/html" href="{SITE_URL}"/>',
           f'<link rel="self" type="application/atom+xml" href="{SITE_URL}feed.xml"/>',
           f"<id>{SITE_URL}</id>",
           f"<updated>{stamp}</updated>",
           "<author><name>Droit Vivant</name></author>"]
    for x in latest:
        url = SITE_URL + module_url(x)
        out.append("<entry>")
        out.append("<title>" + esc(x["title"]) + "</title>")
        out.append(f'<link rel="alternate" type="text/html" href="{esc(url)}"/>')
        out.append("<id>" + esc(url) + "</id>")
        out.append("<updated>" + x["date"] + "T12:00:00Z</updated>")
        for t in x["tags"]:
            out.append(f'<category term="{esc(t)}"/>')
        if x["excerpt"]:
            out.append("<summary>" + esc(x["excerpt"]) + "</summary>")
        out.append("</entry>")
    out.append("</feed>")
    return "\n".join(out)


# --------------------------------------------------------------------------- #
#  Page « Comment c'est fait »                                                 #
# --------------------------------------------------------------------------- #
def build_about():
    steps = (
        ("Collecte",
         "Des tâches récurrentes, exécutées avec un LLM (grand modèle de langage) dans "
         "Claude Cowork, rassemblent les sources d’un sujet : textes officiels, décisions "
         "de justice, communiqués d’autorités, presse spécialisée."),
        ("Rédaction",
         "Pour chaque sujet, la tâche produit trois documents : un brief (texte court, "
         "sources à l’appui), une infographie HTML et un texte source plus long, destiné à "
         "NotebookLM pour la production d’un podcast."),
        ("Archivage",
         "Les trois fichiers sont déposés dans le dépôt Git du projet, dans un dossier par "
         "date (<code>archive/AAAA-MM-JJ/</code>)."),
        ("Génération",
         "Un script Python, qui n’utilise que la bibliothèque standard, lit l’archive et "
         "produit le site statique : fiches, pages de brief, index de recherche, flux Atom."),
        ("Publication",
         "À chaque mise à jour de l’archive ou du script sur la branche principale, "
         "GitHub Actions relance le script et publie le résultat sur GitHub Pages."),
    )
    lis = "".join(f"<li><strong>{t}</strong>{d}</li>" for t, d in steps)
    body = (
        '<main class="page about" id="main"><article class="doc">'
        '<h1>Comment c’est fait</h1>'
        '<p class="lede">Droit Vivant est une veille sur le droit du numérique, produite avec '
        'l’aide d’un LLM et publiée sous forme de site statique. Cette page décrit la chaîne '
        'de production et ses limites.</p>'
        '<h2>La chaîne de production</h2>'
        f'<ol class="steps">{lis}</ol>'
        '<h2>Les fiches</h2>'
        '<p>Chaque fiche affiche un titre court et un résumé en trois lignes (ce qui s’est '
        'passé, qui est concerné, ce qui change). Ces éléments sont rédigés à partir du brief '
        'du module, avec l’aide d’un LLM. L’analyse complète, repliée par défaut, reprend le '
        'brief tel qu’il a été publié. Les sources sont listées en bas de page. Le thème '
        '(IA, cyber, RGPD, DSA, jurisprudence, autres) sert de filtre sur la page d’accueil.</p>'
        '<h2>Limites</h2>'
        '<ul>'
        '<li>Un LLM peut se tromper sur une date, un montant ou une interprétation. Les liens '
        'de sources permettent de vérifier chaque point.</li>'
        '<li>Une fiche reflète l’état des sources à sa date de publication. Une décision peut '
        'ensuite être réformée, un texte modifié, un calendrier décalé.</li>'
        '<li>Le résumé en trois lignes condense l’analyse et en omet les nuances. L’analyse '
        'complète et les sources font foi.</li>'
        '</ul>'
        '<h2>Avertissement</h2>'
        '<p>Droit Vivant est un contenu pédagogique. Il ne constitue pas un conseil juridique '
        'et ne remplace pas l’avis d’un avocat ou d’un juriste pour une situation particulière.</p>'
        '<h2>Code et archive</h2>'
        '<p>Le script de génération, l’archive et les résumés sont versionnés dans un dépôt '
        'Git. Les nouveautés sont aussi disponibles par <a href="feed.xml">flux Atom</a>.</p>'
        '</article></main>')
    return shell("Comment c’est fait — Droit Vivant", body, "", current="about",
                 desc="Comment Droit Vivant est produit : tâches récurrentes avec LLM, "
                      "génération statique, publication sur GitHub Pages.", feed=True)

# --------------------------------------------------------------------------- #
#  Index                                                                      #
# --------------------------------------------------------------------------- #
def build_index(modules, tag_counts):
    by_month = {}
    for m in modules:
        by_month.setdefault(m["date"][:7], []).append(m)

    # --- chronologie : mois du plus recent au plus ancien
    sections = []
    for ym in sorted(by_month, reverse=True):
        mods = by_month[ym]
        cards = "".join(entry_card(m) for m in mods)
        sections.append(
            f'<section class="month" id="m-{ym}" data-month="{ym}" '
            f'aria-labelledby="h-{ym}">'
            f'<h3 class="month__head" id="h-{ym}">'
            f'<span class="month__name">{fr_month(ym)}</span>'
            f'<span class="month__count">{plural(len(mods), "fiche")}</span>'
            f'</h3>'
            f'<div class="entries">{cards}</div></section>')
    timeline = "\n".join(sections) or "<p>Aucune entrée pour le moment.</p>"

    # --- navigation par mois
    nav = "".join(
        f'<a href="#m-{ym}" data-month="{ym}">'
        f'<b>{MOIS_COURT[int(ym[5:7]) - 1]}</b> {ym[2:4]}</a>'
        for ym in sorted(by_month, reverse=True))

    # --- filtres par theme
    per_theme = {k: 0 for k in THEMES}
    for m in modules:
        per_theme[m["theme"]] += 1
    theme_btns = [f'<button type="button" class="theme-btn" data-theme="" data-label="Tous" '
                  f'aria-pressed="true">Tous <span class="n">{len(modules)}</span></button>']
    for k, lab in THEMES.items():
        if per_theme[k]:
            theme_btns.append(
                f'<button type="button" class="theme-btn" data-theme="{k}" '
                f'data-label="{html.escape(lab, quote=True)}" aria-pressed="false">'
                f'{html.escape(lab)} <span class="n">{per_theme[k]}</span></button>')
    themes_block = ('<div class="themes" role="group" aria-label="Filtrer par thème">'
                    + "".join(theme_btns) + '</div>')

    # --- nuage de tags (replie), tries par frequence puis alphabetiquement
    _all = sorted(tag_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    _singles = [kv for kv in _all if kv[1] < TAGS_MIN]
    ordered = [kv for kv in _all if kv[1] >= TAGS_MIN]
    head = "".join(tag_chip(t, n) for t, n in ordered[:TAGS_VISIBLES])
    rest = ordered[TAGS_VISIBLES:]
    more = ""
    if rest or _singles:
        more = ('<details><summary>' + plural(len(rest), "autre mot-clé", "autres mots-clés")
                + singles_label(_singles)
                + '</summary><ul class="tags__list">'
                + "".join(tag_chip(t, n) for t, n in rest) + "</ul></details>")
    tags_block = (f'<details class="tagbox"><summary>Filtrer par mot-clé</summary>'
                  f'<section class="tags" aria-label="Mots-clés">'
                  f'<ul class="tags__list">{head}</ul>{more}</section></details>'
                  ) if ordered else ""

    # --- index de recherche embarque : id -> {haystack replie, tags, theme}
    data = {module_id(m): {
        "h": fold(" ".join([m["short"], m["title"], " ".join(m["lines"].values()),
                            " ".join(m["tags"]).replace("-", " "),
                            " ".join(m["tags"]), m["category_full"],
                            THEMES[m["theme"]], m["excerpt"], m["date"]])),
        "g": m["tags"],
        "t": m["theme"],
    } for m in modules}

    n_days = len({m["date"] for m in modules})
    body = (
        '<main class="page" id="main">'
        '<h1>Droit Vivant</h1>'
        '<p class="lede">Veille sur le droit qui se construit : IA, cybersécurité, données '
        'personnelles, plateformes, jurisprudence. Chaque module tient dans une fiche : '
        'trois lignes pour comprendre ce qui change, l’analyse complète à déplier, les '
        f'sources en fin de page. <a href="{ABOUT_PAGE}">Comment c’est fait</a>.</p>'

        '<div class="toolbar">'
        '<form class="search" role="search" action="index.html" method="get">'
        '<span class="search__field">'
        '<input type="search" id="q" name="q" autocomplete="off" spellcheck="false" '
        'aria-label="Rechercher une fiche par mot-clé ou #tag" '
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
        f'{themes_block}'
        '<noscript><p class="nojs">La recherche et les filtres nécessitent '
        'JavaScript. La chronologie complète reste consultable ci-dessous.</p></noscript>'
        '</div>'

        f'{tags_block}'
        f'<nav class="monthnav" aria-label="Aller à un mois">{nav}</nav>'

        '<div class="status">'
        f'<span class="status__n" id="count" aria-live="polite">'
        f'{plural(len(modules), "fiche")} sur {plural(n_days, "jour")}</span>'
        '<a class="status__reset" id="reset" href="index.html" hidden>Réinitialiser</a>'
        '</div>'
        '<p class="empty" id="empty" hidden>Aucune fiche ne correspond à '
        '<b id="empty-q"></b>.<br>Essayez un mot-clé plus court, changez de thème, '
        'retirez un <code>#tag</code>, ou activez la recherche dans le texte intégral.</p>'

        '<h2 class="section-title">Derniers modules</h2>'
        f'<div id="dv" class="timeline">{timeline}</div>'
        '</main>'
        f'{site_footer("", feed=True)}'
        '<script type="application/json" id="dv-data">'
        + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        + '</script>'
        f'<script>{SEARCH_JS}</script>')

    return ('<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<title>Droit Vivant — veille juridique</title>'
            '<meta name="description" content="Veille sur le droit du numérique, '
            'les libertés, l\'IA et la cybersécurité : une fiche par sujet, avec résumé '
            'en trois lignes, analyse complète et sources.">'
            '<link rel="alternate" type="application/atom+xml" '
            'title="Droit Vivant — flux Atom" href="feed.xml">'
            '<link rel="stylesheet" href="assets/style.css"></head><body>'
            + topbar("", current="index") + body + "</body></html>")

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
    (SITE / FICHES_DIR).mkdir(parents=True, exist_ok=True)

    modules = collect()
    resumes = load_resumes()
    sans_resume = attach_resumes(modules, resumes)
    inconnus = sorted(set(resumes) - {module_id(x) for x in modules})
    if sans_resume:
        print(f"Sans resume complet ({len(sans_resume)}) : {', '.join(sans_resume)}")
    if inconnus:
        print(f"AVERTISSEMENT : resumes sans module correspondant : {', '.join(inconnus)}",
              file=sys.stderr)

    light, full, tag_counts = [], {}, {}
    for i, x in enumerate(modules):
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
        (SITE / fiche_href(x)).write_text(render_fiche(x, i, modules), encoding="utf-8")

        for t in x["tags"]:
            tag_counts[t] = tag_counts.get(t, 0) + 1

        mid = module_id(x)
        light.append({
            "id": mid,
            "date": x["date"],
            "slug": x["slug"],
            "title": x["title"],
            "short_title": x["short"],
            "url": module_url(x),
            "fiche": fiche_href(x),
            "category": x["category"],
            "theme": x["theme"],
            "tags": x["tags"],
            "excerpt": x["excerpt"],
            "summary": x["lines"],
        })
        full[mid] = fold(md_plain(read(x["_brief_path"]) + "\n" + read(x["_source_path"])))

    (SITE / "search-index.json").write_text(
        json.dumps(light, ensure_ascii=False, indent=None, separators=(",", ":")),
        encoding="utf-8")
    (SITE / "search-fulltext.json").write_text(
        json.dumps(full, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    (SITE / "index.html").write_text(build_index(modules, tag_counts), encoding="utf-8")
    (SITE / ABOUT_PAGE).write_text(build_about(), encoding="utf-8")
    (SITE / "feed.xml").write_text(build_feed(modules), encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    (SITE / "CNAME").write_text(CUSTOM_DOMAIN + "\n", encoding="utf-8")
    n_days = len({m["date"] for m in modules})
    print(f"{len(modules)} module(s) sur {n_days} jour(s) construits, "
          f"{len(tag_counts)} mot(s)-cle(s), {len(modules) - len(sans_resume)} resume(s).")

if __name__ == "__main__":
    main()
