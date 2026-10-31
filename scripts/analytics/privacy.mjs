export const CONSENT_KEY = 'droit-vivant:analytics-consent:v1';
export const CONSENT_MAX_AGE = 180 * 24 * 60 * 60 * 1000;

export function readConsent(storage, now = Date.now()) {
  try {
    const saved = JSON.parse(storage.getItem(CONSENT_KEY));
    if (!saved || saved.version !== 1 || typeof saved.analytics !== 'boolean' || typeof saved.replay !== 'boolean' || !Number.isFinite(saved.date) || saved.date > now || now - saved.date >= CONSENT_MAX_AGE) return null;
    return saved;
  } catch { return null; }
}

export function saveConsent(storage, consent, now = Date.now()) {
  const saved = { version: 1, analytics: consent.analytics === true, replay: consent.replay === true, date: now };
  try { storage.setItem(CONSENT_KEY, JSON.stringify(saved)); } catch { /* A blocked store never implies consent. */ }
  return saved;
}

export function publicUrl(value, origin = 'https://maxzer.fr') {
  if (typeof value !== 'string' || !value.trim()) return undefined;
  try {
    const url = new URL(value, origin);
    if (!['http:', 'https:'].includes(url.protocol)) return undefined;
    return `${url.origin}${url.pathname}`;
  } catch { return undefined; }
}

export function privacyOptions(consent, origin = 'https://maxzer.fr') {
  return {
    // All clicks are tracked explicitly; DOM text and form values are never event properties.
    autocapture: false,
    capture_dead_clicks: false,
    capture_pageview: false,
    capture_pageleave: false,
    capture_heatmaps: consent.analytics,
    capture_performance: consent.analytics ? { web_vitals: true } : false,
    capture_exceptions: consent.analytics ? {
      capture_unhandled_errors: true,
      capture_unhandled_rejections: true,
      capture_console_errors: false,
    } : false,
    error_tracking: { exception_steps: { enabled: false } },
    disable_session_recording: !consent.replay,
    enable_recording_console_log: false,
    person_profiles: 'never',
    persistence: 'localStorage',
    persistence_name: 'maxzer_usage',
    cross_subdomain_cookie: false,
    disable_capture_url_hashes: true,
    disable_surveys: true,
    disable_product_tours: true,
    disable_conversations: true,
    disable_web_experiments: true,
    session_recording: {
      maskAllInputs: true,
      maskInputFn: () => '[masqué]',
      maskTextSelector: '.ph-mask, [data-private]',
      blockSelector: '.ph-no-capture, [data-analytics-private]',
      recordHeaders: false,
      recordBody: false,
      captureCanvas: { recordCanvas: false },
      maskAttributeFn: (name, value, element) => {
        if (name === 'value' || element?.closest('[data-private], .ph-mask')) return '[masqué]';
        if (['href', 'src', 'action'].includes(name)) return publicUrl(value, origin) || '[masqué]';
        return value;
      },
      maskCapturedNetworkRequestFn: request => {
        const url = publicUrl(request.name, origin);
        if (!url || new URL(url).pathname === '/api/contact.php') return undefined;
        return { ...request, name: url, requestBody: undefined, responseBody: undefined, requestHeaders: undefined, responseHeaders: undefined };
      },
    },
  };
}

function privateException(exception, origin) {
  const type = ['Error', 'TypeError', 'ReferenceError', 'RangeError', 'SyntaxError', 'URIError', 'EvalError', 'AggregateError'].includes(exception?.type) ? exception.type : 'Error';
  const frames = (Array.isArray(exception?.stacktrace?.frames) ? exception.stacktrace.frames : []).flatMap(frame => {
    const filename = publicUrl(frame.filename || frame.abs_path, origin);
    if (!filename || new URL(filename).origin !== origin) return [];
    return [{ platform: 'web:javascript', filename,
      ...(Number.isInteger(frame.lineno) && frame.lineno >= 0 ? { lineno: frame.lineno } : {}),
      ...(Number.isInteger(frame.colno) && frame.colno >= 0 ? { colno: frame.colno } : {}),
    }];
  });
  return { type, value: '[masqué]',
    mechanism: { handled: exception?.mechanism?.handled === true, type: 'generic' },
    stacktrace: { type: 'raw', frames },
  };
}

export function filterEvent(event, consent, origin = 'https://maxzer.fr') {
  if (event.event === '$snapshot') return consent.replay ? event : null;
  if (!consent.analytics) return null;
  const properties = { ...event.properties, $geoip_disable: true };
  for (const key of Object.keys(properties)) {
    if (/^(name|email|message|password|value|\$set|\$set_once|\$initial_utm_|utm_)/i.test(key)) delete properties[key];
    else if (/(url|referrer|href)$/i.test(key) && typeof properties[key] === 'string') properties[key] = publicUrl(properties[key], origin);
  }
  if (event.event === '$exception') {
    // Error messages, source excerpts, variables and breadcrumbs can include contact values.
    const exceptions = (Array.isArray(properties.$exception_list) ? properties.$exception_list : []).map(exception => privateException(exception, origin));
    for (const key of Object.keys(properties)) if (key.startsWith('$exception_')) delete properties[key];
    properties.$exception_list = exceptions;
    properties.$exception_level = 'error';
  }
  return { ...event, properties };
}

// The async boundary is injectable so consent withdrawal during SDK loading can be tested.
export function createAnalyticsController({ token, host, origin, loadSdk, onReady = () => {} }) {
  let consent = { analytics: false, replay: false };
  let sdk;
  let pending;
  const allowed = () => consent.analytics || consent.replay;
  async function apply(next) {
    consent = { analytics: next.analytics === true, replay: next.replay === true };
    if (!allowed()) {
      if (sdk) { sdk.stopSessionRecording(); sdk.opt_out_capturing(); sdk.set_config({ disable_persistence: true }); }
      return;
    }
    if (!sdk) {
      pending ||= loadSdk().catch(error => { pending = undefined; throw error; });
      const provider = await pending;
      if (!allowed()) return;
      if (!sdk) {
        sdk = provider;
        sdk.init(token, {
          api_host: host,
          ui_host: host.includes('eu.') ? 'https://eu.posthog.com' : 'https://us.posthog.com',
          defaults: '2026-05-30',
          ...privacyOptions(consent, origin),
          before_send: event => filterEvent(event, consent, origin),
          loaded: () => { if (allowed()) onReady(); },
        });
      }
    }
    sdk.set_config({ ...privacyOptions(consent, origin), disable_persistence: false });
    sdk.opt_in_capturing({ captureEventName: false });
    if (consent.replay) sdk.startSessionRecording(); else sdk.stopSessionRecording();
  }
  return {
    apply,
    capture(name, properties = {}) { if (sdk && consent.analytics && !sdk.has_opted_out_capturing()) sdk.capture(name, properties); },
    getConsent: () => ({ ...consent }),
  };
}
