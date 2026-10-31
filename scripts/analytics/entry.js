// Point d'entrée PostHog de Droit Vivant. client.js et privacy.mjs viennent du
// portfolio (src/analytics/) : mêmes filtres, même consentement. Le SDK n'est
// téléchargé qu'après un choix positif du visiteur.
// Reconstruire assets/analytics/ : voir scripts/analytics/README.md.

const TOKEN = 'phc_wmacfL9zwEYhSbKtBMjwjrMf75vAdW52LuhEsQXBPLyR';
const HOST = 'https://eu.i.posthog.com';
const SITE_HOST = 'droit-vivant.maxzer.fr';

const MARKUP = `
<button class="privacy-link" type="button" data-consent-open>Confidentialité</button>
<section class="consent-banner" data-consent-banner aria-labelledby="consent-banner-title" hidden>
  <button class="consent-dismiss" type="button" data-consent-none aria-label="Fermer sans accepter" title="Fermer sans accepter"><span aria-hidden="true">×</span></button>
  <div class="consent-copy"><h2 id="consent-banner-title">Un mot sur la confidentialité</h2><p>Avec votre accord, PostHog mesure la navigation et permet de revoir les interactions. Les saisies sont masquées.</p><p class="consent-hint">Fermer ce bandeau refuse la collecte. Votre choix reste modifiable.</p></div>
  <div class="consent-footer"><a href="/mentions-legales.html#mesure-audience">En savoir plus</a><div class="consent-actions"><button type="button" data-consent-open>Choisir</button><button type="button" data-consent-all>Accepter</button></div></div>
</section>
<dialog aria-labelledby="consent-dialog-title">
  <header><h2 id="consent-dialog-title">Vos préférences de confidentialité</h2><button type="button" data-consent-close aria-label="Fermer les préférences">×</button></header>
  <p>Le site fonctionne avec ou sans collecte. Vous pouvez modifier votre choix à tout moment.</p>
  <label><input type="checkbox" name="usage-analytics" /><span><strong>Statistiques de navigation</strong><small>Pages consultées, clics, défilement, performances et erreurs techniques masquées.</small></span></label>
  <label><input type="checkbox" name="usage-replay" /><span><strong>Enregistrement des sessions</strong><small>Relecture de la navigation et des interactions. Les champs saisis sont masqués.</small></span></label>
  <p><a href="/mentions-legales.html#mesure-audience">Comment les données sont utilisées</a></p>
  <div class="consent-actions"><button type="button" data-consent-save>Enregistrer mon choix</button><button type="button" data-consent-all>Tout accepter</button></div>
</dialog>
<p class="consent-status" data-consent-status role="status" aria-live="polite"></p>`;

if (location.hostname === SITE_HOST && !document.querySelector('[data-site-analytics]')) {
  const root = document.createElement('div');
  root.className = 'site-analytics';
  root.dataset.siteAnalytics = '';
  root.dataset.analyticsPrivate = '';
  root.dataset.token = TOKEN;
  root.dataset.host = HOST;
  root.innerHTML = MARKUP;
  (document.querySelector('.sitefoot .inner') || document.body).append(root);
  import('./client.js');
}
