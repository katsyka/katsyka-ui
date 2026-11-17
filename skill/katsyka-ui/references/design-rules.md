# Katsyka UI design rules

The same rules the Katsyka UI MCP serves through get_design_rules. Follow all that apply.

## Integration rules (every component)

- Icons: inline SVG (or the project's icon set), never emoji as icons. Decorative SVGs get aria-hidden="true"; icon-only buttons need aria-label.
- Tokens: map the component's --bg/--fg/--ac/--r* variables to the project's existing tokens. No new hard-coded hex colours, px font sizes or one-off spacing; reuse the project's scale.
- Content: replace demo copy, names, prices and photos with the project's real content, or clearly marked placeholders. Never invent testimonials, stats, logos or reviews and present them as real.
- Keep both themes working: the CSS uses light-dark(); don't strip the dark values or hard-code a single background.
- Keep the states that exist (hover, focus-visible, active, disabled) and add any that are missing for elements you wire up. Never remove focus outlines without a visible replacement.
- Keep prefers-reduced-motion handling, and animate only transform/opacity.
- Scope: keep the root class prefix so styles don't leak; rename it to fit the project's naming if needed, consistently in HTML, CSS and JS.
- Responsive: check at 360px wide. No horizontal scroll, tap targets at least 44px, text never below 12px.
- Don't add libraries, frameworks or a build step the project doesn't already use; the component is plain HTML/CSS/JS on purpose.

## Situational rules

- Async actions: every button or form that triggers a request needs pending, success and error states. Disable it and show a spinner or 'Saving…' while pending so a second click can't double-submit; show errors inline with a retry, never fail silently or only console.log.
- Forms: every field needs a visible <label> (not only a placeholder), the right type/inputmode/autocomplete, and an error message next to the field linked with aria-describedby. Validate on blur or submit, not every keystroke, and keep the user's input when the request fails.
- Images: set width/height or aspect-ratio (no layout shift), meaningful alt text (alt="" if decorative), loading="lazy" below the fold, and a fallback background if it fails to load. Swap media/ paths for the project's own assets.
- Canvas/WebGL: keep the plain <img>/DOM fallback the component ships with, cap devicePixelRatio, pause the animation loop when off-screen or hidden, and clean up observers and listeners if the component unmounts.
- Data: show a loading skeleton, an empty state and an error state; handle non-2xx responses explicitly.
- Dialogs: trap focus while open, close on Escape and backdrop click, return focus to the trigger, and lock page scroll.

## Colour, type and craft (anti-AI-slop)

- Colour: two colours get it right, the third gets it noticed. Build on a calm 2-colour base (e.g. brown + pale gold, black + ice white), then add ONE bold accent (glowing gold, hot pink, aurora green) used sparingly for the thing that matters. Not five competing brand colours, not the default purple-blue gradient.
- Define colours in OKLCH so lightness stays even across hues and dark-mode variants don't shift in perceived brightness.
- Optical centre: centre by eye, not by math. Play triangles, chevrons and arrows sit a little off the geometric centre so they look centred.
- Kerning/tracking: tighten large display text slightly; add letter-spacing (~0.04–0.1em) to ALL-CAPS labels so they don't look cramped.
- Tabular numbers: font-variant-numeric: tabular-nums on prices, timers, counters and table columns so digits don't jitter as they change.
- Layout shift: reserve space for images, async content and changing labels (fixed width for 'Save'→'Saving…'). Nothing should jump when data loads.
- Optimistic updates: show the result of likes, toggles and small edits immediately, roll back with a message if the request fails.
- Touch targets: at least 44×44px hit area even when the visible control is smaller.
- Line length: body text around 65 characters per line (max-width ~65ch); leading ~1.5 for body, tighter (1.05–1.2) for big headings.
- Widows: avoid a single word on the last line of headings and short paragraphs (text-wrap: balance on headings, pretty on paragraphs).
- Safe areas: keep fixed bars and bottom buttons clear of the notch and home bar with env(safe-area-inset-*).
- Affordance: things that can be clicked, dragged or swiped must look like it; don't rely on hover to reveal that something is interactive.
- Progressive disclosure: show the essentials first, tuck advanced options behind a clear 'More' / disclosure instead of one giant form.
- Comboboxes: long option lists get type-to-filter, keyboard navigation and a visible selected state, not a bare <select> of 200 items.

## 10 niche design hacks

- Concentric radius: a rounded element nested inside another uses inner radius = outer radius − padding (e.g. card 24px, padding 8px → inner 16px). Equal radii on both look wrong at the corners.
- Alpha borders: draw borders as translucent black/white (border-color: rgb(0 0 0 / .1) light, rgb(255 255 255 / .1) dark) instead of a solid grey hex, so they blend into whatever surface or colour is behind them. A fixed #e5e5e5 looks ugly on tinted or coloured cards.
- OKLCH palettes: HSL/hex lightness is not perceptual (yellow and green read far brighter than blue/purple at the same L). Build palette steps and swatch sets in oklch() so equal L means equal perceived brightness.
- OKLCH gradients: gradients interpolated in sRGB go grey and muddy in the middle (blue→orange). Interpolate in OKLCH to stay vivid: linear-gradient(in oklch 90deg, #3b82f6, #f59e0b).
- Matched icon weight: icon stroke-width should match the weight of the text beside it (≈1.5 for regular 400 text at 14–16px, ≈2 for medium/semibold). Heavy icons next to light text look sloppy; one stroke width across the UI.
- Masked edges: horizontally scrolling rows (carousels, chips, tabs) fade out at the edges with mask-image: linear-gradient(to right, transparent, #000 24px, #000 calc(100% - 24px), transparent) instead of cutting items off hard. Don't use a coloured overlay gradient for this.
- Blurred icon swaps: when one icon replaces another (copy → check, play → pause, menu → close), crossfade them with opacity + filter: blur(4px) + scale(.8→1), ~150–200ms ease-out, both icons stacked in the same box. Never a hard swap.
- Dark mode depth: shadows barely show on dark backgrounds, so create depth with lighter surfaces for raised layers (menu/card a step lighter than the page) plus a hairline border, not bigger shadows.
- Dynamic viewport: 100vh is taller than the visible area on mobile and hides content under the browser toolbar. Use 100dvh (or svh for a stable minimum) for full-height heroes, screens and sheets, with 100vh only as a fallback.
- Multiply blending: product photos shot on white look like pasted boxes on a tinted surface. Put them on the tinted card with mix-blend-mode: multiply so the white disappears (light theme only; in dark mode use a light plate or a cut-out image).

## Motion

- Ease-out for entrances (things arrive fast and settle); ease-in-out for things moving from A to B on screen; never linear for UI movement.
- Dropdowns/popovers open in 150–250ms. 400ms+ feels sluggish; make exits ~20% shorter than entrances (e.g. 250ms in / 200ms out).
- Origin-aware: popovers and menus scale from the trigger (transform-origin at the trigger corner) and start at scale(0.95)+opacity 0, never scale(0) from the centre. Exits go back toward the trigger.
- Press feedback: scale buttons to ~0.97 on :active.
- Stagger list rows by ~30ms (not 100–200ms); let a badge or detail trail its parent by ~50ms as it settles.
- Stretch moving knobs/indicators ~12% in the direction of travel (area-preserving), then settle.
- Objects travelling a distance move along a slight arc, not a dead-straight line.
- Confirm success with a short pulse or state change on the control itself.
- No bounce or overshoot on everyday UI (menus, buttons, tabs); save springs for playful, rare moments.
- Don't tween while the user is dragging: track the pointer directly, animate only on release.
- Interruptible: animations must reverse or retarget mid-way when the user changes their mind (CSS transitions or springs, not fixed keyframes that must finish).
- Overlap old and new states (crossfade/exit while the next enters); never out → blank beat → in.
- Reveals and colour changes use clip/mask (clip-path, mask) rather than fading the whole content.
- Swap icons with a scale + opacity + slight blur crossfade, not a hard replacement.
- Dragging past a limit rubber-bands with diminishing resistance instead of a hard stop.
- Shared element transitions: when a card opens into a view, the same element expands (FLIP / View Transitions), not a disconnected replacement.

## 20 principles of UX & animation

- 1 Squash & stretch: things squish slightly on impact to show weight (a dropped chip compresses ~8% then settles).
- 2 Anticipation wind-up: a small wind-up before the big move (send icon pulls back a few px before flying off).
- 3 Staging the focus: direct the eye to one thing at a time; dim/blur or de-emphasise the rest while one element is active.
- 4 Pose to pose: define the key states (start, end, maybe one middle) and let interpolation fill in; don't hand-animate every frame.
- 5 Follow through: parts keep moving briefly after the main body stops (a toast's icon/subtitle trails and settles ~50ms after the card).
- 6 Slow in & slow out: speed up and slow down, never constant speed; no linear easing on UI movement.
- 7 Moving in arcs: objects travelling a distance follow a curve, not a straight line (add-to-cart fly, FAB morphs).
- 8 Secondary action: a small flourish that backs up the main one (a ring/sparkle pulse on the 'Saved' button), never competing with it.
- 9 Snappy timing: duration sets the feel; keep everyday UI under 300ms (tooltips/menus ~150ms, not 500ms).
- 10 Exaggerated feedback: push it past real so the moment lands (wrong password = red border + short shake, not just tiny red text).
- 11 Solid drawing in 3D: give flat things depth and volume where it helps (cards tilt with perspective, light/shadow follow the tilt).
- 12 Overall appeal: the sum of every detail done with care (a bare 'Downloading...' label vs. a proper progress ring with state).
- 13 Fitts's law: bigger, closer targets are faster to hit; put primary actions large and near the user's pointer/thumb.
- 14 Bigger hit areas: the clickable zone can be bigger than it looks (24px icon inside a 44x44 hit box via padding or ::before).
- 15 Hick's law: more choices = slower decisions; cut and group options, show the few that matter first.
- 16 Miller's law: we hold ~7 things at once, so chunk it (card numbers 4-4-4-4, phones 3-3-4, codes in groups).
- 17 Doherty threshold: respond within 400ms or it feels slow; show optimistic UI/instant state change (~100ms), spinners only after that.
- 18 Postel's law: accept messy input, give back clean output (paste '4532015112830366' or '(415) 555-0132' -> normalise and format; never reject spaces/dashes).
- 19 Jakob's law: people expect your app to work like the others (logo top-left goes home, cart top-right, standard icons/gestures).
- 20 Frequency of use: the more it's used, the less it should animate (command palette/keyboard nav = instant; save flourishes for rare moments).

## Mobile (always)

- MOBILE IS NOT A SHRUNK DESKTOP. Design every screen at 360–430px wide first; test at 360, 390 and 430. No horizontal scroll ever (check document.scrollWidth === innerWidth).
- Viewport: <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">. Never disable zoom (no maximum-scale/user-scalable=no).
- Heights: use 100dvh / min-height:100dvh, never bare 100vh (it hides content under mobile browser bars). Scroll containers get overscroll-behavior:contain.
- Safe areas: pad fixed/sticky top bars with env(safe-area-inset-top) and bottom bars/CTAs with max(16px, env(safe-area-inset-bottom)). Nothing tappable inside the home-indicator zone.
- Spacing grid: 8pt with 4pt half-steps (4, 8, 12, 16, 24, 32, 48). Side gutters 16px (20px on ≥414px or for reading). Same gutter on every element of a screen: titles, lists, cards, chips all align to one left edge.
- Touch targets: ≥44×44 (iOS) / 48×48 (Android) for every tappable thing, even when the visible icon is 20–24px — extend the hit area with padding or ::before. ≥8px between adjacent targets. WCAG 2.5.8 floor is 24×24.
- Thumb zone: primary actions live in the bottom third. One primary button per screen, full width, 48–56px tall, radius 12–16, pinned above the safe area. Destructive actions never sit where the thumb rests by default.
- Type scale (px / line-height): large title 34/41 bold, title 28/34, title-2 22/28, headline 17/22 semibold, body 17/22 (min 16), callout 16/21, subhead 15/20, footnote 13/18, caption 12/16. Never under 12px. Inputs must be ≥16px or iOS zooms in.
- Text must survive 200% / largest Dynamic Type: no fixed heights on text containers, allow wrapping, truncate with ellipsis only for single-line list titles. Use rem/em or clamp() for headings.
- Navigation: 3–5 tabs in a bottom tab bar, each with icon AND label (11–12px, 600). Active tab shows filled/weighted icon + full-contrast label, not colour alone. Katsyka standard: floating liquid-glass pill (left/right 20px, 62px tall, radius 31) with a springy lens behind the active tab and an optional round glass search button that stretches into a field — see component m-tabbar.
- Liquid glass: background color-mix(bg 55–60%, transparent) + backdrop-filter: blur(12–20px) saturate(1.6–1.8) + 1px gradient rim (lit top-left/bottom-right) + soft shadow. Provide @media (prefers-reduced-transparency: reduce) solid fallback. Use glass only on floating chrome over scrolling content, never on body text blocks.
- Top bars: 44px nav bar (back · centred 17px title · ≤2 actions). Large title (34px) in content that hands off to the small bar title on scroll; bar gets a hairline/blur only after content scrolls under it.
- Lists: rows ≥44px (52–56 single line, 64–76 with subtitle/avatar). Inset separators aligned to the text start, not the screen edge. Chevron only when the row navigates. Grouped sections with 13px muted captions and footnotes.
- Sheets: grabber 36×5, top radius 16–28, detents (peek / half / full) that snap by position AND flick velocity, drag-down to dismiss, backdrop tap closes, focus moves into the sheet and back to the opener.
- Gestures always have a visible alternative: swipe-to-delete also has a button/menu, long-press menus also open via a ••• button or contextmenu/keyboard. Lock gesture direction after ~8px so vertical scroll isn't hijacked (touch-action: pan-y).
- Feedback: every tap shows a pressed state within 100ms (:active scale .96–.98 or background), no hover-only affordances. Use -webkit-tap-highlight-color:transparent and touch-action:manipulation to kill the 300ms delay and grey flash.
- Keyboards: correct type/inputmode/autocomplete/enterkeyhint on every field (email, tel, one-time-code, numeric, search). Return moves to the next field. Keep the focused field and the submit button visible above the keyboard.
- Images: aspect-ratio boxes to prevent layout shift, object-fit:cover, loading=lazy below the fold, real alt text (empty alt for decorative). Horizontal carousels use scroll-snap with the next item peeking ~16px.
- Motion on mobile: 200–350ms, spring-like ease-out for things that follow the finger, interruptible (a new tap must redirect an animation mid-flight). Respect prefers-reduced-motion.
- States are part of the design: empty, loading (skeletons matching final layout), offline (cached content + banner + retry), error with a way out, and success. Show them, don't leave a blank screen.

## Dark mode

- Dark mode is a second design, not an inverted one. Build tokens with light-dark() (or [data-theme] vars) for every colour: bg, surfaces, text, muted, borders, accent, semantic colours, shadows, chart series.
- Base is NOT pure black: use ~#0f0f11–#121214 (pure #000 only as an explicit OLED option). Pure black removes depth cues and smears on OLED when scrolling.
- Elevation = lighter surface, not bigger shadow: page #0f0f11 → card #18181b → raised #1f1f23 → menu #26262b → dialog #2e2e34 (≈+3–5% lightness per step). Add a 1px inset top highlight (#ffffff0d–17) on raised surfaces; shadows only as a soft extra on the highest layers.
- Text is off-white, not #fff: primary ~#ececee–#f4f4f5 (≈87–93%), secondary ~#a1a1aa (≈60–65%), disabled ~40%. Check ≥4.5:1 for body and ≥3:1 for UI on the ACTUAL surface it sits on (cards and menus are lighter than the page).
- Accents: never reuse the light-mode accent. Raise OKLCH lightness to ~0.7–0.8 and cut chroma 15–30% so it doesn't vibrate; text on accent buttons usually flips to dark. Same for success/warning/error (green-400/amber-300/red-400 range).
- No saturated or neon large areas, no glows, no gradients bleeding colour across the page. Saturated colour is for small signals only (badges, active states, chart lines).
- Borders: hairlines in white at 6–12% alpha (#ffffff0f–1f) instead of grey hexes, so they work on every surface level.
- Typography: light text on dark looks heavier and tighter — drop weight ~50 (e.g. 400→380 variable) for long text, add ~0.05–0.1 line-height and a hair of letter-spacing. Don't use thin weights (<300) for small text.
- Images & media: dim photos slightly (filter: brightness(.88–.92)), give transparent logos/illustrations a dark variant or a subtle plate, avoid large pure-white images in the UI chrome.
- Shadows that remain: darker and larger (e.g. 0 24px 48px #000a), never coloured glows.
- Charts: retune the palette for dark (lighter, less saturated series), gridlines at #ffffff0f, tooltips on a raised surface.
- Respect the system: default to prefers-color-scheme, offer System / Light / Dark, persist the choice, apply it before first paint (inline script in <head>) so there is no flash, set color-scheme on :root so native controls & scrollbars follow, and update <meta name=theme-color> for both schemes.
- Focus rings and selection must be retuned too (lighter blue #93c5fd-ish on dark). Test every component in both themes — a component that only looks good in one theme is unfinished.
