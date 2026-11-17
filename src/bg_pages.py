# Page layouts for the Backgrounds category. "$" = component class prefix. One concept per background, no shared hero template.
P = {}

P["felt-texture"] = ("Stitchwork Radio", ["Stories", "Makers", "Sleep timer"], """
.$-main{grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:48px;align-items:end}
.$ h1{font:400 clamp(40px,6vw,80px)/1 "Instrument Serif",serif;letter-spacing:-.02em;margin:12px 0 16px;max-width:12ch;text-wrap:balance}
.$-play{display:flex;align-items:center;gap:14px;margin-top:28px}
.$-play .$-btn{width:56px;padding:0;border-radius:50%}
.$-bar{flex:1;max-width:260px;height:4px;border-radius:2px;background:color-mix(in oklab,var(--ink) 25%,transparent)}.$-bar i{display:block;width:34%;height:100%;border-radius:2px;background:var(--ink)}
.$-ep{list-style:none;margin:0;padding:0}.$-ep li{display:grid;grid-template-columns:28px 1fr auto;gap:12px;padding:14px 0;border-top:1px solid color-mix(in oklab,var(--ink) 16%,transparent);font-size:15px}
.$-ep li:first-child{border-top:0}.$-ep b{font-weight:500}.$-ep span{opacity:.6}
""", """
<div><p class="$-eye">Tonight's story · Episode 31</p>
<h1>The whale who kept the lighthouse</h1>
<p class="$-sub">Read slowly, with the lights low. Every character is cut and sewn from wool before we record a single word.</p>
<div class="$-play"><button class="$-btn" type="button" aria-label="Play episode" data-tg aria-pressed="false"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></button><div class="$-bar"><i></i></div><span class="$-mono">04:51 / 14:20</span></div></div>
<div class="$-card"><p class="$-eye">This week</p><ol class="$-ep">
<li><span class="$-mono">31</span><b>The whale who kept the lighthouse</b><span class="$-mono">14:20</span></li>
<li><span class="$-mono">30</span><b>A fox learns to knit</b><span class="$-mono">11:05</span></li>
<li><span class="$-mono">29</span><b>Moon in a teacup</b><span class="$-mono">09:48</span></li></ol></div>
""")

P["water-ripples"] = ("Lido Home", ["Pool", "Garden", "Energy"], """
.$-main{grid-template-rows:1fr auto;gap:32px}
.$-temp{font:300 clamp(96px,18vw,220px)/.85 Geist,system-ui,sans-serif;letter-spacing:-.06em;font-variant-numeric:tabular-nums;margin:8px 0 0}
.$-temp sup{font-size:.3em;letter-spacing:0;vertical-align:top;margin-left:6px}
.$-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) minmax(0,1.2fr);gap:12px}
.$-tg{display:flex;flex-direction:column;align-items:flex-start;gap:18px;min-height:120px;text-align:left;font:500 15px Geist,system-ui,sans-serif;color:inherit;cursor:pointer;transition:background .2s ease-out}
.$-tg i{position:relative;width:40px;height:24px;border-radius:12px;background:color-mix(in oklab,var(--ink) 25%,transparent);transition:background .2s ease-out}
.$-tg i::after{content:"";position:absolute;top:3px;left:3px;width:18px;height:18px;border-radius:50%;background:var(--ink);transition:transform .2s ease-out}
.$-tg[aria-pressed=true] i{background:var(--ink)}.$-tg[aria-pressed=true] i::after{background:var(--fb);transform:translateX(16px)}
.$-tg:active{transform:scale(.97)}
.$-q{display:grid;grid-template-columns:1fr 1fr;gap:4px 16px;align-content:end}.$-q b{font:500 28px Geist,system-ui,sans-serif;font-variant-numeric:tabular-nums}
@media (max-width:760px){.$-row{grid-template-columns:repeat(3,minmax(0,1fr))}.$-q{grid-column:1/-1}}
""", """
<div><p class="$-eye">Water temperature · heating to 28°</p><p class="$-temp">27.5<sup>°C</sup></p></div>
<div class="$-row">
<button type="button" class="$-card $-tg" data-tg aria-pressed="true"><i></i>Filter pump</button>
<button type="button" class="$-card $-tg" data-tg aria-pressed="false"><i></i>Underwater lights</button>
<button type="button" class="$-card $-tg" data-tg aria-pressed="false"><i></i>Pool cover</button>
<div class="$-card $-q"><span class="$-eye">Chlorine</span><span class="$-eye">pH</span><b>1.4<small> ppm</small></b><b>7.3</b></div></div>
""")

P["speckled-graphite"] = ("Halden", ["Recorders", "Microphones", "Support"], """
.$-main{grid-template-columns:minmax(0,1fr) minmax(0,380px);gap:48px;align-items:center}
.$ h1{font:600 clamp(40px,6vw,76px)/.98 Geist,system-ui,sans-serif;letter-spacing:-.045em;margin:14px 0 18px;max-width:13ch}
.$-price{font:500 22px Geist,system-ui,sans-serif;font-variant-numeric:tabular-nums;margin:0 0 24px}
.$-acts{display:flex;gap:10px;flex-wrap:wrap}
.$-spec{display:grid;grid-template-columns:auto 1fr;margin:0}.$-spec dt,.$-spec dd{padding:13px 0;border-top:1px solid color-mix(in oklab,var(--ink) 14%,transparent);font-size:14.5px}
.$-spec dt{opacity:.6;padding-right:24px}.$-spec dd{margin:0;text-align:right;font-variant-numeric:tabular-nums}.$-spec dt:first-of-type,.$-spec dd:first-of-type{border-top:0}
""", """
<div><p class="$-eye">H4 field recorder</p><h1>Machined from one block of aluminium.</h1>
<p class="$-sub">Four preamps quiet enough for birdsong at dawn, in a body you can drop on a riverbank.</p>
<p class="$-price">€1,290</p><div class="$-acts"><a class="$-btn" href="#">Pre-order</a><a class="$-btn $-ghost" href="#">Compare models</a></div></div>
<div class="$-card"><p class="$-eye">Specifications</p><dl class="$-spec"><dt>Inputs</dt><dd>4 × XLR / TRS</dd><dt>Recording</dt><dd>32-bit float, 192 kHz</dd><dt>Battery</dt><dd>9 h, USB-C</dd><dt>Weight</dt><dd>410 g</dd><dt>Ships</dt><dd>March</dd></dl></div>
""")

P["grass-texture"] = ("Verge Seed Co.", ["Lawns", "Meadows", "Guides"], """
.$-main{grid-template-columns:minmax(0,1fr) minmax(0,400px);gap:48px;align-items:start}
.$ h1{font:400 clamp(44px,6.5vw,88px)/.95 "Instrument Serif",serif;letter-spacing:-.02em;margin:14px 0 0;max-width:11ch}
.$-card{padding:24px}.$-card h2{font:600 20px Geist,system-ui,sans-serif;margin:0 0 6px}
.$-opts{display:grid;gap:8px;margin:20px 0;border:0;padding:0}.$-opts legend{font-size:13px;opacity:.7;margin-bottom:8px}
.$-opts label{display:flex;justify-content:space-between;align-items:center;min-height:48px;padding:0 14px;border-radius:10px;border:1px solid color-mix(in oklab,var(--ink) 18%,transparent);cursor:pointer;font-size:15px}
.$-opts label:has(input:checked){border-color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}.$-opts input{accent-color:var(--ink);margin:0 10px 0 0}
.$-opts span{font-variant-numeric:tabular-nums}.$-card .$-btn{width:100%}
""", """
<div><p class="$-eye">Shade mix · sow March to May</p><h1>Stays green under the oak tree.</h1></div>
<form class="$-card" onsubmit="return false"><h2>Shade mix lawn seed</h2><p class="$-sub" style="margin:0">Fine fescues that cope with four hours of light a day.</p>
<fieldset class="$-opts"><legend>Bag size</legend>
<label><span><input type="radio" name="sz" checked>1 kg · 30 m²</span><span>€14</span></label>
<label><span><input type="radio" name="sz">2.5 kg · 75 m²</span><span>€29</span></label>
<label><span><input type="radio" name="sz">5 kg · 150 m²</span><span>€52</span></label></fieldset>
<button class="$-btn" type="submit">Add to basket</button></form>
""")

P["dithered-image"] = ("The Municipal Archive", ["Newspapers", "Maps", "Photographs"], """
.$-main{grid-template-rows:auto auto 1fr;align-items:start;gap:24px}
.$-story{align-self:end}
.$-mast{display:flex;justify-content:space-between;align-items:end;gap:16px;border-bottom:2px solid var(--ink);padding-bottom:12px;font:500 13px "Geist Mono",monospace;font-variant-numeric:tabular-nums}
.$-find{display:flex;gap:8px;width:100%;max-width:480px}.$-find input{flex:1;min-width:0;min-height:48px;padding:0 14px;border:1px solid var(--ink);border-radius:0;background:var(--fb);color:var(--ink);font:15px Geist,system-ui,sans-serif}
.$-find .$-btn{border-radius:0}
.$-story{max-width:520px;background:var(--fb);color:var(--ink);padding:22px;border:1px solid var(--ink);border-radius:0;backdrop-filter:none}
.$-story h1{font:400 clamp(30px,4vw,48px)/1.02 "Instrument Serif",serif;margin:8px 0 10px;text-wrap:balance}
.$-story a{color:inherit;font-weight:600}
""", """
<div class="$-mast"><span>Morning Edition</span><span>Tuesday 14 January 1936</span><span>Page 1 of 12</span></div>
<form class="$-find" role="search" onsubmit="return false"><label class="$-vh" for="$-q">Search the archive</label><input id="$-q" type="search" placeholder="Search names, streets, years" autocomplete="off"><button class="$-btn" type="submit">Search</button></form>
<article class="$-story"><p class="$-eye">Front page · scanned</p><h1>Snow closes the pass road for nine days</h1><p class="$-sub" style="margin:0 0 14px">Post arrives by sledge as crews dig out the upper switchbacks.</p><a href="#">Open the full scan →</a></article>
""")

P["paper-texture"] = ("Oxbow Press", ["Books", "Prints", "About"], """
.$-main{grid-template-columns:minmax(0,1fr) minmax(0,420px);gap:56px;align-items:center}
.$ h1{font:400 clamp(48px,7vw,104px)/.92 "Instrument Serif",serif;letter-spacing:-.02em;margin:10px 0 16px}
.$ h1 i{display:block;font-size:.45em;opacity:.7}
.$-toc{list-style:none;margin:0;padding:0;font:17px/1.4 "Instrument Serif",serif}
.$-toc li{display:flex;align-items:baseline;gap:10px;padding:10px 0;border-top:1px solid color-mix(in oklab,var(--ink) 22%,transparent)}
.$-toc li::after{content:"";order:2;flex:1;border-bottom:1px dotted color-mix(in oklab,var(--ink) 40%,transparent)}
.$-toc span{order:3;font:13px "Geist Mono",monospace;font-variant-numeric:tabular-nums}
.$-buy{display:flex;align-items:center;gap:16px;margin-top:28px;font-variant-numeric:tabular-nums}
""", """
<div><p class="$-eye">Field Notes · Volume III</p><h1>Moths at the Window<i>and other night studies</i></h1>
<p class="$-sub">Forty engravings and short essays, printed letterpress on cotton paper and sewn by hand.</p>
<div class="$-buy"><a class="$-btn" href="#">Order the print edition</a><span>€38 · 212 pages</span></div></div>
<ol class="$-toc"><li>I. The lamp and the garden<span>3</span></li><li>II. Wings under glass<span>27</span></li><li>III. A census of one hedge<span>61</span></li><li>IV. Dust, scale and colour<span>98</span></li><li>V. The last warm night<span>154</span></li></ol>
""")

P["cloud-sky"] = ("Overcast", ["Today", "10 days", "Radar"], """
.$-main{grid-template-rows:1fr auto;gap:28px}
.$-now{display:flex;align-items:flex-end;gap:24px;flex-wrap:wrap}
.$-now .$-deg{font:200 clamp(110px,20vw,240px)/.8 Geist,system-ui,sans-serif;letter-spacing:-.07em;font-variant-numeric:tabular-nums;margin:0}
.$-now p{margin:0 0 12px;font-size:18px;line-height:1.4}
.$-hrs{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));text-align:center;padding:18px 8px}
.$-hrs div{display:grid;gap:10px;font-variant-numeric:tabular-nums;font-size:15px}.$-hrs b{font-size:20px;font-weight:500}
.$-hrs svg{margin:0 auto}
""", """
<div><p class="$-eye">Harbour district · updated 2 min ago</p><div class="$-now"><p class="$-deg">14°</p><p>Mostly cloudy<br>Light wind from the west, 12 km/h</p></div></div>
<div class="$-card $-hrs" role="list" aria-label="Next six hours">
<div role="listitem"><span>Now</span><svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 18h10a4 4 0 0 0 .5-8A6 6 0 0 0 6 11a3.5 3.5 0 0 0 1 7z" fill="none" stroke="currentColor" stroke-width="1.6"/></svg><b>14°</b></div>
<div role="listitem"><span>15:00</span><svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 18h10a4 4 0 0 0 .5-8A6 6 0 0 0 6 11a3.5 3.5 0 0 0 1 7z" fill="none" stroke="currentColor" stroke-width="1.6"/></svg><b>15°</b></div>
<div role="listitem"><span>16:00</span><svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2" stroke="currentColor" stroke-width="1.6"/></svg><b>15°</b></div>
<div role="listitem"><span>17:00</span><svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2" stroke="currentColor" stroke-width="1.6"/></svg><b>13°</b></div>
<div role="listitem"><span>18:00</span><svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 18h10a4 4 0 0 0 .5-8A6 6 0 0 0 6 11a3.5 3.5 0 0 0 1 7z" fill="none" stroke="currentColor" stroke-width="1.6"/></svg><b>12°</b></div>
<div role="listitem"><span>19:00</span><svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 15h10a4 4 0 0 0 .5-8A6 6 0 0 0 6 8a3.5 3.5 0 0 0 1 7zM9 18l-1 3M13 18l-1 3M17 18l-1 3" fill="none" stroke="currentColor" stroke-width="1.6"/></svg><b>11°</b></div></div>
""")

P["lens-distortion"] = ("Narrow Light", ["Walks", "Gear hire", "Gallery"], """
.$-main{grid-template-columns:minmax(0,1fr) minmax(0,420px);gap:48px;align-items:end}
.$ h1{font:600 clamp(40px,6vw,78px)/.95 Geist,system-ui,sans-serif;letter-spacing:-.045em;margin:12px 0 0;max-width:10ch;text-shadow:0 1px 24px rgb(0 0 0/.25)}
.$-slots{display:grid;gap:8px;margin:14px 0 16px;border:0;padding:0}
.$-slots label{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;min-height:52px;padding:0 14px;border-radius:10px;border:1px solid color-mix(in oklab,var(--ink) 16%,transparent);cursor:pointer;font-size:14.5px;font-variant-numeric:tabular-nums}
.$-slots label:has(input:checked){border-color:var(--ink)}.$-slots input{accent-color:var(--ink);margin:0}.$-slots small{opacity:.6;display:block}
.$-card{color:var(--ink2);--ink:var(--ink2)}.$-card .$-btn{width:100%}
""", """
<div><p class="$-eye">Guided photo walks · 3 hours</p><h1>Shoot the canyon at noon light.</h1></div>
<form class="$-card" onsubmit="return false"><p class="$-eye">Choose a session</p><fieldset class="$-slots"><legend class="$-vh">Session</legend>
<label><input type="radio" name="sl" checked><span>Sat 11:30<small>Overhead beams</small></span><span>€45</span></label>
<label><input type="radio" name="sl"><span>Sun 11:00<small>4 places left</small></span><span>€45</span></label>
<label><input type="radio" name="sl"><span>Sun 15:30<small>Warm walls</small></span><span>€40</span></label></fieldset>
<button class="$-btn" type="submit">Book this walk</button></form>
""")

P["stippled-gradient"] = ("Halfmoon Records", ["Releases", "Artists", "Shop"], """
.$-main{grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:48px;align-items:end}
.$ h1{font:700 clamp(56px,10vw,150px)/.82 Geist,system-ui,sans-serif;letter-spacing:-.065em;margin:10px 0 18px;text-transform:uppercase}
.$-fmt{display:flex;gap:8px;flex-wrap:wrap}.$-fmt button{min-height:44px;padding:0 16px;border-radius:0;border:1.5px solid var(--ink);background:none;color:inherit;font:600 14px Geist,system-ui,sans-serif;cursor:pointer;font-variant-numeric:tabular-nums}
.$-fmt button[aria-pressed=true]{background:var(--ink);color:var(--fb)}
.$-trk{list-style:none;margin:0;padding:0;counter-reset:t;background:var(--fb);border:1.5px solid var(--ink)}
.$-trk li{display:grid;grid-template-columns:32px 1fr auto;gap:10px;padding:12px 16px;border-top:1px solid color-mix(in oklab,var(--ink) 25%,transparent);font-size:15px;counter-increment:t}
.$-trk li:first-child{border-top:0}.$-trk li::before{content:counter(t,decimal-leading-zero);font:13px "Geist Mono",monospace;opacity:.6}.$-trk span{font:13px "Geist Mono",monospace;font-variant-numeric:tabular-nums}
""", """
<div><p class="$-eye">Low Tide Choir · LP · out 21 March</p><h1>Salt<br>Hours</h1>
<div class="$-fmt" role="group" aria-label="Format"><button type="button" aria-pressed="true" data-one>Vinyl €28</button><button type="button" aria-pressed="false" data-one>Cassette €12</button><button type="button" aria-pressed="false" data-one>Digital €9</button></div></div>
<ol class="$-trk"><li>Harbour lights<span>4:12</span></li><li>Brine<span>3:47</span></li><li>Rope and pulley<span>5:03</span></li><li>Night ferry<span>6:30</span></li><li>Salt hours<span>4:58</span></li></ol>
""")

P["square-dot-grid"] = ("relay/status", ["Incidents", "Subscribe"], """
.$-main{grid-template-columns:minmax(0,1fr) minmax(0,460px);gap:48px;align-items:center;font-family:"Geist Mono",monospace}
.$ h1{font:500 clamp(36px,5vw,64px)/1 Geist,system-ui,sans-serif;letter-spacing:-.04em;margin:14px 0 12px}
.$-ok{display:inline-flex;align-items:center;gap:8px;font-size:13px}.$-ok::before{content:"";width:8px;height:8px;border-radius:50%;background:#3ccf7e;box-shadow:0 0 0 4px rgb(60 207 126/.2)}
.$-up{font:500 clamp(44px,6vw,72px)/1 Geist,system-ui,sans-serif;letter-spacing:-.04em;font-variant-numeric:tabular-nums;margin:20px 0 4px}
.$-svc{list-style:none;margin:0;padding:0;font-size:14px}.$-svc li{display:flex;justify-content:space-between;gap:12px;padding:13px 0;border-top:1px solid color-mix(in oklab,var(--ink) 14%,transparent)}
.$-svc li:first-child{border-top:0}.$-svc em{font-style:normal;color:#3ccf7e}.$-svc em.w{color:#e8a33a}
""", """
<div><span class="$-ok">All systems operational</span><h1>Relay platform status</h1><p class="$-up">99.98%</p><p class="$-sub">Uptime across all regions, last 90 days</p></div>
<div class="$-card"><p class="$-eye">Services</p><ul class="$-svc"><li>API<em>Operational</em></li><li>Dashboard<em>Operational</em></li><li>Webhooks<em class="w">Degraded · investigating</em></li><li>Object storage<em>Operational</em></li><li>EU-West edge<em>Operational</em></li></ul></div>
""")

P["iridescent-shapes"] = ("Clear Coat", ["Serums", "Ritual", "Journal"], """
.$-main{grid-template-columns:minmax(0,440px) 1fr;align-items:center}
.$ h1{font:500 clamp(44px,6vw,84px)/.95 Geist,system-ui,sans-serif;letter-spacing:-.05em;margin:12px 0 16px}
.$-buy{display:flex;align-items:center;gap:18px;margin-top:26px;font-variant-numeric:tabular-nums}
.$-note{display:flex;gap:20px;margin-top:40px;font-size:13px;opacity:.7}
@media (max-width:760px){.$-main{align-items:end}}
""", """
<div><p class="$-eye">Barrier serum · 30 ml</p><h1>A coat you can almost see.</h1>
<p class="$-sub">A weightless film that holds moisture in and catches the light the way a soap bubble does.</p>
<div class="$-buy"><a class="$-btn" href="#">Add to bag</a><span>€48</span></div>
<div class="$-note"><span>Fragrance free</span><span>Refillable glass</span></div></div><div></div>
""")

P["impressionist-painting"] = ("The Garden Museum", ["Visit", "What's on", "Members"], """
.$-main{grid-template-columns:minmax(0,1fr) minmax(0,440px);gap:48px;align-items:end}
.$ h1{font:400 clamp(48px,7vw,100px)/.92 "Instrument Serif",serif;letter-spacing:-.02em;margin:10px 0 0;max-width:9ch;text-shadow:0 2px 30px rgb(0 0 0/.35)}
.$-ev{list-style:none;margin:0;padding:0}.$-ev li{display:grid;grid-template-columns:56px 1fr auto;gap:14px;align-items:center;padding:14px 0;border-top:1px solid color-mix(in oklab,var(--ink) 14%,transparent)}
.$-ev li:first-child{border-top:0}.$-ev time{font:500 13px/1.2 "Geist Mono",monospace;text-transform:uppercase;font-variant-numeric:tabular-nums}.$-ev time b{display:block;font:500 24px Geist,system-ui,sans-serif}
.$-ev small{display:block;opacity:.6;font-size:13px}.$-ev a{font-size:14px;font-weight:600;color:inherit;min-height:44px;display:inline-flex;align-items:center}
.$-card{color:var(--ink2);--ink:var(--ink2)}
""", """
<div><p class="$-eye">Late openings · Thursdays until 21:00</p><h1>Paint by the pond after dark.</h1></div>
<div class="$-card"><p class="$-eye">This month</p><ul class="$-ev">
<li><time>Thu<b>6</b></time><span>Sketching the lily pond<small>18:30 · Free with entry</small></span><a href="#">Book</a></li>
<li><time>Thu<b>13</b></time><span>Colour mixing for beginners<small>19:00 · €12</small></span><a href="#">Book</a></li>
<li><time>Thu<b>20</b></time><span>Curator's walk: water gardens<small>19:30 · €8</small></span><a href="#">Book</a></li></ul></div>
""")

P["single-hue-landscape"] = ("Ridge 50", ["Race", "Route", "Volunteer"], """
.$-main{grid-template-columns:minmax(0,1fr) minmax(0,460px);gap:48px;align-items:end}
.$ h1{font:400 clamp(46px,7vw,100px)/.92 "Instrument Serif",serif;letter-spacing:-.02em;margin:10px 0 18px;max-width:10ch}
.$-stats{display:flex;gap:28px;font-variant-numeric:tabular-nums}.$-stats b{display:block;font:500 26px Geist,system-ui,sans-serif}.$-stats span{font-size:13px;opacity:.7}
.$-tbl{width:100%;border-collapse:collapse;font-size:14.5px;font-variant-numeric:tabular-nums;margin-bottom:16px}
.$-tbl th{text-align:left;font:500 11px "Geist Mono",monospace;letter-spacing:.08em;text-transform:uppercase;opacity:.6;padding:0 0 10px}
.$-tbl td{padding:12px 0;border-top:1px solid color-mix(in oklab,var(--ink) 16%,transparent)}.$-tbl td:last-child,.$-tbl th:last-child{text-align:right}
.$-card .$-btn{width:100%}
""", """
<div><p class="$-eye">Trail race · 14 June</p><h1>Fifty kilometres along the green ridge.</h1>
<div class="$-stats"><div><b>50 km</b><span>distance</span></div><div><b>2,140 m</b><span>climb</span></div><div><b>11 h</b><span>cut-off</span></div></div></div>
<div class="$-card"><table class="$-tbl"><thead><tr><th>Wave</th><th>Start</th><th>Places</th></tr></thead><tbody>
<tr><td>A · Fast</td><td>06:00</td><td>12 left</td></tr><tr><td>B · Open</td><td>06:30</td><td>48 left</td></tr><tr><td>C · Relay</td><td>07:00</td><td>20 teams</td></tr></tbody></table>
<a class="$-btn" href="#">Enter the race</a></div>
""")
