#!/usr/bin/env python3
"""Hook Stop : si des fichiers front ont changé depuis le dernier audit, demande
à Claude de lancer le skill ai-patterns-audit avant de rendre la main.

- Lu par Claude Code à la fin de chaque tour (événement Stop, JSON sur stdin).
- Ne bloque qu'une fois par tour (stop_hook_active) : pas de boucle.
- `--mark` enregistre l'état courant comme audité (appelé par le skill).
L'empreinte est stockée dans .claude/.ai-audit-stamp (non versionné).
"""
import hashlib, json, os, subprocess, sys
from pathlib import Path

# Racine du projet courant : fonctionne aussi copie dans ~/.claude/hooks/ (usage global).
ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()
STAMP = ROOT / ".claude" / ".ai-audit-stamp"
FRONT = {".html", ".css", ".js", ".jsx", ".tsx", ".vue", ".svelte"}
FRONT_FILES = {"scripts/build_index.py"}       # generateur du site droit-vivant (sans effet ailleurs)
SKIP = ("archive/", "site/", ".claude/", "node_modules/")


def front_changes():
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=all"],
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return []
    files = []
    for line in out.splitlines():
        path = line[3:].split(" -> ")[-1].strip('"')
        if path.startswith(SKIP):
            continue
        if Path(path).suffix in FRONT or path in FRONT_FILES:
            files.append(path)
    return sorted(files)


def digest(files):
    h = hashlib.sha256()
    for f in files:
        h.update(f.encode())
        p = ROOT / f
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()


def main():
    files = front_changes()
    if "--mark" in sys.argv:
        STAMP.parent.mkdir(exist_ok=True)
        STAMP.write_text(digest(files))
        print("Audit enregistré pour l'état courant.")
        return 0
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}
    if event.get("stop_hook_active") or not files:
        return 0
    current = digest(files)
    if STAMP.exists() and STAMP.read_text().strip() == current:
        return 0
    print(json.dumps({
        "decision": "block",
        "reason": ("Des fichiers front ont été créés ou modifiés (" + ", ".join(files[:6])
                   + ("…" if len(files) > 6 else "") + "). Lance le skill ai-patterns-audit "
                   "(Skill tool, skill « ai-patterns-audit ») avant de rendre la main, puis "
                   "termine par `python3 .claude/hooks/ai_patterns_gate.py --mark`."),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
