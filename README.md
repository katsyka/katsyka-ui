# Katsyka UI

A library of 500+ hand-built web components: everyday controls, custom interactive pieces, WebGL shaders, scroll-driven video heroes, image effects and backgrounds. Every component is a single self-contained file of plain HTML, CSS and JavaScript, with no framework and no build step.

**Live:** [ui.katsyka.dev](https://ui.katsyka.dev)

## Features

- **Copy and paste.** Each component is one standalone file. The site splits it into HTML, CSS and JS tabs, or gives you a complete `index.html` ready to run.
- **Light and dark.** Core components share a token set built on `light-dark()`, with contrast-checked colours, a visible focus ring and reduced-motion support.
- **MCP server.** AI coding tools can search and fetch components, along with integration and design rules, from `ui.katsyka.dev/mcp`.
- **Tested in a real browser.** Every component is rendered in headless Chromium, run through scripted interactions, and checked for JavaScript errors before it ships.

## Categories

Buttons, Forms, Navigation, Overlays, Feedback, Display, Cards, Text, Custom, Shaders, Video, Heroes, Images, Backgrounds.

## Repository layout

| Path | Contents |
| --- | --- |
| `components/` | One `<id>.html` file per component |
| `index.html`, `app.js`, `app.css` | Gallery site; the component registry is the `C` array in `app.js` |
| `view.html` | Renders a single component full-screen |
| `src/tokens.py` | Injects the shared design tokens into components that declare `@TOKENS` |
| `src/gen_bg.py` | Generates the WebGL background components |
| `mcp/server.mjs` | MCP server (Node, no dependencies) |
| `thumbs/` | Gallery thumbnails |

Video and media assets are not included in this repository.

## Using with an AI assistant

Add the MCP server to any MCP-capable client:

```json
{
  "mcpServers": {
    "katsyka-ui": { "url": "https://ui.katsyka.dev/mcp" }
  }
}
```

Tools: `list_components`, `search_components`, `get_component`, `get_design_rules`.

## Running locally

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

## Adding a component

1. Create `components/<id>.html` containing a `<style>` block, the markup and a `<script>` block.
2. Register it in the `C` array in `app.js`.
3. To use the shared tokens, put `@TOKENS(.root)` in the style block and run `python3 src/tokens.py components/<id>.html`.

## License

MIT
