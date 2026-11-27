// Demote skills that came from the bulk upstream families, matched by their ORIGINAL source folder.
const fs = require('node:fs');
const path = require('node:path');

const DEST = path.join(process.env.USERPROFILE, '.dsh', 'skills');
const manifest = JSON.parse(fs.readFileSync(path.join(DEST, '.ingest-manifest.json'), 'utf8'));
const FAMILIES = ['ecc-', 'trade-', 'gsd-', 'cli-anything-', 'mp-', 'sp-'];

function sourceFamily(srcDir) {
  const parts = srcDir.split(/[\\/]/);
  const idx = parts.lastIndexOf('skills');
  if (idx < 0) return '';
  let folder = parts[idx + 1] || '';
  if (folder === 'everything-claude-code' || folder === 'superpowers' || folder === 'mattpocock-skills' || folder === 'gstack' || folder === 'day-trader-skill') {
    // bundled collections: use the skill's own folder name (two levels down)
    const inner = parts[parts.length - 2];
    return /^(ecc|sp|mp|trader|gstack)-/.test(inner) ? inner : inner;
  }
  return folder;
}

function patch(mdPath) {
  let text = fs.readFileSync(mdPath, 'utf8');
  if (text.charCodeAt(0) === 0xfeff) text = text.slice(1);
  const m = text.match(/^---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|$)/);
  if (!m) return 'no-frontmatter';
  if (/^disable-model-invocation:/m.test(m[1])) return 'already';
  const fmLines = m[1].split(/\r?\n/);
  fmLines.push('disable-model-invocation: true');
  fs.writeFileSync(mdPath, `---\n${fmLines.join('\n')}\n---\n${text.slice(m[0].length)}`, 'utf8');
  return 'patched';
}

// Container children (superpowers/gstack/...) are stored under their own frontmatter name, so the
// source folder is the only reliable family signal for those.
const byFamily = {};
const result = { patched: 0, already: 0, failed: 0, perFamily: {} };
for (const s of manifest.skills) {
  const folder = sourceFamily(s.srcDir);
  const family = FAMILIES.find(f => folder.startsWith(f));
  if (!family) continue;
  byFamily[family] = (byFamily[family] || 0) + 1;
  const md = path.join(DEST, s.name, 'SKILL.md');
  if (!fs.existsSync(md)) { result.failed++; continue; }
  const r = patch(md);
  if (r === 'patched') result.patched++;
  else if (r === 'already') result.already++;
  else result.failed++;
}
result.perFamily = byFamily;
console.log(JSON.stringify(result, null, 1));
