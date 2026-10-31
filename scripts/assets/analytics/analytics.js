var t="phc_wmacfL9zwEYhSbKtBMjwjrMf75vAdW52LuhEsQXBPLyR",n="https://eu.i.posthog.com",s="droit-vivant.maxzer.fr",a=`
<button class="privacy-link" type="button" data-consent-open>Confidentialit\xE9</button>
<section class="consent-banner" data-consent-banner aria-labelledby="consent-banner-title" hidden>
  <button class="consent-dismiss" type="button" data-consent-none aria-label="Fermer sans accepter" title="Fermer sans accepter"><span aria-hidden="true">\xD7</span></button>
  <div class="consent-copy"><h2 id="consent-banner-title">Un mot sur la confidentialit\xE9</h2><p>Avec votre accord, PostHog mesure la navigation et permet de revoir les interactions. Les saisies sont masqu\xE9es.</p><p class="consent-hint">Fermer ce bandeau refuse la collecte. Votre choix reste modifiable.</p></div>
  <div class="consent-footer"><a href="/mentions-legales.html#mesure-audience">En savoir plus</a><div class="consent-actions"><button type="button" data-consent-open>Choisir</button><button type="button" data-consent-all>Accepter</button></div></div>
</section>
<dialog aria-labelledby="consent-dialog-title">
  <header><h2 id="consent-dialog-title">Vos pr\xE9f\xE9rences de confidentialit\xE9</h2><button type="button" data-consent-close aria-label="Fermer les pr\xE9f\xE9rences">\xD7</button></header>
  <p>Le site fonctionne avec ou sans collecte. Vous pouvez modifier votre choix \xE0 tout moment.</p>
  <label><input type="checkbox" name="usage-analytics" /><span><strong>Statistiques de navigation</strong><small>Pages consult\xE9es, clics, d\xE9filement, performances et erreurs techniques masqu\xE9es.</small></span></label>
  <label><input type="checkbox" name="usage-replay" /><span><strong>Enregistrement des sessions</strong><small>Relecture de la navigation et des interactions. Les champs saisis sont masqu\xE9s.</small></span></label>
  <p><a href="/mentions-legales.html#mesure-audience">Comment les donn\xE9es sont utilis\xE9es</a></p>
  <div class="consent-actions"><button type="button" data-consent-save>Enregistrer mon choix</button><button type="button" data-consent-all>Tout accepter</button></div>
</dialog>
<p class="consent-status" data-consent-status role="status" aria-live="polite"></p>`;if(location.hostname===s&&!document.querySelector("[data-site-analytics]")){let e=document.createElement("div");e.className="site-analytics",e.dataset.siteAnalytics="",e.dataset.analyticsPrivate="",e.dataset.token=t,e.dataset.host=n,e.innerHTML=a,(document.querySelector(".sitefoot .inner")||document.body).append(e),import("./chunk-7S4B6WS4.js")}
