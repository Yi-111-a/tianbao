import { defineConfig, type Plugin } from 'vite';
import react from '@vitejs/plugin-react';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import yaml from 'js-yaml';

const here = path.dirname(fileURLToPath(import.meta.url));
const scenarioDir = path.resolve(here, '../scenarios/tianbao_751');
const assetsDir = path.join(scenarioDir, 'assets');
const IMAGE_EXT = new Set(['.webp', '.png', '.jpg', '.jpeg', '.svg']);
const MIME: Record<string, string> = {
  '.webp': 'image/webp',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
};

function walk(dir: string, out: string[] = []): string[] {
  if (!fs.existsSync(dir)) return out;
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) walk(full, out);
    else if (IMAGE_EXT.has(path.extname(name).toLowerCase())) out.push(full);
  }
  return out;
}

/**
 * Dev-only: lets mock mode load the art agent's generated images straight from
 * scenarios/tianbao_751/assets without the engine. Builds an id → url index from
 * assets.yaml (if present) plus the file layout (portrait/li_linfu.default.webp →
 * portrait.li_linfu.default). Never answers 404 for ids — the app asks the index first.
 */
function scenarioAssets(): Plugin {
  const buildIndex = () => {
    const index: Record<string, string> = {};
    for (const file of walk(assetsDir)) {
      if (fs.statSync(file).size < 64) continue;
      const rel = path.relative(assetsDir, file).split(path.sep).join('/');
      const url = `/mock-assets/file/${rel}`;
      const base = path.basename(rel).replace(/\.[^.]+$/, '');
      // portrait/li_linfu.default.webp → portrait.li_linfu.default; portrait/portrait.x.webp → portrait.x
      index[rel.replace(/\.[^.]+$/, '').split('/').join('.')] = url;
      if (base.includes('.')) index[base] = url;
    }
    const manifestFile = path.join(scenarioDir, 'assets.yaml');
    if (fs.existsSync(manifestFile)) {
      try {
        const manifest = yaml.load(fs.readFileSync(manifestFile, 'utf-8')) as {
          entries?: { id?: string; path?: string }[];
        };
        for (const entry of manifest?.entries ?? []) {
          if (!entry.id || !entry.path) continue;
          const full = path.resolve(scenarioDir, entry.path);
          if (!full.startsWith(scenarioDir) || !fs.existsSync(full)) continue;
          const rel = path.relative(assetsDir, full).split(path.sep).join('/');
          if (rel.startsWith('..')) continue;
          index[entry.id] = `/mock-assets/file/${rel}`;
        }
      } catch {
        /* malformed manifest: fall back to file layout only */
      }
    }
    return index;
  };
  return {
    name: 'tianbao-scenario-assets',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = decodeURIComponent((req.url ?? '').split('?')[0]);
        if (url === '/mock-assets/scenario.json') {
          const read = (name: string) => {
            const file = path.join(scenarioDir, name);
            if (!fs.existsSync(file)) return undefined;
            try {
              return yaml.load(fs.readFileSync(file, 'utf-8'));
            } catch {
              return undefined;
            }
          };
          const bundle = {
            scenario: read('scenario.yaml'),
            characters: read('characters.yaml'),
            regions: read('regions.yaml'),
            armies: read('armies.yaml'),
            factions: read('factions.yaml'),
            memorials: read('memorials.yaml'),
            events: read('events.yaml'),
          };
          res.setHeader('Content-Type', 'application/json; charset=utf-8');
          res.setHeader('Cache-Control', 'no-store');
          res.end(JSON.stringify(bundle));
          return;
        }
        if (url === '/mock-assets/index.json') {
          let map: unknown = null;
          const mapFile = path.join(scenarioDir, 'map.json');
          if (fs.existsSync(mapFile)) {
            try {
              map = JSON.parse(fs.readFileSync(mapFile, 'utf-8'));
            } catch {
              map = null;
            }
          }
          res.setHeader('Content-Type', 'application/json; charset=utf-8');
          res.setHeader('Cache-Control', 'no-store');
          res.end(JSON.stringify({ assets: buildIndex(), map }));
          return;
        }
        if (url.startsWith('/mock-assets/file/')) {
          const rel = url.slice('/mock-assets/file/'.length);
          const full = path.resolve(assetsDir, rel);
          if (!full.startsWith(assetsDir) || !fs.existsSync(full)) {
            res.statusCode = 404;
            res.end();
            return;
          }
          res.setHeader('Content-Type', MIME[path.extname(full).toLowerCase()] ?? 'application/octet-stream');
          fs.createReadStream(full).pipe(res);
          return;
        }
        next();
      });
    },
  };
}

export default defineConfig({
  plugins: [react(), scenarioAssets()],
  clearScreen: false,
  server: {
    port: 5173,
    strictPort: false,
    fs: { allow: [path.resolve(here, '..')] },
  },
  build: {
    target: 'es2021',
    chunkSizeWarningLimit: 1500,
    assetsInlineLimit: 0,
  },
});
