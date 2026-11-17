---
name: katsyka-ui
description: Build interfaces with Katsyka UI (ui.katsyka.dev), a library of 506 hand-made, original components, full landing pages and mobile screens with strict anti-AI-slop design rules. Use whenever the user asks to build, redesign or polish a UI — a landing page, hero, pricing, auth, dashboard, settings, mobile screen, form, nav, footer, empty/error page, email, background or any control — or asks to make an interface look less generic. Also use when the user mentions Katsyka or Katsyka UI.
---

# Katsyka UI

A component library where every piece is one standalone file (`<style>` + markup + `<script>`, no framework, no build step), designed in light and dark, mobile-first, with reduced-motion fallbacks. Your job is to pick the right pieces, adapt them to the user's project and hold the result to the design rules.

Categories: Mobile 50 · Custom 39 · Forms 36 · Landings 26 · Video 24 · Navigation 21 · Overlays 16 · Pricing 16 · Images 15 · Commerce 15 · States 15 · Display 14 · Auth 14 · Charts 14 · Dashboards 14 · Cards 13 · Text 13 · Backgrounds 13 · Feedback 12 · AI 12 · Content 12 · Features 12 · Emails 12 · Heroes 11 · Testimonials 11 · Settings 10 · Data 9 · Buttons 9 · Scheduling 8 · Dark 6 · Footers 6 · Sections 4 · Shaders 4.

## Workflow

1. **Read the rules once per task.** If the `katsyka-ui` MCP is connected, call `get_design_rules`. Otherwise read `references/design-rules.md`. These rules win over your habits.
2. **Find components.**
   - MCP: `search_components` (query + optional category), then `list_components` to browse a category.
   - Offline: grep `references/catalog.md` (e.g. `grep -i pricing references/catalog.md`).
   - Prefer a full page (Landings, Auth, Dashboards, Errors, Emails) when the user wants a whole page; compose sections when they want something bespoke.
3. **Fetch the code.** MCP: `get_component` (returns HTML, CSS, JS, a full standalone file and integration rules — follow those rules). Offline: `sh scripts/fetch.sh <id> out.html`.
4. **Adapt, don't paste.**
   - Port to the project's stack (React/Vue/Svelte/Astro/plain). Scope the CSS (CSS modules, a wrapper class, or Tailwind equivalents).
   - Replace the component's colours, radii and fonts with the project's tokens. If the project has none, keep Katsyka's `light-dark()` tokens.
   - Replace placeholder copy with the user's real content. Never invent testimonials, logos, stats, prices or customer names — ask, or leave a clearly marked TODO.
   - Self-host any media from ui.katsyka.dev/media before shipping.
   - Keep the accessibility the component already has: labels, focus rings, aria, keyboard support, `prefers-reduced-motion`.
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
- MCP endpoint (Streamable HTTP): https://ui.katsyka.dev/mcp — add with `claude mcp add --transport http katsyka-ui https://ui.katsyka.dev/mcp`
