# Droit Vivant

Veille sur le droit contemporain (numérique, cyber, libertés, IA, jurisprudence FR/UE/CEDH), générée à la demande et publiée sur GitHub Pages.

- **Site** : https://maax6.github.io/droit-vivant/
- **Archive** : `archive/AAAA-MM-JJ/` — chaque module : infographie HTML, brief, source NotebookLM.
- **Résumés** : `scripts/data/resumes.json` — titre court, résumé en 3 lignes (`quoi`, `qui`, `change`) et thème (`IA`, `cyber`, `RGPD`, `DSA`, `jurisprudence`, `autres`) de chaque module, clé = `AAAA-MM-JJ` ou `AAAA-MM-JJ-slug`. Un module sans entrée s'affiche quand même (titre d'origine, analyse dépliée). Le fichier vit sous `scripts/` pour que la CI se déclenche quand on le modifie.
- **Build** : `python3 scripts/build_index.py` génère `site/` (accueil, une fiche par module dans `fiches/`, page « Comment c'est fait », index de recherche, flux Atom). Python standard uniquement.
- **CI** : `.github/workflows/deploy.yml` reconstruit l'index (`scripts/build_index.py`) et déploie Pages à chaque push.

Contenu pédagogique — ne constitue pas un conseil juridique.
