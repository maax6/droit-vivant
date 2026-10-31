# PostHog sur Droit Vivant

`client.js` et `privacy.mjs` sont repris du portfolio (`cG9yZm9saW8K/src/analytics/`) :
mêmes filtres de confidentialité, même bandeau de consentement. Seule la clé de stockage
du choix change (`droit-vivant:analytics-consent:v1`). `entry.js` crée le bandeau et ne
s'active que sur `droit-vivant.maxzer.fr`.

Le bundle publié est versionné dans `scripts/assets/analytics/` (la CI n'a que Python).
Après une modification, le reconstruire avec les `node_modules` du portfolio :

    node scripts/analytics/build.mjs ~/github/cG9yZm9saW8K/node_modules

`analytics.js` (quelques Ko) est chargé sur chaque page ; le SDK PostHog est dans un
fichier séparé, téléchargé seulement après un choix positif.
