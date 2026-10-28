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
l'analyse complete ouverte. Champs editoriaux facultatifs :
  note        encadre « Note de cohérence » (deux briefs qui divergent, etc.)
  voir        liste d'ids de fiches liees (« Sur le même sujet »)
  doublon_de  id de la fiche de reference : la fiche reste servie (URL stable,
              canonical vers la reference) mais sort de l'accueil et du flux.
L'archive n'est jamais reecrite : toute correction passe par ce fichier.

ASSETS
------
scripts/assets/fonts/ (woff2 sous licence OFL, auto-heberges) et
scripts/assets/og.jpg sont copies tels quels dans site/assets/. Aucune
ressource n'est chargee depuis un tiers.

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
FONTS = ROOT / "scripts" / "assets" / "fonts"
OG_IMAGE = ROOT / "scripts" / "assets" / "og.jpg"
HERO = ROOT / "assets" / "hero"     # visuels du heros, deja convertis (AVIF, WebP, JPEG)    # image de partage, statique
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
CHAMPS_RESUME = ("titre_court", "quoi", "qui", "change", "theme", "note", "doublon_de")
# Champs facultatifs : note = encadre « Note de cohérence » affiche sur la fiche ;
# doublon_de = id de la fiche de reference (la fiche reste servie, hors accueil) ;
# voir = liste d'ids de fiches liees (« Sur le même sujet »).
FICHES_DIR = "fiches"
ABOUT_PAGE = "comment-cest-fait.html"

TAGS_VISIBLES = 12      # taille du nuage avant repli dans <details>
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
    # trop general pour filtrer (la moitie du corpus) : retire
    "droit-du-numerique": "",
}


def canon_tags(seq):
    """Replie les synonymes sur leur forme canonique, sans doublon."""
    out = []
    for t in seq:
        c = TAG_ALIAS.get(t, t)
        if c and c not in out:
            out.append(c)
    return out


# --------------------------------------------------------------------------- #
#  Charte graphique partagee : sombre par defaut, clair au choix (bouton).    #
#  Tailles et espacements en variables (--fs-*, --space-*). Polices auto-      #
#  hebergees (woff2, OFL) copiees depuis scripts/assets/fonts/.               #
# --------------------------------------------------------------------------- #
STYLE = """
@font-face{font-family:"Public Sans";src:url("fonts/public-sans-latin-wght-normal.woff2") format("woff2");
  font-weight:100 900;font-style:normal;font-display:swap}
@font-face{font-family:"Source Serif 4";src:url("fonts/source-serif-4-latin-wght-normal.woff2") format("woff2");
  font-weight:200 900;font-style:normal;font-display:swap}
@font-face{font-family:"Source Serif 4";src:url("fonts/source-serif-4-latin-wght-italic.woff2") format("woff2");
  font-weight:200 900;font-style:italic;font-display:swap}
@font-face{font-family:"JetBrains Mono";src:url("fonts/jetbrains-mono-latin-wght-normal.woff2") format("woff2");
  font-weight:100 800;font-style:normal;font-display:swap}

/* Echelles : tailles et espacements en variables, une seule source. */
:root{
  --fs-xs:.75rem; --fs-sm:.875rem; --fs-base:1rem; --fs-md:1.0625rem; --fs-lg:1.125rem;
  --fs-xl:1.25rem; --fs-2xl:1.5rem; --fs-3xl:1.875rem; --fs-4xl:2.25rem; --fs-5xl:2.75rem;
  --space-1:.25rem; --space-2:.5rem; --space-3:.75rem; --space-4:1rem; --space-5:1.25rem;
  --space-6:1.5rem; --space-8:2rem; --space-10:2.5rem; --space-12:3rem; --space-16:4rem;
  --radius:10px; --radius-sm:6px; --radius-full:999px;
  --measure:46rem; --ease:cubic-bezier(.2,.7,.2,1); --dur:.18s;
  --serif:"Source Serif 4","Iowan Old Style",Georgia,serif;
  --sans:"Public Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
  --mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;

  /* Sombre par defaut : encre bleu nuit, accent laiton. */
  color-scheme:dark;
  --bg:#141a2e; --surface:#1b2239; --surface-2:#232b46; --border:#2f3856; --border-strong:#46507a;
  --text:#ece6d9; --muted:#a9aec3; --accent:#e8c26f; --accent-hover:#f3d792; --on-accent:#1d1708;
  --link:#e8c26f; --mark:rgba(232,194,111,.2); --shadow:0 1px 0 rgba(255,255,255,.03),0 10px 30px rgba(5,8,20,.45);
  --note-bg:#262337; --note-border:#5b5170; --note-ink:#ecd29b;
  --ins:#e8c26f; --del:#e58e9c;
  --hero-bg:#010818; --hero-ink:#efe8da; --hero-muted:#b9bccb;
  --t-ia:#b49cff; --t-cyber:#f39a7b; --t-rgpd:#62c9a5; --t-dsa:#e8c862; --t-jurisprudence:#86b4ff; --t-autres:#a9aec3;
}
:root[data-theme=light]{
  color-scheme:light;
  --bg:#f4eee2; --surface:#fbf7ee; --surface-2:#ece4d3; --border:#dccfb8; --border-strong:#bfae90;
  --text:#2a2117; --muted:#5c4f3f; --accent:#8a4a14; --accent-hover:#6b370b; --on-accent:#ffffff;
  --link:#8a4a14; --mark:rgba(138,74,20,.12); --shadow:0 1px 2px rgba(42,33,23,.06),0 14px 34px rgba(42,33,23,.12);
  --note-bg:#fbf4e2; --note-border:#d9b96b; --note-ink:#5e4100;
  --ins:#8a4a14; --del:#9e3445;
  --hero-ink:#2a2117; --hero-muted:#5c4f3f;
  --t-ia:#6a48c4; --t-cyber:#b3401f; --t-rgpd:#1b7656; --t-dsa:#876500; --t-jurisprudence:#2a5cbf; --t-autres:#6a5f52;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-padding-top:var(--space-16)}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--sans);
  font-size:var(--fs-md);line-height:1.65;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
  font-kerning:normal}
a{color:var(--link);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.18em;
  text-decoration-color:color-mix(in srgb,currentColor 40%,transparent);transition:color var(--dur),text-decoration-color var(--dur)}
a:hover{color:var(--accent-hover);text-decoration-color:currentColor}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}
[hidden]{display:none !important}
html:not(.js) .needs-js{display:none !important}
::selection{background:var(--accent);color:var(--on-accent)}
em,i,cite{font-style:italic}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.icon{width:1em;height:1em;flex:0 0 auto;vertical-align:-.125em}

/* ---- en-tete ---- */
.skip{position:absolute;left:var(--space-2);top:-100px;background:var(--accent);color:var(--on-accent);
  padding:var(--space-2) var(--space-4);border-radius:var(--radius-sm);z-index:20;font-size:var(--fs-sm);font-weight:600}
.skip:focus{top:var(--space-2)}
.topbar{position:sticky;top:0;z-index:10;border-bottom:1px solid var(--border);
  background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:saturate(1.4) blur(8px);-webkit-backdrop-filter:saturate(1.4) blur(8px)}
.topbar .inner{max-width:var(--measure);margin:0 auto;padding:var(--space-3) var(--space-4);display:flex;
  align-items:center;justify-content:space-between;gap:var(--space-3)}
.brand{display:inline-flex;align-items:center;gap:var(--space-2);font-family:var(--serif);font-weight:700;
  font-size:var(--fs-lg);color:var(--text);text-decoration:none;letter-spacing:-.01em;white-space:nowrap}
.brand:hover{color:var(--text)}
.brand svg{width:22px;height:22px;color:var(--accent)}
.topbar nav{display:flex;align-items:center;gap:var(--space-1)}
.topbar nav a,.theme-toggle{display:inline-flex;align-items:center;gap:var(--space-2);min-height:40px;
  font-size:var(--fs-sm);color:var(--muted);padding:0 var(--space-3);border-radius:var(--radius-sm);text-decoration:none}
.topbar nav a:hover{color:var(--text);background:var(--surface-2)}
.topbar nav a[aria-current=page]{color:var(--text);font-weight:600;box-shadow:inset 0 -2px 0 var(--accent);border-radius:0}
.theme-toggle{background:none;border:1px solid var(--border);cursor:pointer;font:inherit;font-size:var(--fs-sm);
  min-width:40px;justify-content:center;padding:0 var(--space-2)}
.topbar .inner{display:grid;grid-template-columns:1fr auto 1fr}
.topbar nav{justify-self:center}
.topbar__end{justify-self:end;display:flex;align-items:center;gap:var(--space-2)}
.home .topbar{background:rgb(1 8 24/.72);border-bottom-color:rgb(236 230 217/.08)}
:root[data-theme=light] .home .topbar{background:color-mix(in srgb,var(--bg) 88%,transparent);border-bottom-color:var(--border)}
.topbar--wide .inner{max-width:72rem;padding-left:var(--space-6);padding-right:var(--space-6)}
.feed-pill{display:inline-flex;align-items:center;gap:var(--space-2);min-height:40px;padding:0 var(--space-4);
  border-radius:var(--radius-full);background:var(--accent);color:var(--on-accent);font-size:var(--fs-sm);font-weight:600;text-decoration:none}
.feed-pill:hover{background:var(--accent-hover);color:var(--on-accent)}
.feed-pill svg{width:16px;height:16px}
@media (max-width:560px){.feed-pill{padding:0 var(--space-3)}.topbar .inner{grid-template-columns:auto 1fr auto}}
.theme-toggle:hover{color:var(--text);border-color:var(--border-strong)}
.theme-toggle svg{width:18px;height:18px;transition:transform .4s var(--ease)}
.theme-toggle:hover svg{transform:rotate(20deg)}
.theme-toggle .i-sun{display:none}
:root[data-theme=light] .theme-toggle .i-sun{display:block}
:root[data-theme=light] .theme-toggle .i-moon{display:none}
@media (max-width:560px){.nav-label{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
  .topbar nav a{padding:0 var(--space-2)}.topbar--wide .inner{padding-left:var(--space-4);padding-right:var(--space-4)}}

.sitefoot{border-top:1px solid var(--border);color:var(--muted);font-size:var(--fs-sm);margin-top:var(--space-12)}
.sitefoot .inner{max-width:var(--measure);margin:0 auto;padding:var(--space-6) var(--space-4) var(--space-12)}
.sitefoot p{margin:0 0 var(--space-2)}
.sitefoot__links{display:flex;flex-wrap:wrap;gap:var(--space-2) var(--space-5);list-style:none;margin:0;padding:0}
.sitefoot a{color:var(--muted)}
.sitefoot a:hover{color:var(--text)}

.page,.wrap{max-width:var(--measure);margin:0 auto;padding:var(--space-8) var(--space-4) var(--space-12)}

/* ---- typographie ---- */
h1{font-family:var(--serif);font-weight:650;font-size:clamp(var(--fs-3xl),5.5vw,var(--fs-4xl));line-height:1.15;
  margin:0 0 var(--space-3);letter-spacing:-.02em;text-wrap:balance}
h2{font-family:var(--serif);font-weight:650;font-size:var(--fs-2xl);line-height:1.25;margin:var(--space-10) 0 var(--space-3);letter-spacing:-.01em;text-wrap:balance}
h3{font-size:var(--fs-lg);line-height:1.35;margin:var(--space-8) 0 var(--space-2)}
p{margin:0 0 var(--space-4)}
.doc p,.doc li{max-width:68ch}
code{background:var(--surface-2);border:1px solid var(--border);border-radius:var(--radius-sm);
  padding:1px 6px;font-size:.85em;color:var(--text);font-family:var(--mono)}
hr{border:0;border-top:1px solid var(--border);margin:var(--space-8) 0}
blockquote{margin:var(--space-4) 0;padding:var(--space-1) 0 var(--space-1) var(--space-4);border-left:3px solid var(--border-strong);color:var(--muted)}

/* ---- classes des infographies (contrat inchange) ---- */
.kicker,.wrap .tag{display:inline-block;font-size:var(--fs-xs);
  color:var(--accent);font-weight:600;background:var(--surface-2);border:1px solid var(--border);
  padding:var(--space-1) var(--space-3);border-radius:var(--radius-full);margin-bottom:var(--space-5)}
.principle{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:var(--space-5) var(--space-6);
  font-size:var(--fs-lg);margin:var(--space-6) 0}
.principle strong{color:var(--accent)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:var(--space-4);margin:var(--space-6) 0}
@media(max-width:640px){.grid{grid-template-columns:1fr}}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:var(--space-5) var(--space-6)}
.card h2{font-size:var(--fs-xs);
  color:var(--muted);margin:0 0 var(--space-3);font-weight:600}
.card.full{grid-column:1/-1}
.ref,.refs{font-size:var(--fs-base)}
.ref ul,.refs ul{margin:var(--space-2) 0 0;padding-left:var(--space-5)}
.ref li,.refs li{margin-bottom:var(--space-2)}
.ref a,.refs a,.doc a{overflow-wrap:anywhere}
.case b,.case strong{color:var(--text);background:linear-gradient(transparent 62%,var(--mark) 0);padding:0 1px}
.why{background:var(--note-bg);border:1px solid var(--note-border);border-radius:var(--radius);padding:var(--space-5) var(--space-6);margin:var(--space-6) 0}
.why h2{color:var(--note-ink);font-size:var(--fs-xs);
  margin:0 0 var(--space-2);font-weight:600}
.glossary dt,.wrap dl dt{font-weight:700;color:var(--accent);margin-top:var(--space-3)}
.glossary dd,.wrap dl dd{margin:2px 0 0;color:var(--muted)}
.wrap dl{margin:0}
footer{margin-top:var(--space-10);padding-top:var(--space-4);border-top:1px solid var(--border);color:var(--muted);font-size:var(--fs-sm)}
.gloss-grid{display:grid;gap:var(--space-3);margin-top:var(--space-1)}
.term b{display:block;color:var(--accent)}
.term span{display:block;color:var(--muted)}
.pills{display:flex;flex-wrap:wrap;gap:var(--space-2);margin:var(--space-5) 0}
.pill{display:inline-flex;align-items:center;font-size:var(--fs-sm);line-height:1.35;
  padding:var(--space-1) var(--space-3);border-radius:var(--radius-full);border:1px solid var(--border);background:var(--surface)}
.pill.yes{color:var(--accent)}
.pill.no{color:var(--muted)}
.verdict{display:inline-block;margin-top:var(--space-3);font-size:var(--fs-sm);color:var(--muted);
  border:1px solid var(--border);border-radius:var(--radius-full);padding:2px var(--space-3);background:var(--bg)}
.wrap .sub{color:var(--muted);font-size:var(--fs-lg);margin:-2px 0 var(--space-1)}
.wrap .date{color:var(--muted);font-size:var(--fs-sm);margin:-2px 0 var(--space-2)}

/* ---- accueil : en-tete ---- */
/* ---- accueil et 404 : heros cinematographique ----
   L'image (hemicycle de nuit) est le point focal. Le cadre .hero__frame a
   exactement le ratio de l'image et la recouvre comme object-fit:cover : les
   calques animes (faisceau, ecrans) y sont places en % de l'image elle-meme. */
.hero{position:relative;isolation:isolate;overflow:hidden;background:var(--hero-bg);color:var(--hero-ink);
  min-height:min(92vh,880px);display:flex;flex-direction:column;justify-content:flex-end}
.hero__media{position:absolute;inset:0;z-index:-2;container-type:size;overflow:hidden;
  background:var(--hero-bg) var(--lqip) right center/cover no-repeat}
.hero__frame{position:absolute;top:50%;right:0;transform:translateY(-50%);
  width:max(100cqw,177.87cqh);aspect-ratio:1672/940}
.hero__frame img{display:block;width:100%;height:100%}
.hero::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
  background:linear-gradient(90deg,var(--hero-bg) 0%,rgb(1 8 24/.92) 30%,rgb(1 8 24/.45) 55%,transparent 75%),
             linear-gradient(0deg,var(--bg) 0%,rgb(1 8 24/.6) 24%,transparent 45%)}
.grain::after{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;opacity:.09;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.beam{position:absolute;left:70%;width:16%;top:-4%;height:50%;pointer-events:none;mix-blend-mode:screen;
  background:radial-gradient(60% 100% at 50% 0%,rgb(255 190 90/.38),rgb(255 170 60/.12) 55%,transparent 75%);
  filter:blur(6px);opacity:.6}
.dust{position:absolute;left:72%;width:12%;top:0;height:40%;pointer-events:none;mix-blend-mode:screen;opacity:.55;
  background-image:radial-gradient(1px 1px at 20% 30%,#ffd9a0,transparent),radial-gradient(1px 1px at 70% 60%,#ffd9a0,transparent),
    radial-gradient(1.5px 1.5px at 45% 80%,#ffe3b5,transparent),radial-gradient(1px 1px at 85% 15%,#ffd9a0,transparent);
  background-size:60px 90px;-webkit-mask:linear-gradient(transparent,#000 20%,#000 70%,transparent);mask:linear-gradient(transparent,#000 20%,#000 70%,transparent)}
.screen{position:absolute;width:1.4%;aspect-ratio:1.6;translate:-50% -50%;border-radius:2px;pointer-events:none;
  background:#9cc4ff;mix-blend-mode:screen;filter:blur(3px);opacity:0}
.hero__body{position:relative;width:100%;max-width:72rem;margin:0 auto;padding:var(--space-16) var(--space-6) var(--space-8)}
.hero__text{max-width:40rem}
.pill{display:inline-flex;align-items:center;gap:var(--space-2);font-size:var(--fs-sm);font-weight:500;
  padding:var(--space-1) var(--space-3);border:1px solid rgb(232 194 111/.45);border-radius:var(--radius-full);
  color:var(--hero-ink);background:rgb(232 194 111/.08);margin:0 0 var(--space-5)}
.hero__title{font-family:var(--serif);font-weight:500;font-size:clamp(2.5rem,5.4vw,4.5rem);line-height:1.02;
  letter-spacing:-.03em;margin:0 0 var(--space-5);text-wrap:balance;color:var(--hero-ink)}
.hero .lede{color:var(--hero-muted);font-size:var(--fs-lg);max-width:32rem;margin:0 0 var(--space-6)}
.hero__cta{display:flex;flex-wrap:wrap;gap:var(--space-3)}
.btn-pill{display:inline-flex;align-items:center;gap:var(--space-2);min-height:44px;padding:0 var(--space-5);
  border-radius:var(--radius-full);font-size:var(--fs-base);font-weight:600;text-decoration:none;
  transition:background var(--dur),border-color var(--dur),color var(--dur)}
.btn-pill--main{background:var(--accent);color:var(--on-accent)}
.btn-pill--main:hover{background:var(--accent-hover);color:var(--on-accent)}
.btn-pill--ghost{border:1px solid rgb(236 230 217/.35);color:var(--hero-ink)}
.btn-pill--ghost:hover{border-color:var(--hero-ink);color:var(--hero-ink);background:rgb(236 230 217/.06)}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--space-6);margin:var(--space-12) 0 0;padding:var(--space-5) 0 0;
  border-top:1px solid rgb(236 230 217/.16);list-style:none}
.stats li{display:flex;flex-direction:column;gap:var(--space-1)}
.stats b{font-family:var(--serif);font-weight:500;font-size:clamp(var(--fs-xl),2.4vw,var(--fs-2xl));line-height:1.1;color:var(--hero-ink);
  font-variant-numeric:tabular-nums lining-nums}
.stats span{font-size:var(--fs-sm);color:var(--hero-muted)}
@media (max-width:760px){.stats{grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--space-5) var(--space-4)}}
/* Jusqu'a 1023 px : l'image passe au-dessus du texte, en bandeau 16:9 */
@media (max-width:1023px){
  .hero{min-height:0;display:block}
  .hero__media{position:relative;inset:auto;aspect-ratio:1672/940;container-type:normal}
  .hero__frame{position:absolute;inset:0;transform:none;width:100%;aspect-ratio:auto}
  .hero::before{background:linear-gradient(0deg,var(--hero-bg) 0%,transparent 40%);height:calc(100vw*940/1672);bottom:auto}
  .hero{background:linear-gradient(var(--hero-bg) 60%,var(--bg))}
  .hero__body{padding:var(--space-2) var(--space-4) var(--space-8)}
}
/* Mode clair : fond creme, l'image devient une grande carte arrondie a droite */
:root[data-theme=light] .hero{background:var(--bg);color:var(--text);min-height:0;display:block}
:root[data-theme=light] .hero::before{display:none}
@media (min-width:1024px){
  :root[data-theme=light] .hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);
    grid-template-areas:"text media" "stats stats";column-gap:var(--space-10);align-items:center;
    max-width:72rem;margin:0 auto;padding:var(--space-12) var(--space-6) var(--space-8)}
  :root[data-theme=light] .hero__body{display:contents}
  :root[data-theme=light] .hero__text{grid-area:text}
  :root[data-theme=light] .stats{grid-area:stats}
  :root[data-theme=light] .hero__media{grid-area:media;position:relative;inset:auto;aspect-ratio:1672/940;
    border-radius:20px;container-type:normal;box-shadow:var(--shadow)}
  :root[data-theme=light] .hero__frame{inset:0;transform:none;width:100%;aspect-ratio:auto}
}
@media (max-width:1023px){:root[data-theme=light] .hero__media{border-radius:0}}
:root[data-theme=light] .hero__text{max-width:none}
:root[data-theme=light] .hero__title{font-size:clamp(2.5rem,5vw,4.2rem)}
:root[data-theme=light] .pill{border-color:var(--border-strong);background:var(--surface);color:var(--text)}
:root[data-theme=light] .btn-pill--ghost{border-color:var(--border-strong)}
:root[data-theme=light] .btn-pill--ghost:hover{background:var(--surface-2)}
:root[data-theme=light] .stats{border-top-color:var(--border)}
@media (prefers-reduced-motion:no-preference){
  .beam{animation:beam 7s ease-in-out infinite alternate}
  .dust{animation:dust 18s linear infinite}
  .screen{animation:twinkle var(--t,5s) ease-in-out var(--d,0s) infinite}
  @keyframes beam{from{opacity:.45}to{opacity:.85}}
  @keyframes dust{to{background-position:0 -180px,12px -270px,-8px -180px,6px -360px}}
  @keyframes twinkle{0%,100%{opacity:0}45%,55%{opacity:.75}}
}
@media (prefers-reduced-motion:reduce){.beam,.dust,.screen{display:none}}

/* ---- frise des fiches (sous le heros) ---- */
.frise{margin:0 0 var(--space-8)}
.frise svg{display:block;width:100%;height:46px;overflow:visible}
.frise line{stroke-width:3;stroke-linecap:round}
.frise .axis{stroke:var(--border-strong);stroke-width:1}
.frise__months{position:relative;height:1.6em;margin:var(--space-2) 0 0;font-size:var(--fs-xs);color:var(--muted)}
.frise__months a{position:absolute;top:0;white-space:nowrap;padding-left:5px;border-left:1px solid var(--border-strong);color:var(--muted);text-decoration:none}
.frise__months a:hover{color:var(--text);text-decoration:underline}
.frise__legend{display:flex;flex-wrap:wrap;gap:var(--space-1) var(--space-4);margin:var(--space-3) 0 0;padding:0;list-style:none;font-size:var(--fs-xs);color:var(--muted)}
.frise__legend li{display:inline-flex;align-items:center;gap:6px}
.frise__legend li::before{content:"";width:10px;height:3px;border-radius:2px;background:var(--tc)}
.section-title{font-family:var(--serif);font-weight:600;font-size:var(--fs-2xl);margin:0 0 var(--space-4)}
.lede{color:var(--muted);font-size:var(--fs-lg);margin:0;max-width:60ch;line-height:1.6}
@media (max-width:600px){.hero{margin:0 0 var(--space-6)}.lede{font-size:var(--fs-base)}
  .page,.wrap{padding-top:var(--space-6)}}

/* ---- accueil : recherche et filtres ---- */
.toolbar{margin:0 0 var(--space-4)}
.search__field{position:relative;display:flex;align-items:center}
.search__field .icon{position:absolute;left:var(--space-4);color:var(--muted);width:18px;height:18px;pointer-events:none}
.search input[type=search]{width:100%;font:inherit;font-size:var(--fs-base);color:var(--text);min-height:48px;
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:var(--space-3) var(--space-12) var(--space-3) var(--space-12);appearance:none;-webkit-appearance:none;
  transition:border-color var(--dur),box-shadow var(--dur)}
.search input[type=search]::-webkit-search-cancel-button{display:none}
.search input[type=search]::placeholder{color:var(--muted);opacity:1}
.search input[type=search]:hover{border-color:var(--border-strong)}
.search input[type=search]:focus{border-color:var(--accent);outline:none;box-shadow:0 0 0 3px var(--mark)}
.search__clear{position:absolute;right:var(--space-2);background:none;border:0;color:var(--muted);font:inherit;
  font-size:var(--fs-xl);line-height:1;padding:var(--space-2) var(--space-3);cursor:pointer;border-radius:var(--radius-sm)}
.search__clear:hover{color:var(--text);background:var(--surface-2)}
.kbd{position:absolute;right:var(--space-3);font-family:var(--mono);font-size:var(--fs-xs);color:var(--muted);
  border:1px solid var(--border);border-radius:4px;padding:0 6px;pointer-events:none}
.search__opts{display:flex;align-items:center;gap:var(--space-2) var(--space-4);margin:var(--space-3) 0 0;
  font-size:var(--fs-sm);color:var(--muted);flex-wrap:wrap}
.search__opts input{accent-color:var(--accent);margin:0;width:16px;height:16px}
.search__opts label{display:inline-flex;align-items:center;gap:var(--space-2);cursor:pointer;min-height:32px}
.hint{color:var(--muted);font-size:var(--fs-sm)}
@media (hover:none),(max-width:600px){.kbd,#q-hint{display:none}}
.nojs{background:var(--note-bg);border:1px solid var(--note-border);color:var(--note-ink);
  border-radius:var(--radius);padding:var(--space-3) var(--space-4);font-size:var(--fs-sm);margin:var(--space-3) 0 0}
.themes{display:flex;flex-wrap:wrap;gap:var(--space-2);margin:var(--space-4) 0 0}
.theme-btn{font:inherit;font-size:var(--fs-sm);line-height:1.2;padding:var(--space-2) var(--space-4);border-radius:var(--radius-full);
  min-height:40px;border:1px solid var(--border);background:var(--surface);color:var(--text);cursor:pointer;
  display:inline-flex;align-items:center;gap:var(--space-2);transition:border-color var(--dur),background var(--dur),transform var(--dur)}
.theme-btn:hover{border-color:var(--border-strong);background:var(--surface-2)}
.theme-btn:active{transform:scale(.97)}
.theme-btn .dot{width:8px;height:8px;border-radius:50%;background:var(--tc,var(--muted))}
.theme-btn .n{font-size:var(--fs-xs);color:var(--muted)}
.theme-btn[aria-pressed=true]{background:var(--text);border-color:var(--text);color:var(--bg);font-weight:600}
.theme-btn[aria-pressed=true] .n{color:inherit;opacity:.8}
.tagbox{margin:var(--space-3) 0 0}
.tagbox>summary{font-size:var(--fs-sm);color:var(--muted);cursor:pointer;width:fit-content;padding:var(--space-2) 0}
.tagbox>summary:hover{color:var(--text)}
.tags{margin:var(--space-2) 0 0}
.tags__list{display:flex;flex-wrap:wrap;gap:var(--space-2);margin:0;padding:0;list-style:none}
.tags .tag{display:inline-flex;align-items:baseline;gap:5px;font-size:var(--fs-xs);line-height:1;
  padding:var(--space-2) var(--space-3);border-radius:var(--radius-full);border:1px solid var(--border);
  background:var(--surface);color:var(--muted);white-space:nowrap;text-decoration:none}
.tags .tag:hover{border-color:var(--border-strong);color:var(--text)}
.tag__n{opacity:.75}
.tags .tag.is-active{background:var(--text);border-color:var(--text);color:var(--bg);font-weight:600}
.tags details{margin-top:var(--space-2)}
.tags summary{font-size:var(--fs-sm);color:var(--muted);cursor:pointer;width:fit-content}

/* ---- accueil : statut ---- */
.status{display:flex;align-items:center;justify-content:space-between;gap:var(--space-3);
  flex-wrap:wrap;border-top:1px solid var(--border);padding-top:var(--space-3);margin:var(--space-6) 0 0;
  font-size:var(--fs-sm);color:var(--muted)}
.status__n{font-size:var(--fs-xs);letter-spacing:.02em}
.status__reset{font-size:var(--fs-sm)}
.empty{background:var(--surface);border:1px dashed var(--border-strong);border-radius:var(--radius);
  padding:var(--space-6);margin:var(--space-5) 0;text-align:center;color:var(--muted)}
.empty b{color:var(--text);font-weight:600}

/* ---- accueil : chronologie ---- */
.month{margin:0 0 var(--space-6)}
.month__head{position:sticky;top:var(--topbar-h,65px);z-index:3;background:var(--bg);margin:0;
  padding:var(--space-4) 0 var(--space-2);display:flex;align-items:baseline;justify-content:space-between;gap:var(--space-3);
  font-family:var(--serif);font-size:var(--fs-xl);font-weight:600;color:var(--text)}
.month__name::first-letter{text-transform:uppercase}
.month__count{font-family:var(--sans);font-size:var(--fs-sm);font-weight:400;color:var(--muted)}
.entries{display:grid;gap:var(--space-3);margin:0}

/* ---- carte ---- */
.entry{position:relative;background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);padding:var(--space-4) var(--space-5);
  transition:border-color var(--dur),transform var(--dur) var(--ease),box-shadow var(--dur)}
@media (hover:hover){.entry:hover{border-color:var(--border-strong)}
  .entry:hover .entry__title a{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.15em}}
.entry:focus-within{border-color:var(--accent)}
.entry__meta,.fiche__meta{display:flex;align-items:center;flex-wrap:wrap;gap:var(--space-2) var(--space-3);
  font-size:var(--fs-xs);color:var(--muted);margin:0 0 var(--space-2)}
.date{font-size:var(--fs-sm);font-weight:600;color:var(--text);font-variant-numeric:tabular-nums}
.ago{font-size:var(--fs-xs);color:var(--accent)}
.badge{display:inline-flex;align-items:center;gap:6px;font-size:var(--fs-xs);font-weight:600;color:var(--text)}
.badge::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--tc,var(--muted))}
.t-ia{--tc:var(--t-ia)}.t-cyber{--tc:var(--t-cyber)}.t-rgpd{--tc:var(--t-rgpd)}
.t-dsa{--tc:var(--t-dsa)}.t-jurisprudence{--tc:var(--t-jurisprudence)}.t-autres{--tc:var(--t-autres)}
.entry__slug{font-size:var(--fs-xs);color:var(--muted)}
.entry__title{font-family:var(--serif);font-size:var(--fs-xl);font-weight:600;line-height:1.3;
  letter-spacing:-.01em;margin:0;text-wrap:pretty}
.entry__title a{color:var(--text);text-decoration:none}
.entry__title a::after{content:"";position:absolute;inset:0;border-radius:var(--radius)}
.entry__title a:focus-visible{outline:none}
.entry:has(.entry__title a:focus-visible){outline:2px solid var(--accent);outline-offset:3px}
.entry__change{margin:var(--space-2) 0 0;color:var(--muted);font-size:var(--fs-base);line-height:1.55;
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.entry__change b{color:var(--text);font-weight:600}
mark{background:var(--mark);color:inherit;border-radius:2px;box-shadow:0 1px 0 var(--accent)}
.entry--featured{padding:var(--space-6);border-color:var(--border-strong)}
.entry--featured .entry__title{font-size:clamp(var(--fs-2xl),4vw,var(--fs-3xl));line-height:1.2}
.entry--featured .date{font-size:var(--fs-sm)}
.entry__flag{font-size:var(--fs-xs);font-weight:600;
  color:var(--on-accent);background:var(--accent);border-radius:var(--radius-full);padding:2px var(--space-2)}
.entry--featured .trois{margin-top:var(--space-4)}
.entry__more{display:inline-flex;align-items:center;gap:var(--space-1);margin-top:var(--space-4);font-size:var(--fs-sm);font-weight:600;color:var(--accent)}
.entry__more svg{transition:transform var(--dur) var(--ease)}

/* ---- trois lignes ---- */
.trois{margin:0;display:grid;gap:var(--space-3)}
.trois>div{display:grid;grid-template-columns:10em 1fr;gap:2px var(--space-4);align-items:baseline}
.trois dt{font-size:var(--fs-sm);font-weight:600;color:var(--muted)}
.trois dd{margin:0;line-height:1.6}
@media (max-width:600px){.trois>div{grid-template-columns:1fr}}

/* ---- page fiche ---- */
.backlink{font-size:var(--fs-sm);margin:0 0 var(--space-6)}
.backlink a{display:inline-flex;align-items:center;gap:var(--space-1);color:var(--muted);text-decoration:none}
.backlink a:hover{color:var(--text)}
.fiche__meta{margin:0 0 var(--space-4);font-size:var(--fs-sm)}
.fiche__meta .date{font-size:var(--fs-sm)}
.fiche__full{color:var(--muted);font-family:var(--serif);font-style:italic;font-size:var(--fs-base);line-height:1.5;margin:0 0 var(--space-2)}
.fiche__full .lbl{display:block;font-style:normal;font-size:var(--fs-xs);margin-bottom:2px}
.resume{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:var(--space-5) var(--space-6);margin:var(--space-6) 0}
.resume .trois dd{font-size:var(--fs-md)}
.note{background:var(--note-bg);border:1px solid var(--note-border);border-radius:var(--radius);
  padding:var(--space-4) var(--space-5);margin:var(--space-6) 0;color:var(--text);font-size:var(--fs-base)}
.note h2{display:flex;align-items:center;gap:var(--space-2);font-size:var(--fs-xs);font-weight:600;
  color:var(--note-ink);margin:0 0 var(--space-2)}
.note p:last-child{margin:0}
.analyse{margin:var(--space-6) 0;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface)}
.analyse>summary{cursor:pointer;padding:var(--space-4) var(--space-5);font-weight:600;list-style:none;min-height:48px;
  display:flex;justify-content:space-between;align-items:center;gap:var(--space-3);border-radius:var(--radius)}
.analyse>summary::-webkit-details-marker{display:none}
.analyse>summary svg{width:20px;height:20px;color:var(--muted);transition:transform var(--dur) var(--ease)}
.analyse[open]>summary svg{transform:rotate(180deg)}
.analyse>summary:hover{background:var(--surface-2)}
.analyse[open]>summary{border-bottom:1px solid var(--border);border-radius:var(--radius) var(--radius) 0 0}
.analyse__body{padding:var(--space-2) var(--space-6) var(--space-2)}
.analyse__body h2{font-size:var(--fs-xl);margin-top:var(--space-8)}
.fiche>article>section>h2{font-size:var(--fs-xl);margin:var(--space-10) 0 var(--space-3)}
.sources{list-style:none;padding:0;margin:0;display:grid;gap:var(--space-2)}
.sources li{margin:0;padding:var(--space-3) var(--space-4);background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);
  font-size:var(--fs-base);line-height:1.5}
.sources a{display:block;margin:calc(-1*var(--space-3)) calc(-1*var(--space-4));padding:var(--space-3) var(--space-4);
  color:var(--text);text-decoration:none;border-radius:var(--radius-sm)}
.sources a:hover{background:var(--surface-2);color:var(--text)}
.sources a:hover .src-host{color:var(--accent)}
.sources .src-host{display:block;font-size:var(--fs-xs);color:var(--muted);margin-bottom:2px;transition:color var(--dur)}
.linkrow{display:flex;flex-wrap:wrap;gap:var(--space-2);margin:0}
.btn{display:inline-flex;align-items:center;gap:var(--space-2);min-height:40px;font-size:var(--fs-sm);font-weight:500;
  padding:var(--space-2) var(--space-4);border-radius:var(--radius-sm);text-decoration:none;
  background:var(--surface);color:var(--text);border:1px solid var(--border);transition:border-color var(--dur),background var(--dur)}
.btn:hover{border-color:var(--border-strong);background:var(--surface-2);color:var(--text)}
.btn svg{width:16px;height:16px;color:var(--muted)}
.related{list-style:none;padding:0;margin:0;display:grid;gap:var(--space-2)}
.related a{display:block;padding:var(--space-3) var(--space-4);border:1px solid var(--border);border-radius:var(--radius-sm);
  background:var(--surface);color:var(--text);text-decoration:none;font-family:var(--serif);font-weight:600;line-height:1.35}
.related a:hover{border-color:var(--border-strong);background:var(--surface-2)}
.related .date{display:block;margin-bottom:2px;color:var(--muted);font-weight:500}
.pager{display:grid;grid-template-columns:1fr 1fr;gap:var(--space-3);margin:var(--space-10) 0 0}
.pager a{display:block;padding:var(--space-4);border:1px solid var(--border);border-radius:var(--radius);
  background:var(--surface);color:var(--text);text-decoration:none;font-family:var(--serif);font-weight:600;line-height:1.35}
.pager a:hover{border-color:var(--border-strong);background:var(--surface-2)}
.pager small{display:block;color:var(--muted);font-size:var(--fs-xs);font-weight:500;
  margin-bottom:var(--space-1)}
.pager__next{text-align:right;grid-column:2}
@media (max-width:600px){.pager{grid-template-columns:1fr}.pager__next{grid-column:auto;text-align:left}}
.fiche-tags{display:flex;flex-wrap:wrap;gap:var(--space-2);list-style:none;margin:var(--space-8) 0 0;padding:0}
.fiche-tags a{display:inline-block;font-size:var(--fs-xs);color:var(--muted);border:1px solid var(--border);
  border-radius:var(--radius-full);padding:var(--space-1) var(--space-3);background:var(--surface);text-decoration:none}
.fiche-tags a:hover{color:var(--text);border-color:var(--border-strong)}

/* ---- pages Markdown et « Comment c'est fait » ---- */
.doc .meta{color:var(--muted);font-size:var(--fs-sm);margin:-2px 0 var(--space-8)}
.doc ul,.doc ol{padding-left:var(--space-6);margin:0 0 var(--space-4)}
.doc li{margin-bottom:var(--space-2)}
.about ol.steps{list-style:none;counter-reset:s;padding:0;margin:0 0 var(--space-6);display:grid;gap:var(--space-2)}
.about ol.steps li{counter-increment:s;position:relative;padding:var(--space-4) var(--space-5) var(--space-4) var(--space-16);margin:0;
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);max-width:none}
.about ol.steps li::before{content:counter(s,decimal-leading-zero);position:absolute;left:var(--space-5);top:var(--space-4);
  color:var(--accent);font-weight:600;font-size:var(--fs-sm)}
.about ol.steps strong{display:block}

/* ---- 404 ---- */
.notfound{text-align:left;padding-top:var(--space-12)}
.notfound .code{color:var(--accent);font-size:var(--fs-sm);}

/* ---- mouvement ---- */
@media (prefers-reduced-motion:no-preference){
  .analyse[open] .analyse__body{animation:open .25s var(--ease)}
  @keyframes open{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:none}}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{transition:none !important;animation:none !important;scroll-behavior:auto !important}
}
@media print{.topbar,.sitefoot,.pager,.theme-toggle{display:none}.analyse__body{display:block}body{background:#fff;color:#000}}
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
def _autolink(m):
    url = m.group(1)
    tail = re.search(r"[.,;:!?»]+$", url)
    tail = tail.group(0) if tail else ""
    url = url[:len(url) - len(tail)]
    return f'<a href="{url}">{url}</a>{tail}'

def md_inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://(?:[^\s()<]|\([^\s()<]*\))+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r'(?<![">=])(https?://(?:[^\s()<]|\([^\s()<]*\))+)',
               _autolink, s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*([^*\s][^*]*?)\*(?![*\w])", r"<em>\1</em>", s)
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
NAV = (("index", "index.html", "Fiches", "list"),
       ("about", ABOUT_PAGE, "Comment c’est fait", "info"))

# Icones SVG inline (traits 1.75, currentColor) : aucune police d'icones, aucun CDN.
ICONS = {
    "logo": '<path d="M12 3v18M5 7h14M7 7l-3 7a3 3 0 0 0 6 0L7 7Zm10 0-3 7a3 3 0 0 0 6 0l-3-7ZM8 21h8"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/>',
    "rss": '<path d="M4 11a9 9 0 0 1 9 9M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/>',
    "moon": '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "arrow-left": '<path d="M19 12H5M12 19l-7-7 7-7"/>',
    "arrow-right": '<path d="M5 12h14M12 5l7 7-7 7"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "alert": '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4M12 17h.01"/>',
    "chart": '<path d="M3 3v18h18M7 15l4-4 3 3 5-6"/>',
    "file": '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/>',
    "download": '<path d="M12 3v12M7 10l5 5 5-5M5 21h14"/>',
}

def icon(name, cls="icon"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true" focusable="false">{ICONS[name]}</svg>')

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
           '<rect width="32" height="32" rx="7" fill="#141a2e"/>'
           '<g fill="none" stroke="#e5bc6e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
           '<path d="M16 6v20M9 10h14M11 10l-3 7a3 3 0 0 0 6 0l-3-7Zm10 0-3 7a3 3 0 0 0 6 0l-3-7ZM12 26h8"/>'
           '</g></svg>')

# Lu avant le premier rendu : evite le flash de theme. Sombre si aucun choix.
THEME_INIT = ("<script>document.documentElement.classList.add('js');"
              "try{var t=localStorage.getItem('dv-theme');"
              "if(t==='light'||t==='dark')document.documentElement.dataset.theme=t}catch(e){}</script>")

def topbar(prefix, current=None, wide=False):
    links = "".join(
        f'<a href="{prefix}{href}"' + (' aria-current="page"' if key == current else "")
        + f'>{icon(ico)}<span class="nav-label">{html.escape(label)}</span></a>'
        for key, href, label, ico in NAV)
    toggle = ('<button type="button" class="theme-toggle" id="theme-toggle" '
              'aria-label="Activer le thème clair" hidden>'
              + icon("moon", "i-moon") + icon("sun", "i-sun") + '</button>')
    feed = (f'<a class="feed-pill" href="{prefix}feed.xml" type="application/atom+xml">{icon("rss")}'
            f'<span class="nav-label">Suivre le flux</span></a>')
    return (f'<a class="skip" href="#main">Aller au contenu</a>'
            f'<header class="topbar{" topbar--wide" if wide else ""}"><div class="inner">'
            f'<a class="brand" href="{prefix}index.html">{icon("logo")}Droit Vivant</a>'
            f'<nav aria-label="Navigation principale">{links}</nav>'
            f'<div class="topbar__end">{toggle}{feed}</div>'
            f'</div></header>')

DISCLAIMER = ("Contenu pédagogique, rédigé avec l’aide d’un LLM à partir de sources publiques : "
              "il ne constitue pas un conseil juridique. Les sources citées font foi.")

def site_footer(prefix, feed=False):
    links = [f'<a href="{prefix}{ABOUT_PAGE}">Comment c’est fait</a>',
             f'<a href="{prefix}feed.xml">Flux Atom</a>']
    return (f'<footer class="sitefoot"><div class="inner">'
            f'<p>{DISCLAIMER}</p><ul class="sitefoot__links">{"".join(f"<li>{l}</li>" for l in links)}</ul></div></footer>')

def head(title, prefix, desc="", path="", canonical=None, og_type="website", extra=""):
    """<head> commun : meta, Open Graph, favicon, flux, feuille de style."""
    t, d = html.escape(title, quote=True), html.escape(desc, quote=True)
    url = SITE_URL + (canonical if canonical is not None else path)
    out = ['<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">',
           '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
           f'<title>{html.escape(title)}</title>', THEME_INIT]
    if desc:
        out.append(f'<meta name="description" content="{d}">')
    out += [f'<link rel="canonical" href="{html.escape(url, quote=True)}">',
            '<meta property="og:site_name" content="Droit Vivant">',
            '<meta property="og:locale" content="fr_FR">',
            f'<meta property="og:type" content="{og_type}">',
            f'<meta property="og:title" content="{t}">',
            f'<meta property="og:url" content="{html.escape(url, quote=True)}">',
            f'<meta property="og:image" content="{SITE_URL}assets/og.jpg">',
            '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
            '<meta property="og:image:alt" content="Droit Vivant, veille juridique du droit du numérique">',
            '<meta name="twitter:card" content="summary_large_image">',
            '<meta name="theme-color" content="#141a2e">',
            f'<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">',
            f'<link rel="alternate" type="application/atom+xml" title="Droit Vivant — flux Atom" href="{prefix}feed.xml">',
            f'<link rel="preload" href="{prefix}assets/fonts/public-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>',
            f'<link rel="preload" href="{prefix}assets/fonts/source-serif-4-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>',
            f'<link rel="stylesheet" href="{prefix}assets/style.css">',
            f'<script src="{prefix}assets/site.js" defer></script>']
    if desc:
        out.append(f'<meta property="og:description" content="{d}">')
    out.append(extra)
    return "".join(out) + "</head>"

def shell(title, body, prefix, current=None, desc="", footer=True, feed=False,
          path="", canonical=None, og_type="website", extra=""):
    return (head(title, prefix, desc, path, canonical, og_type, extra) + '<body>'
            f'{topbar(prefix, current)}{body}'
            f'{site_footer(prefix, feed) if footer else ""}</body></html>')

def back_to_fiche(href):
    return (f'<p class="backlink"><a href="{href}">{icon("arrow-left")} Revenir à la fiche</a></p>'
            if href else "")

def render_md_page(md_text, kicker, prefix, raw_md_name=None, raw_label=None, path="", fiche=""):
    title = md_title(md_text) or kicker
    meta = ""
    if raw_md_name:
        meta = (f'<p class="meta"><a href="{raw_md_name}">{icon("download")} '
                f'{html.escape(raw_label or "Version .md brute")}</a></p>')
    body = (f'<main class="page" id="main">{back_to_fiche(fiche)}<span class="kicker">{html.escape(kicker)}</span>'
            f'<article class="doc">{meta}{md_to_html(md_text)}</article></main>')
    return shell(f"{title} — Droit Vivant", body, prefix, path=path,
                 desc=excerpt_of(md_text), og_type="article")

def reskin_infographie(t, fiche=""):
    """Retire le CSS inline et applique la charte partagee + barre de navigation."""
    t = re.sub(r"<style[^>]*>.*?</style>", "", t, flags=re.S | re.I)
    p = "../../"
    extra = (THEME_INIT + f'<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">'
             f'<link rel="stylesheet" href="{p}assets/style.css">'
             f'<script src="{p}assets/site.js" defer></script>')
    if "assets/style.css" not in t:
        if re.search(r"</head>", t, re.I):
            t = re.sub(r"</head>", lambda m: extra + "\n</head>", t, count=1, flags=re.I)
        else:
            t = extra + t
    if re.search(r"<body[^>]*>", t, re.I):
        t = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + topbar(p),
                   t, count=1, flags=re.I)
    t = promote_main(ensure_wrap(t))
    if fiche:
        t = re.sub(r'(<main class="wrap" id="main"[^>]*>)', lambda m: m.group(1) + back_to_fiche(fiche),
                   t, count=1)
    return t

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
            voir = val.get("voir")
            if isinstance(voir, list):
                out[str(key)]["voir"] = [str(v) for v in voir if isinstance(v, str)]
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
        x["note"] = r.get("note", "")
        x["voir"] = r.get("voir", [])
        x["doublon_de"] = r.get("doublon_de", "")
        if len(x["lines"]) < len(LIGNES) and not x["doublon_de"]:
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
    return f'<span class="badge t-{key}">{html.escape(THEMES[key])}</span>'

def fr_short(iso):
    y, m, d = (int(v) for v in iso.split("-"))
    return f"{'1er' if d == 1 else d} {MOIS_COURT[m - 1]} {y}"

def date_tag(iso, long=False):
    """Date toujours visible : c'est une veille d'actualite. data-ago est
    complete cote client (« il y a 3 jours »), le texte reste sans JS."""
    label = fr_long(iso) if long else fr_short(iso)
    return (f'<time class="date" datetime="{iso}">{label}</time>'
            f'<span class="ago" data-ago="{iso}"></span>')

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

def host_of(url):
    h = re.sub(r"^https?://", "", url).split("/")[0].split("?")[0]
    return h[4:] if h.startswith("www.") else h

def sources_html(src_md):
    """Sources en cartes : domaine en petit, intitule en clair. Une URL nue
    devient « domaine › chemin abrege » plutot qu'une adresse illisible."""
    items = []
    for line in src_md.split("\n"):
        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if not m:
            continue
        raw = m.group(1).strip()
        lm = re.search(r"\[([^\]]+)\]\((https?://[^\s]+?)\)(?:\s|$|[.,;])", raw + " ")
        um = re.match(r"^(https?://\S+)$", raw)
        if lm:
            url, label = lm.group(2), md_inline(lm.group(1))
            rest = raw[:lm.start()] + raw[lm.end() - 1:]
            rest = md_inline(rest.strip(" —-:")) if rest.strip(" —-:.") else ""
            label += f" <span class=\"hint\">{rest}</span>" if rest else ""
        elif um:
            url = um.group(1).rstrip(".,;")
            path = re.sub(r"^https?://[^/]+/?", "", url)
            path = (path[:60] + "…") if len(path) > 60 else path
            label = html.escape(path or host_of(url))
        else:
            items.append(f"<li>{md_inline(raw)}</li>")
            continue
        items.append(f'<li><a href="{html.escape(url, quote=True)}">'
                     f'<span class="src-host">{html.escape(host_of(url))}</span>{label}</a></li>')
    if not items:
        return f'<div class="doc">{md_to_html(src_md)}</div>'
    return f'<ul class="sources">{"".join(items)}</ul>'

# --------------------------------------------------------------------------- #
#  Accueil : une carte par module                                              #
# --------------------------------------------------------------------------- #
def entry_card(x, featured=False):
    mid = module_id(x)
    meta = []
    meta += [date_tag(x["date"]), theme_badge(x["theme"])]
    if x["multi"]:
        meta.append(f'<span class="entry__slug">{html.escape(slug_label(x))}</span>')
    if featured:
        body = lines_html(x)
    else:
        ch = x["lines"].get("change") or x["lines"].get("quoi") or x["excerpt"]
        body = f'<p class="entry__change">{html.escape(ch)}</p>' if ch else ""
    more = ('<span class="entry__more" aria-hidden="true">Lire la fiche</span>'
            if featured else "")
    cls = "entry" + (" entry--featured" if featured else "")
    hn = "h2" if featured else "h3"
    return (f'<article class="{cls}" id="e-{mid}" data-id="{mid}" data-day="{x["date"]}" '
            f'data-theme="{x["theme"]}">'
            f'<div class="entry__meta">{"".join(meta)}</div>'
            f'<{hn} class="entry__title"><a href="{fiche_href(x)}">{html.escape(x["short"])}</a></{hn}>'
            f'{body}{more}</article>')

def tag_chip(tag, n, extra=""):
    return (f'<li><a class="tag{extra}" href="?tag={tag}" data-tag="{tag}">'
            f'#{html.escape(tag)}<span class="tag__n">{n}</span></a></li>')

# --------------------------------------------------------------------------- #
#  Page fiche                                                                  #
# --------------------------------------------------------------------------- #
def related_html(ids, by_id, prefix=""):
    lis = []
    for i in ids:
        y = by_id.get(i)
        if y:
            lis.append(f'<li><a href="{prefix}{sibling_href(y)}"><span class="date">{fr_short(y["date"])}</span>'
                       f'{html.escape(y["short"])}</a></li>')
    return f'<ul class="related">{"".join(lis)}</ul>' if lis else ""

def render_fiche(x, i, listed, by_id):
    prefix = "../"
    body_md, src_md = split_brief(read(x["_brief_path"]))
    meta = [date_tag(x["date"], long=True), theme_badge(x["theme"])]
    if x["multi"]:
        meta.append(f'<span class="entry__slug">{html.escape(slug_label(x))}</span>')

    parts = [f'<p class="backlink"><a href="{prefix}index.html">{icon("arrow-left")} Toutes les fiches</a></p>',
             f'<div class="fiche__meta">{"".join(meta)}</div>',
             f'<h1>{html.escape(x["short"])}</h1>']
    if x["short"] != x["title"]:
        parts.append(f'<p class="fiche__full"><span class="lbl">Titre d’origine du brief</span>'
                     f'{html.escape(x["title"])}</p>')

    ref = by_id.get(x["doublon_de"]) if x["doublon_de"] else None
    if ref:
        parts.append('<aside class="note" aria-labelledby="note-h">'
                     f'<h2 id="note-h">{icon("alert")}Fiche en double</h2>'
                     '<p>Ce module ne comporte qu’une infographie et traite le même sujet que '
                     f'la fiche du {fr_day(ref["date"])}, qui contient le brief et les sources. '
                     f'<a href="{sibling_href(ref)}">Lire la fiche de référence</a>.</p></aside>')
    if x["note"]:
        parts.append('<aside class="note" aria-labelledby="note-h">'
                     f'<h2 id="note-h">{icon("alert")}Note de cohérence</h2>'
                     f'<p>{html.escape(x["note"])}</p></aside>')
    if x["lines"]:
        parts.append('<section class="resume" aria-label="En trois lignes">'
                     f'{lines_html(x)}</section>')

    if body_md:
        # sans resume, l'analyse est la seule matiere de la page : on la deplie
        opened = "" if x["lines"] else " open"
        parts.append(f'<details class="analyse"{opened}><summary>Lire l’analyse complète {icon("chevron")}</summary>'
                     f'<div class="analyse__body doc">{md_to_html(body_md)}</div></details>')
    elif not ref:
        parts.append('<p>Ce module ne comporte pas de brief écrit.'
                     + (' L’infographie en donne la synthèse.' if x["infographie"] else "")
                     + '</p>')

    if src_md:
        parts.append('<section aria-labelledby="sources"><h2 id="sources">Sources</h2>'
                     f'{sources_html(src_md)}</section>')

    links = []
    if x["infographie"]:
        links.append(f'<a class="btn" href="{prefix}{x["infographie"]}">{icon("chart")}Infographie</a>')
    if x["brief"]:
        links.append(f'<a class="btn" href="{prefix}{x["brief"][:-3]}.html">{icon("file")}Brief (page)</a>')
    if x["source"]:
        links.append(f'<a class="btn" href="{prefix}{x["source"][:-3]}.html">{icon("file")}Source NotebookLM</a>')
        links.append(f'<a class="btn" href="{prefix}{x["source"]}" download>{icon("download")}Source (.md)</a>')
    if x["brief"]:
        links.append(f'<a class="btn" href="{prefix}{x["brief"]}" download>{icon("download")}Brief (.md)</a>')
    if links:
        parts.append(f'<section aria-labelledby="plus"><h2 id="plus">Aller plus loin</h2>'
                     f'<div class="linkrow">{"".join(links)}</div></section>')

    rel_html = related_html(x["voir"], by_id)
    if rel_html:
        parts.append(f'<section aria-labelledby="voir"><h2 id="voir">Sur le même sujet</h2>{rel_html}</section>')

    if x["tags"]:
        chips = "".join(f'<li><a href="{prefix}index.html?tag={t}">#{html.escape(t)}</a></li>'
                        for t in x["tags"])
        parts.append(f'<nav aria-label="Mots-clés"><ul class="fiche-tags">{chips}</ul></nav>')

    pager = ""
    if i is not None:
        newer = listed[i - 1] if i > 0 else None
        older = listed[i + 1] if i + 1 < len(listed) else None
        if older:
            pager += (f'<a href="{sibling_href(older)}"><small>&larr; Plus ancienne</small>'
                      f'{html.escape(older["short"])}</a>')
        if newer:
            pager += (f'<a class="pager__next" href="{sibling_href(newer)}"><small>Plus récente &rarr;</small>'
                      f'{html.escape(newer["short"])}</a>')
    if pager:
        parts.append(f'<nav class="pager" aria-label="Fiches voisines">{pager}</nav>')

    desc = x["lines"].get("quoi") or x["excerpt"] or x["title"]
    body = f'<main class="page fiche" id="main"><article>{"".join(parts)}</article></main>'
    canon = fiche_href(ref) if ref else None
    return shell(f'{x["short"]} — Droit Vivant', body, prefix, desc=desc,
                 path=fiche_href(x), canonical=canon, og_type="article")

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
    var kbd = document.getElementById('q-kbd');
    if (kbd) kbd.hidden = !!raw;
    highlight(query ? query.split(/\s+/).filter(function (w) { return w.length > 1; }) : []);
    writeURL(!!push);
  }

  /* ---- surlignage des termes dans les titres et resumes visibles ---- */
  var hlNodes = cards.map(function (c) {
    return Array.prototype.slice.call(c.querySelectorAll('.entry__title a, .entry__change, .trois dd'))
      .map(function (el) { return { el: el, text: el.textContent }; });
  });
  function highlight(words) {
    cards.forEach(function (card, k) {
      hlNodes[k].forEach(function (n) {
        if (!words.length || card.hidden) { if (n.el.firstElementChild) n.el.textContent = n.text; return; }
        var f = fold(n.text), marks = [];
        words.forEach(function (w) {
          var i = -1;
          while (w && (i = f.indexOf(w, i + 1)) !== -1) marks.push([i, i + w.length]);
        });
        if (!marks.length) { n.el.textContent = n.text; return; }
        marks.sort(function (a, b) { return a[0] - b[0]; });
        n.el.textContent = '';
        var pos = 0;
        marks.forEach(function (m) {
          if (m[0] < pos) return;
          n.el.appendChild(document.createTextNode(n.text.slice(pos, m[0])));
          var mk = document.createElement('mark'); mk.textContent = n.text.slice(m[0], m[1]);
          n.el.appendChild(mk); pos = m[1];
        });
        n.el.appendChild(document.createTextNode(n.text.slice(pos)));
      });
    });
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
#  Script commun a toutes les pages (assets/site.js) : theme, dates relatives, #
#  apparition des cartes. Tout est facultatif : sans JS, la page est complete. #
# --------------------------------------------------------------------------- #
SITE_JS = r"""
(function () {
  var doc = document.documentElement;
  doc.classList.add('js');   /* deja pose dans <head> ; repli si absent */

  /* ---- theme : sombre par defaut, choix memorise ---- */
  var btn = document.getElementById('theme-toggle');
  function label() {
    if (!btn) return;
    var light = doc.getAttribute('data-theme') === 'light';
    btn.setAttribute('aria-label', light ? 'Activer le thème sombre' : 'Activer le thème clair');
    btn.title = btn.getAttribute('aria-label');
    var meta = document.querySelector('meta[name=theme-color]');
    if (meta) meta.setAttribute('content', light ? '#f4eee2' : '#141a2e');
  }
  if (btn) {
    btn.hidden = false;
    label();
    btn.addEventListener('click', function () {
      var next = doc.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      doc.setAttribute('data-theme', next);
      try { localStorage.setItem('dv-theme', next); } catch (e) {}
      label();
    });
  }

  /* ---- dates relatives : « aujourd'hui », « il y a 3 jours » ---- */
  var today = new Date(); today.setHours(0, 0, 0, 0);
  Array.prototype.forEach.call(document.querySelectorAll('[data-ago]'), function (el) {
    var p = el.getAttribute('data-ago').split('-');
    var d = new Date(+p[0], +p[1] - 1, +p[2]);
    var n = Math.round((today - d) / 86400000);
    var txt = '';
    if (n === 0) txt = 'aujourd’hui';
    else if (n === 1) txt = 'hier';
    else if (n > 1 && n < 31) txt = 'il y a ' + n + ' jours';
    el.textContent = txt;
    el.hidden = !txt;
  });

})();
"""

# --------------------------------------------------------------------------- #
#  Flux Atom : une veille se lit dans un agregateur                            #
# --------------------------------------------------------------------------- #
SITE_URL = "https://droit-vivant.maxzer.fr/"
CUSTOM_DOMAIN = "droit-vivant.maxzer.fr"
REPO_URL = "https://github.com/maax6/droit-vivant"
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
        # id historique (infographie) conserve ; le lien mene desormais a la fiche
        url = SITE_URL + module_url(x)
        out.append("<entry>")
        out.append("<title>" + esc(x["short"]) + "</title>")
        out.append(f'<link rel="alternate" type="text/html" href="{esc(SITE_URL + fiche_href(x))}"/>')
        out.append("<id>" + esc(url) + "</id>")
        out.append("<updated>" + x["date"] + "T12:00:00Z</updated>")
        for t in x["tags"]:
            out.append(f'<category term="{esc(t)}"/>')
        summary = " ".join(x["lines"][k] for k in ("quoi", "change") if k in x["lines"]) or x["excerpt"]
        if summary:
            out.append("<summary>" + esc(summary) + "</summary>")
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
        '<p>Quand deux briefs se contredisent sur un fait, la fiche l’indique dans une <strong>note '
        'de cohérence</strong> et renvoie vers les sources officielles. Quand un titre d’origine '
        'contredit son brief, la fiche affiche un titre neutre ; le titre du brief reste visible, '
        'étiqueté comme tel. Un module publié deux fois est signalé comme doublon et renvoie vers '
        'la fiche de référence. Les fichiers d’archive ne sont jamais réécrits.</p>'
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
        f'<p>Le script de génération, l’archive et les résumés sont versionnés dans un <a href="{REPO_URL}">dépôt '
        'Git</a>. Les nouveautés sont aussi disponibles par <a href="feed.xml">flux Atom</a>.</p>'
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

    # --- chronologie : mois du plus recent au plus ancien ; la toute derniere
    #     fiche est mise en avant (date en evidence, trois lignes completes)
    sections = []
    first = True
    for ym in sorted(by_month, reverse=True):
        mods = by_month[ym]
        cards = []
        for m in mods:
            cards.append(entry_card(m, featured=first))
            first = False
        sections.append(
            f'<section class="month" id="m-{ym}" data-month="{ym}" '
            f'aria-labelledby="h-{ym}">'
            f'<h2 class="month__head" id="h-{ym}">'
            f'<span class="month__name">{fr_month(ym)}</span>'
            f'<span class="month__count">{plural(len(mods), "fiche")}</span>'
            f'</h2>'
            f'<div class="entries">{"".join(cards)}</div></section>')
    timeline = "\n".join(sections) or "<p>Aucune entrée pour le moment.</p>"


    # --- filtres par theme
    per_theme = {k: 0 for k in THEMES}
    for m in modules:
        per_theme[m["theme"]] += 1
    theme_btns = [f'<button type="button" class="theme-btn" data-theme="" data-label="Tous" '
                  f'aria-pressed="true">Tous <span class="n">{len(modules)}</span></button>']
    for k, lab in THEMES.items():
        if per_theme[k]:
            theme_btns.append(
                f'<button type="button" class="theme-btn t-{k}" data-theme="{k}" '
                f'data-label="{html.escape(lab, quote=True)}" aria-pressed="false">'
                f'<span class="dot" aria-hidden="true"></span>'
                f'{html.escape(lab)} <span class="n">{per_theme[k]}</span></button>')
    themes_block = ('<div class="themes needs-js" role="group" aria-label="Filtrer par thème">'
                    + "".join(theme_btns) + '</div>')

    # --- nuage de tags (replie), tries par frequence puis alphabetiquement
    _all = sorted(tag_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    ordered = [kv for kv in _all if kv[1] >= TAGS_MIN]
    head_tags = "".join(tag_chip(t, n) for t, n in ordered[:TAGS_VISIBLES])
    rest = ordered[TAGS_VISIBLES:]
    more = ""
    if rest:
        more = ('<details><summary>' + plural(len(rest), "autre mot-clé", "autres mots-clés")
                + '</summary><ul class="tags__list">'
                + "".join(tag_chip(t, n) for t, n in rest) + "</ul></details>")
    tags_block = (f'<details class="tagbox needs-js"><summary>Filtrer par mot-clé</summary>'
                  f'<section class="tags" aria-label="Mots-clés">'
                  f'<ul class="tags__list">{head_tags}</ul>{more}</section></details>'
                  ) if ordered else ""

    # --- index de recherche embarque : id -> {haystack replie, tags, theme}
    data = {module_id(m): {
        "h": fold(" ".join([m["short"], m["title"], " ".join(m["lines"].values()),
                            " ".join(m["tags"]).replace("-", " "),
                            " ".join(m["tags"]), m["category_full"],
                            THEMES[m["theme"]], m["excerpt"], m["date"], fr_short(m["date"])])),
        "g": m["tags"],
        "t": m["theme"],
    } for m in modules}

    last = modules[0]["date"] if modules else ""
    hero = build_hero(modules)
    frise = build_frise(modules) if modules else ""
    body = (
        '<main id="main">'
        f'{hero}'
        '<div class="page home__content" id="fiches">'
        '<h2 class="section-title">Les fiches</h2>'
        f'{frise}'

        '<div class="toolbar">'
        '<form class="search needs-js" role="search" action="index.html" method="get">'
        '<label class="sr-only" for="q">Rechercher une fiche</label>'
        f'<span class="search__field">{icon("search")}'
        '<input type="search" id="q" name="q" autocomplete="off" spellcheck="false" '
        'aria-describedby="q-hint" '
        'placeholder="Rechercher : NIS 2, CNIL, chiffrement, #cjue…">'
        '<kbd class="kbd" id="q-kbd" aria-hidden="true">/</kbd>'
        '<button type="button" class="search__clear" id="q-clear" hidden '
        'aria-label="Effacer la recherche">&times;</button>'
        '</span></form>'
        '<p class="search__opts needs-js">'
        '<label><input type="checkbox" id="ft"> Chercher aussi dans le texte intégral</label>'
        '<span class="hint" id="q-hint">Tapez <code>#mot-clé</code> pour filtrer, '
        '<code>/</code> pour revenir au champ.</span>'
        '</p>'
        '<p class="hint" id="ft-note" role="status" hidden></p>'
        f'{themes_block}'
        f'{tags_block}'
        '<noscript><p class="nojs">La recherche et les filtres par thème nécessitent JavaScript. '
        'Toutes les fiches restent consultables ci-dessous, du plus récent au plus ancien.</p></noscript>'
        '</div>'

        '<div class="status">'
        f'<span class="status__n" id="count" aria-live="polite">'
        f'{plural(len(modules), "fiche")}</span>'
        '<a class="status__reset" id="reset" href="index.html" hidden>Réinitialiser les filtres</a>'
        '</div>'
        '<p class="empty" id="empty" hidden>Aucune fiche ne correspond à '
        '<b id="empty-q"></b>.<br>Essayez un terme plus court, un autre thème, '
        'ou cochez la recherche dans le texte intégral.</p>'

        f'<div id="dv" class="timeline">{timeline}</div>'
        '</div></main>'
        f'{site_footer("", feed=True)}'
        '<script type="application/json" id="dv-data">'
        + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        + '</script>'
        f'<script>{SEARCH_JS}</script>')

    desc = ("Veille sur le droit du numérique : IA, cybersécurité, RGPD, DSA, jurisprudence. "
            "Une fiche par sujet, résumé en trois lignes, analyse et sources officielles.")
    return (head("Droit Vivant — veille juridique du numérique", "", desc, path="")
            + '<body class="home">' + topbar("", current="index", wide=True) + body + "</body></html>")

def frise_svg(modules):
    """Une marque par fiche, placee a sa date et coloree par theme : la cadence
    reelle de la veille, de la premiere a la derniere fiche."""
    days = sorted({m["date"] for m in modules})
    d0, d1 = date.fromisoformat(days[0]), date.fromisoformat(days[-1])
    span = max((d1 - d0).days, 1)
    per_day, marks = {}, []
    for i, m in enumerate(sorted(modules, key=lambda m: m["date"])):
        k = per_day.get(m["date"], 0)
        per_day[m["date"]] = k + 1
        x = 6 + 988 * (date.fromisoformat(m["date"]) - d0).days / span
        y2 = 40 - k * 12
        marks.append(f'<line class="t t-{m["theme"]}" style="stroke:var(--tc);--i:{i}" '
                     f'x1="{x:.1f}" x2="{x:.1f}" y1="{y2 - 10}" y2="{y2}"/>')
    return ('<svg viewBox="0 0 1000 46" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            '<line class="axis" x1="0" x2="1000" y1="45" y2="45"/>' + "".join(marks) + '</svg>')

HERO_SCREENS = [(91.4, 66.4), (90.0, 76.6), (88.0, 71.1), (80.1, 88.9), (74.6, 82.1), (64.4, 69.4), (45.7, 77.4), (87.8, 95.3), (54.5, 72.3), (83.7, 63.4), (74.9, 71.1), (97.6, 76.2), (65.6, 74.9), (67.5, 85.1)]  # ecrans de l'image, en % (releves sur hero.png)

def hero_media(prefix):
    """Image du heros (AVIF, WebP, JPEG) et calques d'ambiance. L'apercu flou
    (lqip.txt, ~150 octets) est inline : rien n'est demande a un tiers."""
    if not HERO.exists() or not (HERO / "hero-1672.jpg").exists():
        return ""
    lqip = read(HERO / "lqip.txt").strip() if (HERO / "lqip.txt").exists() else ""
    h = f"{prefix}assets/hero/hero"
    screens = "".join(f'<i class="screen" style="left:{x}%;top:{y}%;--d:{(i * .73) % 5:.2f}s;--t:{4 + i % 4}s"></i>'
                      for i, (x, y) in enumerate(HERO_SCREENS))
    style = f' style="--lqip:url({lqip})"' if lqip else ""
    return (f'<div class="hero__media"{style}><div class="hero__frame">'
            '<picture>'
            f'<source type="image/avif" srcset="{h}-960.avif 960w, {h}-1672.avif 1672w" sizes="100vw">'
            f'<source type="image/webp" srcset="{h}-960.webp 960w, {h}-1672.webp 1672w" sizes="100vw">'
            f'<img src="{h}-1672.jpg" srcset="{h}-960.jpg 960w, {h}-1672.jpg 1672w" sizes="100vw" '
            'width="1672" height="940" alt="" fetchpriority="high" decoding="async">'
            '</picture>'
            f'<span class="beam" aria-hidden="true"></span><span class="dust" aria-hidden="true"></span>{screens}'
            '</div></div>')

def count_sources(modules):
    """Nombre d'adresses distinctes citees dans les sections Sources des briefs."""
    urls = set()
    for m in modules:
        _, src = split_brief(read(m["_brief_path"]))
        urls.update(u.rstrip(".,;") for u in re.findall(r"https?://(?:[^\s()\]]|\([^\s()]*\))+", src))
    return len(urls)

def period_label(first, last):
    a, b = first["date"], last["date"]
    if a[:4] == b[:4]:
        return f"{fr_short(a).rsplit(' ', 1)[0]} – {fr_short(b)}"
    return f"{fr_short(a)} – {fr_short(b)}"

def build_hero(modules):
    if not modules:
        return '<section class="hero"><div class="hero__body"><h1 class="hero__title">Droit Vivant</h1></div></section>'
    last, first = modules[0], modules[-1]
    themes = [THEMES[k] for k in THEMES if k != THEME_DEFAUT and any(m["theme"] == k for m in modules)]
    theme_list = ", ".join(t if t.isupper() else t.lower() for t in themes)
    stats = (
        f'<li><b>{len(modules)}</b><span>fiches publiées</span></li>'
        f'<li><b>{period_label(first, last)}</b><span>période couverte</span></li>'
        f'<li><b>{len(themes)}</b><span>thèmes suivis : {html.escape(theme_list)}</span></li>'
        f'<li><b>{count_sources(modules)}</b><span>sources citées</span></li>')
    return (
        '<section class="hero grain" aria-labelledby="hero-title">'
        f'{hero_media("")}'
        '<div class="hero__body"><div class="hero__text">'
        f'<p class="pill"><span>Mis à jour le <time datetime="{last["date"]}">{fr_day(last["date"])} {last["date"][:4]}</time></span></p>'
        '<h1 class="hero__title" id="hero-title">Ce qui change dans le droit du numérique.</h1>'
        '<p class="lede">Une veille sur l’IA, la cybersécurité, les données personnelles, les '
        'plateformes et la jurisprudence. Chaque fiche dit ce qui s’est passé, qui est concerné '
        'et ce qui change, sources officielles à l’appui.</p>'
        '<p class="hero__cta"><a class="btn-pill btn-pill--main" href="#fiches">Lire les fiches</a>'
        f'<a class="btn-pill btn-pill--ghost" href="{ABOUT_PAGE}">Comment c’est fait</a></p>'
        '</div>'
        f'<ul class="stats" aria-label="La veille en chiffres">{stats}</ul>'
        '</div></section>')

def build_frise(modules):
    last, first = modules[0], modules[-1]
    months = sorted({m["date"][:7] for m in modules})
    present = [k for k in THEMES if any(m["theme"] == k for m in modules)]
    legend = "".join(f'<li class="t-{k}">{html.escape(THEMES[k])}</li>' for k in present)
    d0 = date.fromisoformat(first["date"])
    span = max((date.fromisoformat(last["date"]) - d0).days, 1)
    def left(ym):
        # premier jour du mois, ramene dans l'intervalle de la frise
        pos = max(0, (date.fromisoformat(ym + "-01") - d0).days) / span
        return min(pos, 1) * 100
    month_links = "".join(f'<a href="#m-{ym}" style="left:{left(ym):.1f}%">{MOIS[int(ym[5:7]) - 1]}</a>'
                          for ym in months)
    return ('<figure class="frise" aria-label="Chronologie des fiches">'
            f'{frise_svg(modules)}'
            f'<nav class="frise__months" aria-label="Aller à un mois">{month_links}</nav>'
            f'<ul class="frise__legend">{legend}</ul></figure>')

def build_404():
    body = ('<main id="main"><section class="hero hero--404 grain" aria-labelledby="hero-title">'
            f'{hero_media("/")}'
            '<div class="hero__body"><div class="hero__text">'
            '<p class="pill"><span>Erreur 404</span></p>'
            '<h1 class="hero__title" id="hero-title">Cette page n’existe pas.</h1>'
            '<p class="lede">L’adresse a peut-être changé, ou elle contient une faute de frappe. '
            'Toutes les fiches restent accessibles depuis l’accueil.</p>'
            '<p class="hero__cta"><a class="btn-pill btn-pill--main" href="/index.html">Revenir aux fiches</a></p>'
            '</div></div></section></main>')
    # Chemins absolus : GitHub Pages sert 404.html a n'importe quelle profondeur.
    return (head("Page introuvable — Droit Vivant", "/", "", path="404.html",
                 extra='<meta name="robots" content="noindex">')
            + '<body class="home">' + topbar("/", wide=True) + body + site_footer("/") + "</body></html>")

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
    (SITE / "assets" / "site.js").write_text(SITE_JS.strip() + "\n", encoding="utf-8")
    (SITE / "assets" / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    if FONTS.exists():
        shutil.copytree(FONTS, SITE / "assets" / "fonts")
    if OG_IMAGE.exists():
        shutil.copy(OG_IMAGE, SITE / "assets" / "og.jpg")
    if HERO.exists():
        (SITE / "assets" / "hero").mkdir(parents=True, exist_ok=True)
        for f in HERO.iterdir():
            if f.suffix in (".avif", ".webp", ".jpg"):   # l'original .png n'est pas publie
                shutil.copy(f, SITE / "assets" / "hero" / f.name)
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

    # Une fiche en double reste servie (URL stable) mais sort de l'accueil et du flux.
    listed = [x for x in modules if not x["doublon_de"]]
    by_id = {module_id(x): x for x in modules}
    pos = {module_id(x): k for k, x in enumerate(listed)}
    light, full, tag_counts = [], {}, {}
    for x in modules:
        if x["infographie"]:
            p = SITE / x["infographie"]
            p.write_text(reskin_infographie(read(p), "../../" + fiche_href(x)), encoding="utf-8")
        if x["brief"]:
            p = SITE / x["brief"]
            (p.parent / (p.stem + ".html")).write_text(
                render_md_page(read(p), f"Brief du {fr_short(x['date'])}", "../../",
                               path=x["brief"][:-3] + ".html", fiche="../../" + fiche_href(x),
                               raw_md_name=p.name,
                               raw_label="Version .md brute"), encoding="utf-8")
        if x["source"]:
            p = SITE / x["source"]
            (p.parent / (p.stem + ".html")).write_text(
                render_md_page(read(p), f"Source NotebookLM du {fr_short(x['date'])}", "../../",
                               path=x["source"][:-3] + ".html", fiche="../../" + fiche_href(x),
                               raw_md_name=p.name,
                               raw_label="Version .md brute (pour NotebookLM)"),
                encoding="utf-8")
        (SITE / fiche_href(x)).write_text(render_fiche(x, pos.get(module_id(x)), listed, by_id), encoding="utf-8")

        if x["doublon_de"]:
            continue
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

    (SITE / "index.html").write_text(build_index(listed, tag_counts), encoding="utf-8")
    (SITE / ABOUT_PAGE).write_text(build_about(), encoding="utf-8")
    (SITE / "feed.xml").write_text(build_feed(listed), encoding="utf-8")
    (SITE / "404.html").write_text(build_404(), encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    (SITE / "CNAME").write_text(CUSTOM_DOMAIN + "\n", encoding="utf-8")
    n_days = len({m["date"] for m in modules})
    print(f"{len(modules)} module(s) sur {n_days} jour(s) construits "
          f"({len(listed)} listes, {len(modules) - len(listed)} doublon(s)), "
          f"{len(tag_counts)} mot(s)-cle(s), {len(modules) - len(sans_resume)} resume(s).")

if __name__ == "__main__":
    main()
