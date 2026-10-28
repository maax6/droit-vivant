#!/usr/bin/env python3
"""Scanner mécanique des marqueurs de design généré par IA (stdlib seule).

Usage :
  scan.py            fichiers front modifiés ou non suivis (git), hors archive/ et site/
  scan.py CHEMIN...  fichiers ou dossiers donnés (ex. site/)

Les résultats sont des pistes à vérifier à l'œil, pas des verdicts.
"""
import re, subprocess, sys
from pathlib import Path

EXTS = {".html", ".css", ".js", ".py", ".md", ".jsx", ".tsx", ".vue", ".svelte"}
SKIP = ("archive/", "site/archive/", ".claude/", "node_modules/")

# (identifiant, gravité, regex, explication)
RULES = [
    ("police-inter", "majeur", r"font-family[^;{}]*\bInter\b|[\"']Inter[\"']",
     "Inter partout est le marqueur typographique le plus cité."),
    ("degrade-violet", "majeur", r"(indigo|violet|purple)-[3-7]00|#(6366f1|8b5cf6|7c3aed|a855f7|4f46e5)\b",
     "Violet/indigo par défaut (démos Tailwind)."),
    ("degrade-135", "mineur", r"linear-gradient\(\s*135deg",
     "Dégradé à 135°, réflexe de gabarit."),
    ("lueur", "mineur", r"box-shadow:[^;]*0 0 \d+px[^;]*rgba?\([^)]*\)|text-shadow:[^;]*0 0 \d+px",
     "Lueur décorative (glow)."),
    ("glass", "mineur", r"backdrop-filter:\s*blur\(\s*(1[6-9]|[2-9]\d)px",
     "Glassmorphism appuyé."),
    ("capitales-espacees", "mineur", r"text-transform:\s*uppercase[^}]*letter-spacing|letter-spacing:[^;]*;[^}]*text-transform:\s*uppercase",
     "Étiquettes en capitales espacées."),
    ("fondu-apparition", "majeur", r"fade-?up|fadeInUp|data-aos|\.reveal\b|translateY\(\s*(?:[89]|[1-9]\d)px\s*\)[^}]*opacity:\s*0\b|opacity:\s*0\b[^}]*translateY\(\s*(?:[89]|[1-9]\d)px",
     "Fondu + montée à l'apparition."),
    ("survol-souleve", "mineur", r":hover\s*\{[^}]*translateY\(\s*-\d",
     "Survol qui soulève l'élément."),
    ("separateur-point", "mineur", r">[^<>{}]*\s·\s[^<>{}]*<|[\"'][^\"'\n]*\s·\s[^\"'\n]*[\"']",
     "Séparateur « · » entre métadonnées."),
    ("fleche-lien", "mineur", r"(→|&rarr;)\s*</a>|(→|&rarr;)\s*</button>",
     "« → » ajouté au texte d'un lien ou bouton."),
    ("pas-x-mais-y", "majeur", r"(?i)\bce n['’]est pas [^.<]{1,60}, c['’]est\b|\bit['’]s not [^.<]{1,60}, it['’]s\b|\bpas seulement [^.<]{1,60}, mais\b",
     "Tournure « pas X, c'est Y »."),
    ("chiffre-rond", "majeur", r"\b\d{1,3}(?:[ .,]000)+\s*\+|\b100\s?%\s*(de\s)?(satisf|garanti)|\b10k\+",
     "Chiffre rond ou invérifiable."),
    ("verbe-creux", "mineur", r"(?i)\b(révolutionn\w+|boost\w*|empower\w*|leverag\w*|unlock\w*|supercharg\w*|game[- ]?changer)\b",
     "Verbe ou formule creuse."),
    ("politesse", "mineur", r"(?i)bienvenue sur (notre|le site)|ne cherchez plus|look no further|say goodbye to",
     "Ouverture de politesse ou cliché publicitaire."),
    ("placeholder", "bloquant", r"(?i)\b(lorem ipsum|john doe|jane doe|acme inc)\b",
     "Contenu de remplissage."),
    ("numerotation", "mineur", r">\s*0[1-9]\s*<|content:\s*[\"']0[1-9]",
     "Numéros 01/02/03 : vérifier que c'est une vraie séquence."),
    ("emoji-titre", "mineur", r"<h[1-3][^>]*>[^<]*[\U0001F300-\U0001FAFF]",
     "Emoji dans un titre."),
]


def changed_files():
    try:
        out = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"],
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return []
    files = []
    for line in out.splitlines():
        path = line[3:].split(" -> ")[-1].strip('"')
        if Path(path).suffix in EXTS and not path.startswith(SKIP) and Path(path).is_file():
            files.append(Path(path))
    return files


def expand(args):
    for a in args:
        p = Path(a)
        if p.is_dir():
            for f in sorted(p.rglob("*")):
                rel = f.as_posix()
                if f.is_file() and f.suffix in EXTS and not any(s in rel for s in ("/archive/", "node_modules/")):
                    yield f
        elif p.is_file():
            yield p


def main():
    files = list(expand(sys.argv[1:])) if sys.argv[1:] else changed_files()
    if not files:
        print("Aucun fichier front à scanner.")
        return 0
    hits = {}
    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        if f.suffix == ".html":
            # donnees embarquees (JSON de recherche, scripts) : pas du texte affiche
            text = re.sub(r"<script\b[^>]*>.*?</script>",
                          lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S | re.I)
        for rid, sev, rx, why in RULES:
            for m in re.finditer(rx, text):
                line = text.count("\n", 0, m.start()) + 1
                hits.setdefault((sev, rid, why), []).append(f"{f}:{line}")
    order = {"bloquant": 0, "majeur": 1, "mineur": 2}
    print(f"{len(files)} fichier(s) scanné(s).")
    if not hits:
        print("Aucun marqueur mécanique détecté. Faire quand même l'audit visuel.")
        return 0
    for (sev, rid, why), locs in sorted(hits.items(), key=lambda kv: (order[kv[0][0]], kv[0][1])):
        print(f"\n[{sev}] {rid} ({len(locs)}) : {why}")
        for loc in locs[:5]:
            print(f"  {loc}")
        if len(locs) > 5:
            print(f"  … et {len(locs) - 5} autre(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
