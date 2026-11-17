#!/bin/sh
# Publish Katsyka UI to https://ui.katsyka.dev (nginx root /root/katsyka-ui-site). media is a symlink so it isn't stored twice.
set -e
OUT=/root/katsyka-ui-site
rsync -a --delete --exclude media /root/kiln/index.html /root/kiln/app.css /root/kiln/app.js /root/kiln/view.html /root/kiln/components /root/kiln/thumbs "$OUT/"
ln -sfn /root/kiln/media/web "$OUT/media"
systemctl restart kiln-mcp
echo "deployed: https://ui.katsyka.dev"
