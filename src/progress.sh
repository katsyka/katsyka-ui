#!/bin/sh
# Posts Katsyka UI build progress to YukiChat every 5 min until /root/kiln/src/.progress-stop exists.
cd /root/kiln
while [ ! -f src/.progress-stop ]; do
  sleep 300; [ -f src/.progress-stop ] && break
  n=$(grep -h '^=== ' src/packs/*.txt | wc -l)
  built=$(for i in $(grep -h '^=== ' src/packs/*.txt | cut -c5-); do [ -f components/$i.html ] && echo $i; done | wc -l)
  last=$(ls -t src/packs/*.txt | head -1 | xargs basename | sed 's/.txt//')
  ids=$(grep -h '^=== ' $(ls -t src/packs/*.txt | head -1) | cut -c5- | tr '\n' ' ')
  cats=$(grep -h '^<!--' src/packs/*.txt | awk -F'|' '{print $2}' | sort | uniq -c | awk '{printf "%s %s · ",$2,$1}')
  python3 /root/yukichat/claude_say.py vasiliy "⏱ Katsyka UI progress: $built / 200 components built and tested
By category: $cats
Latest pack ($last): $ids
Not deployed yet. The site updates at the end, after every pack passes the browser tests." >/dev/null 2>&1
done
