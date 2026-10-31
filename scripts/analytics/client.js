import { createAnalyticsController, publicUrl, readConsent, saveConsent } from './privacy.mjs';

let controller;
let currentRoot;
let currentPage;
let scrollDepth = 0;
let pageStarted = 0;
let startedFields = new Set();

function pageProperties() {
  return { $current_url: publicUrl(location.href), $pathname: location.pathname, $referrer: publicUrl(document.referrer), page: location.pathname };
}
function trackPage() {
  if (!controller) return;
  currentPage = location.pathname;
  scrollDepth = 0;
  pageStarted = Date.now();
  startedFields = new Set();
  controller.capture('$pageview', pageProperties());
}

function setup() {
  const root = document.querySelector('[data-site-analytics]');
  if (!root || root.dataset.ready) return;
  root.dataset.ready = 'true';
  currentRoot = root;
  const banner = root.querySelector('[data-consent-banner]');
  const dialog = root.querySelector('dialog');
  const stats = root.querySelector('[name=usage-analytics]');
  const replay = root.querySelector('[name=usage-replay]');
  const status = root.querySelector('[data-consent-status]');
  let storage;
  try { storage = localStorage; } catch { storage = null; }
  let saved = readConsent(storage);
  if (!controller) controller = createAnalyticsController({ token: root.dataset.token, host: root.dataset.host, origin: location.origin, loadSdk: async () => (await import('posthog-js')).default });
  const showChoices = () => {
    const choice = controller.getConsent();
    stats.checked = choice.analytics;
    replay.checked = choice.replay;
    dialog.showModal();
  };
  async function decide(choice) {
    const wasEnabled = controller.getConsent().analytics;
    saved = saveConsent(storage, choice);
    banner.hidden = true;
    dialog.close();
    status.textContent = saved.analytics || saved.replay ? 'Votre choix est enregistré. Vous pouvez le modifier à tout moment.' : 'Collecte désactivée. Votre choix est enregistré.';
    try {
      await controller.apply(saved);
      if (saved.analytics && !wasEnabled) trackPage();
    } catch {
      // A blocked SDK or network must never stop navigation or the contact form.
      status.textContent = 'Votre choix est enregistré.';
    }
  }
  root.querySelectorAll('[data-consent-open]').forEach(button => button.addEventListener('click', showChoices));
  root.querySelectorAll('[data-consent-all]').forEach(button => button.addEventListener('click', () => void decide({ analytics: true, replay: true })));
  root.querySelectorAll('[data-consent-none]').forEach(button => button.addEventListener('click', () => void decide({ analytics: false, replay: false })));
  root.querySelector('[data-consent-save]').addEventListener('click', () => void decide({ analytics: stats.checked, replay: replay.checked }));
  root.querySelector('[data-consent-close]').addEventListener('click', () => dialog.close());
  banner.hidden = saved !== null;
  if (saved) void controller.apply(saved).then(() => { if (currentPage !== location.pathname) trackPage(); }).catch(() => {});
}

function clickProperties(target) {
  const id = target.id || target.dataset.analyticsId || null;
  const values = { ...pageProperties(), control_id: id, control_tag: target.tagName.toLowerCase() };
  // Only fixed public identifiers; no textContent, input values or copied text.
  for (const name of ['storyStep', 'document', 'auditStep', 'auditScope', 'step']) if (target.dataset[name]) values[name] = target.dataset[name];
  if (target instanceof HTMLAnchorElement) {
    values.destination_url = publicUrl(target.href);
    values.link_kind = target.protocol === 'mailto:' ? 'email' : target.origin === location.origin ? 'internal' : 'external';
  }
  return values;
}

document.addEventListener('click', event => {
  const target = event.target instanceof Element ? event.target.closest('a, button, summary') : null;
  if (!target || target.closest('[data-site-analytics], [data-private], .ph-mask, .ph-no-capture, [data-analytics-private]')) return;
  controller?.capture('control_clicked', clickProperties(target));
});
document.addEventListener('focusin', event => {
  const input = event.target;
  if (!(input instanceof HTMLInputElement || input instanceof HTMLTextAreaElement) || !input.closest('#contact-form') || !['name', 'email', 'message'].includes(input.name) || startedFields.has(input.name)) return;
  startedFields.add(input.name);
  controller?.capture('contact_field_started', { ...pageProperties(), field: input.name });
});
document.addEventListener('submit', event => {
  if (event.target instanceof HTMLFormElement && event.target.id === 'contact-form') controller?.capture('contact_submit_attempted', pageProperties());
}, true);
document.addEventListener('contact:result', event => {
  if (event.detail?.outcome === 'success' || event.detail?.outcome === 'error') controller?.capture('contact_submit_result', { ...pageProperties(), outcome: event.detail.outcome });
});
window.addEventListener('scroll', () => {
  const available = document.documentElement.scrollHeight - innerHeight;
  const depth = available <= 0 ? 100 : Math.min(100, Math.round(scrollY / available * 100));
  for (const threshold of [25, 50, 75, 100]) if (depth >= threshold && scrollDepth < threshold) controller?.capture('scroll_depth', { ...pageProperties(), percent: threshold });
  scrollDepth = Math.max(scrollDepth, depth);
}, { passive: true });
window.addEventListener('pagehide', () => controller?.capture('$pageleave', { ...pageProperties(), duration_seconds: Math.round((Date.now() - pageStarted) / 1000), max_scroll_percent: scrollDepth }));
window.addEventListener('storage', event => {
  if (event.key === 'droit-vivant:analytics-consent:v1') {
    let consent;
    try { consent = readConsent(localStorage); } catch { consent = null; }
    void controller?.apply(consent || { analytics: false, replay: false });
    if (currentRoot) currentRoot.querySelector('[data-consent-banner]').hidden = consent !== null;
  }
});
document.addEventListener('astro:page-load', () => { setup(); if (currentPage !== location.pathname) trackPage(); });
setup();
