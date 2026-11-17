#!/bin/sh
# Usage: sh fetch.sh <id> [out.html]  — downloads one Katsyka UI component as a standalone file.
# Use only when the katsyka-ui MCP tools are not connected.
set -e
id="$1"; out="${2:-$1.html}"
[ -n "$id" ] || { echo "usage: fetch.sh <id> [out.html]"; exit 1; }
curl -fsSL "https://ui.katsyka.dev/components/$id.html" | sed 's#\(["'"'"'(]\)\.\{0,1\}/\{0,1\}media/#\1https://ui.katsyka.dev/media/#g' > "$out"
echo "saved $out (style + markup + script in one file; media URLs point at ui.katsyka.dev — self-host them for production)"
