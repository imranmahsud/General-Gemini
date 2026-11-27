// Ingest General-Gemini skills into the DSH user skill root.
const fs = require('node:fs');
const path = require('node:path');

const SRC = path.join(process.env.USERPROFILE, '.dsh', 'vendor', 'general-gemini');
const DEST = path.join(process.env.USERPROFILE, '.dsh', 'skills');
const KEBAB = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

const log = { copied: [], renamed: [], synthesized: [], skippedDup: [], skippedNoSkill: [], errors: [] };

function readUtf8(p) {
  let t = fs.readFileSync(p, 'utf8');
  if (t.charCodeAt(0) === 0xfeff) t = t.slice(1);
  return t;
}

function splitFrontmatter(text) {
  const m = text.match(/^---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|$)/);
  if (!m) return null;
  return { fm: m[1], body: text.slice(m[0].length), raw: m[0] };
}

// Minimal YAML frontmatter reader: top-level scalars plus folded/literal block scalars.
function parseHeaders(fm) {
  const out = {};
  const lines = fm.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/^([A-Za-z0-9_-]+):[ \t]*(.*)$/);
    if (!m) continue;
    const key = m[1];
    let val = m[2].trim();
    if (val === '' || /^[>|][+-]?$/.test(val)) {
      const parts = [];
      let j = i + 1;
      for (; j < lines.length; j++) {
        if (/^[A-Za-z0-9_-]+:/.test(lines[j])) break;
        parts.push(lines[j].trim());
      }
      val = parts.join(' ').trim();
      i = j - 1;
    }
    val = val.replace(/^"(.*)"$/s, '$1').replace(/^'(.*)'$/s, '$1');
    out[key] = val;
  }
  return out;
}

function normalizeName(raw) {
  let n = String(raw || '').toLowerCase().trim();
  n = n.replace(/^["']|["']$/g, '');
  n = n.replace(/[^a-z0-9]+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
  if (n.length > 64) {
    n = n.slice(0, 64).replace(/-+$/, '');
  }
  return n;
}

function validName(n) {
  return !!n && n.length <= 64 && KEBAB.test(n);
}

function firstParagraph(body) {
  const lines = body.split(/\r?\n/);
  const chunks = [];
  let started = false;
  for (const raw of lines) {
    const line = raw.trim();
    if (!line) {
      if (started) break;
      continue;
    }
    if (!started) {
      if (/^[#`>|<]/.test(line) || /^[-*+]\s/.test(line)) continue; // skip structural-first lines
      started = true;
    }
    chunks.push(line);
    if (chunks.join(' ').length > 180) break;
  }
  return chunks.join(' ').replace(/\s+/g, ' ').trim();
}

function ensureFrontmatter(text, name, descFallback) {
  const parsed = splitFrontmatter(text);
  if (!parsed) {
    const body = text.replace(/^\s+/, '');
    const detail = firstParagraph(body) || 'Imported skill.';
    return { text: `---\nname: ${name}\ndescription: ${detail.slice(0, 300)}\n---\n\n${body}`, synthesized: true };
  }
  const headers = parseHeaders(parsed.fm);
  let fmLines = parsed.fm.split(/\r?\n/);
  let changed = false;

  // Resolve description: keep existing, else synthesize from body.
  const hasDesc = headers.description && headers.description.trim().length > 0;
  const descValue = hasDesc ? headers.description : (descFallback || 'Imported skill.').slice(0, 300);

  // Rewrite the name line when it does not carry the normalized identity.
  const nameLineIdx = fmLines.findIndex(l => /^name:/.test(l));
  if (nameLineIdx >= 0) {
    if (fmLines[nameLineIdx].replace(/^name:[ \t]*/, '').trim().replace(/^["']|["']$/g, '') !== name) {
      fmLines[nameLineIdx] = `name: ${name}`;
      changed = true;
    }
  } else {
    fmLines.unshift(`name: ${name}`);
    changed = true;
  }

  if (!hasDesc) {
    // Replace a multi-line description block when present, else append.
    let descIdx = fmLines.findIndex(l => /^description:/.test(l));
    if (descIdx >= 0) {
      let end = descIdx + 1;
      while (end < fmLines.length && !/^[A-Za-z0-9_-]+:/.test(fmLines[end])) end++;
      fmLines.splice(descIdx, end - descIdx, `description: ${descValue}`);
    } else {
      fmLines.push(`description: ${descValue}`);
    }
    changed = true;
  }

  if (!changed) return { text, synthesized: false };
  return { text: `---\n${fmLines.join('\n')}\n---\n${parsed.body}`, synthesized: false, changed: true };
}

function collect() {
  const candidates = [];
  const skillsRoot = path.join(SRC, 'skills');
  const containers = [];

  for (const e of fs.readdirSync(skillsRoot, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    if (!e.isDirectory() || e.name === 'node_modules') continue;
    const dir = path.join(skillsRoot, e.name);
    if (fs.existsSync(path.join(dir, 'SKILL.md'))) {
      candidates.push({ srcDir: dir, origin: 'skills', priority: 1 });
    } else {
      containers.push({ name: e.name, dir });
    }
  }

  // Container folders without their own SKILL.md: take skills one and two levels down.
  for (const c of containers) {
    let found = 0;
    for (const child of fs.readdirSync(c.dir, { withFileTypes: true })) {
      if (!child.isDirectory() || child.name.startsWith('.') || child.name === 'node_modules') continue;
      const childDir = path.join(c.dir, child.name);
      if (fs.existsSync(path.join(childDir, 'SKILL.md'))) {
        candidates.push({ srcDir: childDir, origin: `bundle:${c.name}`, priority: 2 });
        found++;
        continue;
      }
      for (const grand of fs.readdirSync(childDir, { withFileTypes: true })) {
        if (!grand.isDirectory() || grand.name.startsWith('.') || grand.name === 'node_modules') continue;
        const grandDir = path.join(childDir, grand.name);
        if (fs.existsSync(path.join(grandDir, 'SKILL.md'))) {
          candidates.push({ srcDir: grandDir, origin: `bundle:${c.name}`, priority: 2 });
          found++;
        }
      }
    }
    if (!found) log.skippedNoSkill.push(c.name);
  }

  const pluginsRoot = path.join(SRC, 'plugins');
  for (const p of fs.readdirSync(pluginsRoot, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    if (!p.isDirectory()) continue;
    const sk = path.join(pluginsRoot, p.name, 'skills');
    if (!fs.existsSync(sk)) continue;
    for (const s of fs.readdirSync(sk, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      if (!s.isDirectory()) continue;
      const dir = path.join(sk, s.name);
      if (fs.existsSync(path.join(dir, 'SKILL.md'))) {
        candidates.push({ srcDir: dir, origin: `plugin:${p.name}`, priority: 3 });
      }
    }
  }
  return candidates;
}

function main() {
  fs.mkdirSync(DEST, { recursive: true });
  const candidates = collect();
  const taken = new Map(); // normalized name -> {srcDir, desc}

  for (const c of candidates) {
    const md = path.join(c.srcDir, 'SKILL.md');
    let text;
    try { text = readUtf8(md); } catch (e) { log.errors.push(c.srcDir + ': ' + e.message); continue; }
    const parsed = splitFrontmatter(text);
    const headers = parsed ? parseHeaders(parsed.fm) : {};
    const folderName = path.basename(c.srcDir);
    let name = normalizeName(headers.name || folderName);
    if (!validName(name)) {
      const alt = normalizeName(folderName);
      if (!validName(alt)) { log.errors.push(c.srcDir + ': no usable name'); continue; }
      name = alt;
    }

    const desc = (headers.description || '').trim();
    const existing = taken.get(name);
    if (existing) {
      if (existing.desc && desc && existing.desc === desc) { log.skippedDup.push(`${c.srcDir} -> ${name} (identical)`); continue; }
      let i = 2;
      while (taken.has(`${name}-${i}`) || !validName(`${name}-${i}`)) i++;
      const renamed = `${name}-${i}`.slice(0, 64).replace(/-+$/, '');
      log.renamed.push(`${c.srcDir} -> ${renamed} (name clash with ${existing.srcDir})`);
      name = renamed;
    }

    const destDir = path.join(DEST, name);
    try {
      fs.cpSync(c.srcDir, destDir, { recursive: true, force: true });
      const destMd = path.join(destDir, 'SKILL.md');
      const result = ensureFrontmatter(readUtf8(destMd), name, firstParagraph(parsed ? parsed.body : text));
      if (result.synthesized) log.synthesized.push(name);
      if (result.text !== readUtf8(destMd)) fs.writeFileSync(destMd, result.text, 'utf8');
    } catch (e) {
      log.errors.push(c.srcDir + ': ' + e.message);
      continue;
    }

    taken.set(name, { srcDir: c.srcDir, desc });
    log.copied.push({ name, srcDir: c.srcDir, origin: c.origin, priority: c.priority });
  }

  fs.writeFileSync(path.join(DEST, '.ingest-manifest.json'), JSON.stringify({
    generatedAt: new Date().toISOString(),
    source: SRC,
    installed: log.copied.length,
    renamed: log.renamed,
    synthesized: log.synthesized,
    skippedDuplicates: log.skippedDup,
    containersWithoutSkills: log.skippedNoSkill,
    errors: log.errors,
    skills: log.copied,
  }, null, 1), 'utf8');

  console.log(JSON.stringify({
    candidates: candidates.length,
    installed: log.copied.length,
    renamed: log.renamed.length,
    synthesized: log.synthesized.length,
    duplicatesSkipped: log.skippedDup.length,
    containersWithoutSkills: log.skippedNoSkill,
    errors: log.errors.length,
    errorSample: log.errors.slice(0, 5),
    renameSample: log.renamed.slice(0, 8),
    originCounts: log.copied.reduce((a, s) => { const k = s.origin; a[k] = (a[k] || 0) + 1; return a; }, {}),
  }, null, 1));
}

main();
