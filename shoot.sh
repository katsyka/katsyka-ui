#!/bin/bash
# Regenerate thumbs/<id>.jpg for every component (or the ids given) from the live site.
cd "$(dirname "$0")"; mkdir -p thumbs
B=$(ls -d ~/.cache/ms-playwright/chromium-1148/chrome-linux/chrome)
T=$(mktemp -d)
ids=${@:-$(ls components | sed 's/.html$//')}
for id in $ids; do
  timeout 60 $B --headless=new --no-sandbox --hide-scrollbars --use-angle=swiftshader --enable-unsafe-swiftshader \
    --window-size=1200,837 --virtual-time-budget=4000 --autoplay-policy=no-user-gesture-required --screenshot=$T/$id.png "https://ui.katsyka.dev/view.html#$id" >/dev/null 2>&1
  ffmpeg -loglevel error -y -i $T/$id.png -vf crop=1200:750:0:0,scale=960:-1 -q:v 3 thumbs/$id.jpg && echo "ok $id"
done
rm -rf $T
