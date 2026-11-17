// Builds the Claude skill "katsyka-ui" from the MCP rule arrays + live registry.
// node src/build_skill.mjs  → skill/katsyka-ui/** + skill/katsyka-ui.zip (+ copies zip to site/downloads)
import fs from "node:fs";
import { execSync } from "node:child_process";

const K = "/root/kiln", SITE = "/root/katsyka-ui-site", OUT = `${K}/skill/katsyka-ui`;
const srv = fs.readFileSync(`${K}/mcp/server.mjs`, "utf8");
const arr = n => { const m = srv.match(new RegExp(`const ${n} = (\\[[\\s\\S]*?\\n\\]);`)); return new Function(`return ${m[1]}`)(); };
const app = fs.readFileSync(`${K}/app.js`, "utf8");
const C = new Function(`return ${app.slice(app.indexOf("const C = [") + 10, app.indexOf("].map(") + 1)}`)();

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(`${OUT}/references`, { recursive: true });
fs.mkdirSync(`${OUT}/scripts`, { recursive: true });

const sec = (t, a) => `## ${t}\n\n${a.map(x => `- ${typeof x === "string" ? x : x.join ? x.join(" ") : JSON.stringify(x)}`).join("\n")}\n`;
let extra = []; try { extra = arr("EXTRA").map(x => Array.isArray(x) ? x[1] : x); } catch {}
fs.writeFileSync(`${OUT}/references/design-rules.md`, `# Katsyka UI design rules\n\nThe same rules the Katsyka UI MCP serves through get_design_rules. Follow all that apply.\n\n` +
  sec("Integration rules (every component)", arr("RULES")) + "\n" + (extra.length ? sec("Situational rules", extra) + "\n" : "") +
  sec("Colour, type and craft (anti-AI-slop)", arr("DESIGN")) + "\n" + sec("10 niche design hacks", arr("CRAFT")) + "\n" + sec("Motion", arr("MOTION")) + "\n" +
  sec("20 principles of UX & animation", arr("UX")) + "\n" + sec("Mobile (always)", arr("MOBILE")) + "\n" + sec("Dark mode", arr("DARK")));

const cats = {};
for (const [id, name, cat, desc, tags] of C) (cats[cat] ||= []).push(`- \`${id}\` **${name}** — ${desc}${tags?.length ? ` _(${tags.join(", ")})_` : ""}`);
fs.writeFileSync(`${OUT}/references/catalog.md`, `# Katsyka UI catalog (${C.length} components)\n\nGrep this file for a keyword, then fetch the id. Preview any id at https://ui.katsyka.dev/<id>.\n\n` +
  Object.entries(cats).sort((a, b) => b[1].length - a[1].length).map(([c, l]) => `## ${c} (${l.length})\n\n${l.join("\n")}\n`).join("\n"));

fs.writeFileSync(`${OUT}/scripts/fetch.sh`, `#!/bin/sh
# Usage: sh fetch.sh <id> [out.html]  — downloads one Katsyka UI component as a standalone file.
# Use only when the katsyka-ui MCP tools are not connected.
set -e
id="$1"; out="\${2:-$1.html}"
[ -n "$id" ] || { echo "usage: fetch.sh <id> [out.html]"; exit 1; }
curl -fsSL "https://ui.katsyka.dev/components/$id.html" | sed 's#\\(["'"'"'(]\\)\\.\\{0,1\\}/\\{0,1\\}media/#\\1https://ui.katsyka.dev/media/#g' > "$out"
echo "saved $out (style + markup + script in one file; media URLs point at ui.katsyka.dev — self-host them for production)"
`);

const counts = Object.entries(cats).sort((a, b) => b[1].length - a[1].length).map(([c, l]) => `${c} ${l.length}`).join(" · ");
fs.writeFileSync(`${OUT}/SKILL.md`, `---
name: katsyka-ui
description: Build interfaces with Katsyka UI (ui.katsyka.dev), a library of ${C.length} hand-made, original components, full landing pages and mobile screens with strict anti-AI-slop design rules. Use whenever the user asks to build, redesign or polish a UI — a landing page, hero, pricing, auth, dashboard, settings, mobile screen, form, nav, footer, empty/error page, email, background or any control — or asks to make an interface look less generic. Also use when the user mentions Katsyka or Katsyka UI.
---

# Katsyka UI

A component library where every piece is one standalone file (\`<style>\` + markup + \`<script>\`, no framework, no build step), designed in light and dark, mobile-first, with reduced-motion fallbacks. Your job is to pick the right pieces, adapt them to the user's project and hold the result to the design rules.

Categories: ${counts}.

## Workflow

1. **Read the rules once per task.** If the \`katsyka-ui\` MCP is connected, call \`get_design_rules\`. Otherwise read \`references/design-rules.md\`. These rules win over your habits.
2. **Find components.**
   - MCP: \`search_components\` (query + optional category), then \`list_components\` to browse a category.
   - Offline: grep \`references/catalog.md\` (e.g. \`grep -i pricing references/catalog.md\`).
   - Prefer a full page (Landings, Auth, Dashboards, Errors, Emails) when the user wants a whole page; compose sections when they want something bespoke.
3. **Fetch the code.** MCP: \`get_component\` (returns HTML, CSS, JS, a full standalone file and integration rules — follow those rules). Offline: \`sh scripts/fetch.sh <id> out.html\`.
4. **Adapt, don't paste.**
   - Port to the project's stack (React/Vue/Svelte/Astro/plain). Scope the CSS (CSS modules, a wrapper class, or Tailwind equivalents).
   - Replace the component's colours, radii and fonts with the project's tokens. If the project has none, keep Katsyka's \`light-dark()\` tokens.
   - Replace placeholder copy with the user's real content. Never invent testimonials, logos, stats, prices or customer names — ask, or leave a clearly marked TODO.
   - Self-host any media from ui.katsyka.dev/media before shipping.
   - Keep the accessibility the component already has: labels, focus rings, aria, keyboard support, \`prefers-reduced-motion\`.
5. **Check before you call it done.**
   - 360px, 390px and 430px wide: no horizontal scroll, 44px+ touch targets, inputs ≥16px.
   - Light and dark both designed, not inverted.
   - Async buttons and forms have loading, success and error states.
   - At most two base colours + one accent; no glows, no gradient text, no emoji as icons, no generic "bento of features".

## Taste notes

- Original concepts beat familiar SaaS templates. If a section looks like every other AI landing page (glowing orb hero, three icon cards, logo cloud of fake brands), change it.
- One idea per section, generous whitespace, real typographic hierarchy (size + weight + colour, not just size).
- Motion is ease-out, 150–300ms for UI; long choreography only for heroes and scroll stories.
- Photos stay untinted; text sits beside images, not in cards over them.

## Links

- Browse: https://ui.katsyka.dev · Preview one: https://ui.katsyka.dev/<id>
- MCP endpoint (Streamable HTTP): https://ui.katsyka.dev/mcp — add with \`claude mcp add --transport http katsyka-ui https://ui.katsyka.dev/mcp\`
`);

execSync(`cd ${K}/skill && rm -f katsyka-ui.zip && zip -qr katsyka-ui.zip katsyka-ui`);
fs.mkdirSync(`${SITE}/downloads`, { recursive: true });
fs.copyFileSync(`${K}/skill/katsyka-ui.zip`, `${SITE}/downloads/katsyka-ui-skill.zip`);
console.log(`skill built: ${C.length} components, ${fs.statSync(`${K}/skill/katsyka-ui.zip`).size} bytes`);
