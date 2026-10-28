---
name: ai-patterns-audit
description: Audite une interface (HTML, CSS, JS, gabarits, textes d'interface) contre les marqueurs actuels de « design généré par IA » et les corrige. Rafraîchit d'abord la liste des marqueurs par une recherche web datée du mois en cours. À lancer après toute création ou modification de front-end, ou quand l'utilisateur demande « vérifie les patterns IA », « est-ce que ça fait généré », « de-slop ».
---

# Audit des marqueurs de design généré par IA

Objectif : qu'aucun choix visible ne soit un défaut que personne n'a choisi. Un marqueur est un indice
de choix par défaut, pas une preuve qu'une IA a produit la page. Ce qui compte, c'est l'accumulation.

## 1. Rafraîchir la liste des marqueurs (à chaque lancement)

1. Lis `references/patterns.md` et sa date de mise à jour.
2. Lance 2 ou 3 recherches web en mode « standard », datées du mois et de l'année en cours, par exemple :
   - `AI generated website design tells <mois> <année>`
   - `AI slop UI patterns to avoid <année>`
   - `AI writing tells copywriting <année>`
3. Ajoute à `references/patterns.md` les marqueurs nouveaux ou en hausse, avec leur source (URL) et la date.
   Ne recopie pas un marqueur déjà présent. Si une source est un vendeur d'outil, note-le.
4. Si la recherche web est indisponible (réseau filtré), dis-le et continue avec la liste existante.

## 2. Scanner automatiquement

Lance le scanner mécanique sur ce qui a changé (ou sur le site construit) :

```bash
python3 .claude/skills/ai-patterns-audit/scan.py            # fichiers front modifiés (git)
python3 .claude/skills/ai-patterns-audit/scan.py site/      # tout le site construit
```

Le scanner repère ce qui se détecte par motif (police par défaut, dégradés décoratifs, capitales espacées,
séparateurs « · », flèches « → », fondus à l'apparition, chiffres ronds, tournures « pas X mais Y »…).
Ses résultats sont des pistes, pas des verdicts.

## 3. Audit visuel (ce qu'un motif ne voit pas)

Prends des captures (Playwright) de l'accueil et d'une page de contenu, en sombre et en clair, à 360 et
1440 px, et passe la grille de `references/patterns.md`. Cherche en priorité :
- un titre qui ne se lit pas tel quel sans mise en forme (copier-coller, aperçu de partage) ;
- un mot isolé en italique, en gras ou en couleur dans un titre ;
- des effets « partout » (lueurs, dégradés, ombres, survol qui soulève chaque carte, fondus à chaque bloc) ;
- des chiffres non sourcés ou ronds, des libellés génériques, des boutons de même poids ;
- une structure en cartes identiques pour des contenus qui n'ont pas la même importance.

## 4. Corriger, puis prouver

1. Classe les constats : bloquant (trompe ou gêne la lecture), majeur (marqueur évident), mineur.
2. Corrige les bloquants et les majeurs à la source (pour droit-vivant : `scripts/build_index.py`),
   en respectant les règles du projet (pas de ressource tierce, AA, reduced-motion, rien dans `archive/`).
3. Ce que l'utilisateur a explicitement demandé reste, même si c'est un marqueur : signale-le sans le retirer.
4. Reconstruis, relance le scanner, refais une capture, vérifie les contrastes.
5. Marque l'audit comme fait pour que le hook ne se redéclenche pas sur le même état :
   ```bash
   python3 .claude/hooks/ai_patterns_gate.py --mark
   ```

## 5. Rapport

En français, court : marqueurs corrigés, marqueurs gardés et pourquoi, nouveaux marqueurs ajoutés à la
liste (avec leurs sources en liens).
