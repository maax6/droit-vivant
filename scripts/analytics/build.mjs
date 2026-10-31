// Compile entry.js en assets/analytics/ (ESM découpé : le SDK PostHog reste
// dans un fichier à part, chargé seulement après consentement).
// Usage : node scripts/analytics/build.mjs <dossier node_modules contenant posthog-js et esbuild>
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
const modules = path.resolve(process.argv[2] ?? '');
const require = createRequire(path.join(modules, 'noop.js'));
const esbuild = require(require.resolve('esbuild', { paths: [modules, ...fs.readdirSync(path.join(modules, '.pnpm')).filter(d => d.startsWith('esbuild@')).map(d => path.join(modules, '.pnpm', d, 'node_modules'))] }));
const here = path.dirname(new URL(import.meta.url).pathname);
const out = path.join(here, '..', 'assets', 'analytics');
fs.rmSync(out, { recursive: true, force: true });
await esbuild.build({
  entryPoints: { analytics: path.join(here, 'entry.js') },
  bundle: true, splitting: true, format: 'esm', minify: true, target: 'es2020',
  outdir: out, entryNames: '[name]', chunkNames: 'chunk-[hash]', nodePaths: [modules], legalComments: 'none',
});
for (const f of fs.readdirSync(out)) console.log(f, fs.statSync(path.join(out, f)).size);
