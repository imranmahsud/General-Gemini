const fs = require('node:fs');
const path = require('node:path');
const DEST = path.join(process.env.USERPROFILE, '.dsh', 'skills');
const KEBAB = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

function splitFrontmatter(text) {
  const m = text.match(/^---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|$)/);
  return m ? m[1] : null;
}
function header(fm, key) {
  const lines = fm.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(new RegExp('^' + key + ':[ \\t]*(.*)$'));
    if (!m) continue;
    let v = m[1].trim();
    if (v === '' || /^[>|][+-]?$/.test(v)) {
      const parts = [];
      for (let j = i + 1; j < lines.length && !/^[A-Za-z0-9_-]+:/.test(lines[j]); j++) parts.push(lines[j].trim());
      v = parts.join(' ').trim();
    }
    return v.replace(/^"(.*)"$/s, '$1').replace(/^'(.*)'$/s, '$1');
  }
  return undefined;
}

let dirs = 0, valid = 0, modelInvocable = 0, userOnly = 0;
const problems = [];
let catalogChars = 0;
for (const e of fs.readdirSync(DEST, { withFileTypes: true })) {
  if (!e.isDirectory()) continue;
  dirs++;
  const md = path.join(DEST, e.name, 'SKILL.md');
  if (!fs.existsSync(md)) { problems.push(e.name + ': missing SKILL.md'); continue; }
  const text = fs.readFileSync(md, 'utf8');
  const fm = splitFrontmatter(text);
  if (!fm) { problems.push(e.name + ': no frontmatter'); continue; }
  const name = header(fm, 'name');
  const desc = header(fm, 'description');
  if (name !== e.name) problems.push(e.name + ': frontmatter name=' + name);
  if (!KEBAB.test(name || '') || name.length > 64) problems.push(e.name + ': invalid kebab name');
  if (!desc || !desc.trim()) problems.push(e.name + ': empty description');
  const dmi = (header(fm, 'disable-model-invocation') || '').toLowerCase();
  const userInvocable = (header(fm, 'user-invocable') || '').toLowerCase();
  if (['true', 'yes', 'on', '1'].includes(dmi)) userOnly++;
  else if (['false', 'no', 'off', '0'].includes(userInvocable)) { /* user-only too */ }
  else modelInvocable++;
  valid++;
  catalogChars += (name || '').length + Math.min((desc || '').length, 500) + 15;
}
console.log(JSON.stringify({
  installedDirs: dirs,
  validSkills: valid,
  modelInvocable,
  userInvocableOnly: userOnly,
  problems: problems.length,
  problemSample: problems.slice(0, 10),
  catalogChars: catalogChars,
  estCatalogTokens: Math.round(catalogChars / 3.6),
}, null, 1));
