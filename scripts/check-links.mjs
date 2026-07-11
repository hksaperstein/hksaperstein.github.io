// Checks that every root-relative href/src in dist/**/*.html resolves to a file in dist/.
import { readdirSync, readFileSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';

const DIST = 'dist';

function htmlFiles(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) return htmlFiles(path);
    return entry.name.endsWith('.html') ? [path] : [];
  });
}

const failures = [];
for (const file of htmlFiles(DIST)) {
  const html = readFileSync(file, 'utf8');
  for (const match of html.matchAll(/(?:href|src)="(\/[^"#?]*)/g)) {
    const url = decodeURIComponent(match[1]);
    if (url === '/') continue;
    const clean = url.replace(/\/$/, '');
    const candidates = [join(DIST, clean), join(DIST, clean, 'index.html')];
    if (!candidates.some((c) => existsSync(c) && statSync(c).isFile())) {
      failures.push(`${file}: ${url}`);
    }
  }
}

if (failures.length) {
  console.error(`BROKEN INTERNAL LINKS (${failures.length}):`);
  for (const failure of failures) console.error('  ' + failure);
  process.exit(1);
}
console.log('all internal links resolve');
