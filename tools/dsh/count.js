const fs = require('node:fs'), path = require('node:path');
const D = path.join(process.env.USERPROFILE, '.dsh', 'skills');
let total = 0, model = 0, userOnly = 0, neither = 0;
for (const e of fs.readdirSync(D, { withFileTypes: true })) {
  if (!e.isDirectory()) continue; total++;
  const fm = (fs.readFileSync(path.join(D, e.name, 'SKILL.md'), 'utf8').match(/^---\r?\n([\s\S]*?)\r?\n---/) || [])[1] || '';
  const dmi = /^disable-model-invocation:\s*(true|yes|on|1)$/mi.test(fm);
  const uinv = /^user-invocable:\s*(false|no|off|0)$/mi.test(fm);
  if (dmi) userOnly++; else if (uinv) neither++; else model++;
}
console.log(JSON.stringify({ total, modelInvocable: model, userOnly, neither }));
