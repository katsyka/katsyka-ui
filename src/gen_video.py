#!/usr/bin/env python3
"""Scroll-scrubbed video heroes from frame sequences in media/web/<clip>/001-120.jpg.
Text never sits on a tint: per-frame luminance of each text region is measured here and the text flips dark/light.
Run: python3 src/gen_video.py [ids] [--reg]"""
import sys, json, pathlib
from PIL import Image, ImageStat
ROOT = pathlib.Path('/root/kiln'); N = 120
# region boxes (x0,y0,x1,y1) in 0..1 of a 16:9 frame; 'm' = mobile bottom band
REG = {'tl': (.04, .1, .46, .42), 'bl': (.04, .58, .5, .92), 'tr': (.54, .1, .96, .42), 'br': (.54, .58, .96, .92), 'm': (.36, .62, .64, .94), 'nav': (0, 0, 1, .09)}

def lum(clip):
    out = {k: '' for k in REG}
    for i in range(1, N + 1):
        im = Image.open(ROOT / f'media/web/{clip}/{i:03d}.jpg').convert('L'); w, h = im.size
        for k, (a, b, c, d) in REG.items():
            v = ImageStat.Stat(im.crop((int(a*w), int(b*h), int(c*w), int(d*h)))).mean[0]
            out[k] += '0123456789abcdefghijklmnopqrstuvwxyz'[min(35, int(v / 256 * 36))]
    return out

CSS = r'''
.vs{--fg:#f4f2ee;--ink:#141412;position:relative;height:var(--len,560vh);background:#0d0d0c;color:var(--fg);font:16px/1.5 Geist,system-ui,sans-serif}
.vs-st{position:sticky;top:0;height:100vh;height:100dvh;overflow:hidden}
.vs canvas{position:absolute;inset:0;width:100%;height:100%;display:block}
.vs-nav{position:absolute;top:0;left:0;right:0;display:flex;align-items:center;gap:24px;padding:20px clamp(16px,4vw,48px);z-index:3;transition:color .3s}
.vs-nav b{font-weight:650;letter-spacing:-.01em;font-size:17px}.vs-nav nav{display:flex;gap:22px;margin-left:auto;font-size:14px}.vs-nav nav a{color:inherit;text-decoration:none;opacity:.85}.vs-nav nav a:hover{opacity:1}
.vs-cta{display:inline-flex;align-items:center;height:44px;padding:0 20px;border-radius:999px;font-weight:600;font-size:14px;text-decoration:none;background:var(--fg);color:var(--ink);transition:background .3s,color .3s}
.vs .dk{color:var(--ink)}.vs .dk .vs-cta,.vs-nav.dk .vs-cta{background:var(--ink);color:var(--fg)}
.vs-ch{position:absolute;z-index:2;width:min(440px,calc(100% - 32px));opacity:0;transform:translateY(16px);transition:opacity .45s cubic-bezier(.23,1,.32,1),transform .45s cubic-bezier(.23,1,.32,1),color .3s;pointer-events:none}
.vs-ch.on{opacity:1;transform:none;pointer-events:auto}
.vs-ch.tl{left:clamp(16px,4vw,48px);top:16vh}.vs-ch.bl{left:clamp(16px,4vw,48px);bottom:12vh}.vs-ch.tr{right:clamp(16px,4vw,48px);top:16vh}.vs-ch.br{right:clamp(16px,4vw,48px);bottom:12vh}
.vs-ch h2{margin:0 0 12px;font-size:clamp(34px,5vw,64px);line-height:1;letter-spacing:-.035em;font-weight:620;text-wrap:balance}
.vs-ch p{margin:0;font-size:17px;max-width:38ch;opacity:.9;text-wrap:pretty}
.vs-ch dl{display:flex;gap:28px;margin:20px 0 0}.vs-ch dt{font-size:12px;opacity:.75}.vs-ch dd{margin:0;font-size:26px;font-weight:600;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.vs-ch .vs-cta{margin-top:22px}
.vs-rail{position:absolute;right:clamp(12px,2vw,28px);top:50%;translate:0 -50%;display:grid;gap:6px;z-index:3;transition:color .3s}
.vs-rail button{width:44px;height:28px;display:grid;place-items:center;background:none;border:0;padding:0;cursor:pointer;color:inherit}
.vs-rail button i{width:2px;height:14px;border-radius:1px;background:currentColor;opacity:.35;transition:opacity .2s,height .25s cubic-bezier(.23,1,.32,1)}
.vs-rail button[aria-current=true] i{opacity:1;height:24px}
.vs-rail button:focus-visible{outline:2px solid currentColor;outline-offset:2px;border-radius:4px}
.vs-hint{position:absolute;left:50%;bottom:24px;translate:-50% 0;font-size:12px;letter-spacing:.04em;opacity:.8;transition:opacity .3s,color .3s;z-index:2}
.vs-hint.off{opacity:0}
@media (max-width:760px){.vs-nav nav{display:none}.vs-ch,.vs-ch.tl,.vs-ch.bl,.vs-ch.tr,.vs-ch.br{left:16px;right:auto;top:auto;bottom:max(80px,calc(env(safe-area-inset-bottom) + 64px))}.vs-ch h2{font-size:clamp(32px,9vw,44px)}.vs-ch p{font-size:16px}.vs-rail{right:4px}}
@media (prefers-reduced-motion:reduce){.vs-ch{transition:opacity .2s}}
'''

JS = r'''
(()=>{
const root=document.querySelector('.vs'),c=root.querySelector('canvas'),x=c.getContext('2d'),N=120,DIR=root.dataset.dir,L=JSON.parse(root.dataset.lum),CH=[...root.querySelectorAll('.vs-ch')],rail=root.querySelector('.vs-rail'),nav=root.querySelector('.vs-nav'),hint=root.querySelector('.vs-hint');
const imgs=[],load=i=>{if(imgs[i])return;const im=imgs[i]=new Image();im.onload=()=>{if(Math.abs(i-cur)<9)draw(true)};im.src=DIR+String(i+1).padStart(3,'0')+'.jpg'};
load(0);new IntersectionObserver((e,o)=>{if(e[0].isIntersecting){o.disconnect();[8,4,2,1].forEach(s=>{for(let i=0;i<N;i+=s)load(i)})}},{rootMargin:'100%'}).observe(root);
let cur=0,tgt=0,shown=-1,raf=0;
const pick=f=>{for(let d=0;d<N;d++)for(const j of[f-d,f+d]){const im=imgs[j];if(im&&im.complete&&im.naturalWidth)return im}};
function draw(force){const f=Math.round(cur);if(f===shown&&!force)return;const im=pick(f);if(!im)return;shown=f;const s=Math.max(c.width/im.naturalWidth,c.height/im.naturalHeight),w=im.naturalWidth*s,h=im.naturalHeight*s;x.drawImage(im,(c.width-w)/2,(c.height-h)/2,w,h)}
new ResizeObserver(()=>{const d=Math.min(devicePixelRatio,2);c.width=c.clientWidth*d;c.height=c.clientHeight*d;draw(true)}).observe(c);
const mob=matchMedia('(max-width:760px)'),dk=(el,k,f)=>el.classList.toggle('dk',parseInt(L[k][f],36)>=17);
rail.innerHTML=CH.map((ch,i)=>`<button aria-label="Go to: ${ch.querySelector('h2').textContent}"><i></i></button>`).join('');const RB=[...rail.children];
RB.forEach((b,i)=>b.onclick=()=>{const a=+CH[i].dataset.a,top=root.getBoundingClientRect().top+scrollY;scrollTo({top:top+(a+.02)*(root.offsetHeight-innerHeight),behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'})});
function update(){draw();const f=Math.round(cur),p=cur/(N-1);dk(nav,'nav',f);dk(rail,'tr',f);hint&&(hint.classList.toggle('off',p>.04),dk(hint,'m',f));
CH.forEach((ch,i)=>{const on=p>=+ch.dataset.a&&p<+ch.dataset.b;ch.classList.toggle('on',on);ch.inert=!on;dk(ch,mob.matches?'m':ch.dataset.r,f);RB[i].setAttribute('aria-current',on)})}
const tick=()=>{cur+=(tgt-cur)*.2;if(Math.abs(tgt-cur)<.05)cur=tgt;update();raf=cur===tgt?0:requestAnimationFrame(tick)};
const onScroll=()=>{const r=root.getBoundingClientRect();tgt=Math.max(0,Math.min(1,-r.top/(root.offsetHeight-innerHeight)))*(N-1);if(!raf)raf=requestAnimationFrame(tick)};
addEventListener('scroll',onScroll,{passive:true});onScroll();
})();
'''

# id, clip, name, desc, tags, brand, links, cta, chapters [(a,b,region,h2,body,extra)]
V = [
 ('gt-reveal', 'sportcar', 'Supercar Reveal', 'Scroll a matte supercar from a smoky studio arrival to doors up and the engine bay exposed; specs appear per chapter, chapter rail jumps between them.', ['video', 'scroll', 'car', 'product', 'reveal'],
  'Vanta', ['Models', 'Configure', 'Dealers'], 'Configure yours',
  [(0, .3, 'tl', 'Vanta GT', 'Carbon tub, 1,390 kg dry. Built in batches of forty.', ''),
   (.36, .64, 'bl', 'Doors up.', 'Dihedral doors open in 1.2 seconds and clear a standard parking bay.', '<dl><div><dt>0–100 km/h</dt><dd>2.6 s</dd></div><div><dt>Top speed</dt><dd>338 km/h</dd></div></dl>'),
   (.72, 1.01, 'tl', 'Nothing hidden.', 'A 4.0 litre twin-turbo V8 with a 160 kW e-motor on the front axle, under glass.', '<dl><div><dt>Combined</dt><dd>1,040 hp</dd></div><div><dt>Torque</dt><dd>1,100 Nm</dd></div></dl><a class="vs-cta" href="#">Configure yours</a>')]),
 ('hammam-descent', 'hammam', 'Hammam Descent', 'Scroll down from a star-pierced dome through shafts of light to the warm pool and marble platform of an old bathhouse; a spa booking story.', ['video', 'scroll', 'spa', 'architecture', 'light'],
  'Çinili Hamam', ['Rituals', 'History', 'Visit'], 'Book a ritual',
  [(0, .3, 'bl', 'Built in 1640.', 'A dome with 99 glass stars. At noon each one throws its own beam onto the stone.', ''),
   (.38, .66, 'tl', 'Warm, then hot.', 'Three rooms, each a few degrees hotter, ending at the göbek taşı: the heated marble platform.', ''),
   (.74, 1.01, 'tl', 'Ninety minutes, no phone.', 'Scrub, foam massage and mint tea in the cold room after.', '<dl><div><dt>Ritual</dt><dd>€65</dd></div><div><dt>Open</dt><dd>7–23</dd></div></dl><a class="vs-cta" href="#">Book a ritual</a>')]),
 ('movement-reveal', 'clocks', 'Watch Movement Reveal', 'Scroll from inside a mechanical watch movement, past the balance wheel and gear train, pulling back to the finished watch resting on basalt.', ['video', 'scroll', 'watch', 'luxury', 'product'],
  'Holm Horlogerie', ['Collection', 'Atelier', 'Service'], 'Find a retailer',
  [(0, .28, 'bl', '312 parts.', 'The calibre H-7 is assembled by one watchmaker, start to finish, in about nine days.', ''),
   (.34, .58, 'tl', 'Beats 21,600 times an hour.', 'A free-sprung balance with a silicon hairspring, unaffected by magnetism.', '<dl><div><dt>Reserve</dt><dd>72 h</dd></div><div><dt>Jewels</dt><dd>31</dd></div></dl>'),
   (.68, 1.01, 'tl', 'Basalt, 40 mm.', 'A grey dial cut from volcanic stone, in a bronze case that darkens with you.', '<dl><div><dt>Edition</dt><dd>180</dd></div><div><dt>Price</dt><dd>CHF 9,400</dd></div></dl><a class="vs-cta" href="#">Find a retailer</a>')]),
 ('studio-walkin', 'workshop', 'Studio Walk-in', 'Scroll through the door of a ceramics workshop on a wet cobbled street, past shelves of glazed pots to the workbench; a craft class booking story.', ['video', 'scroll', 'craft', 'workshop', 'ceramics'],
  'Kiln Lane', ['Classes', 'Shop', 'Visit'], 'See class dates',
  [(0, .26, 'tr', 'Come in, it\'s raining.', 'A pottery studio in a 1902 stable, two minutes from the tram.', ''),
   (.36, .62, 'bl', 'Four wheels, one kiln.', 'Six people per class, so everyone gets a wheel and time with the teacher.', ''),
   (.72, 1.01, 'tl', 'Leave with a set.', 'Throw, trim and glaze four pieces over three evenings. We fire them and text you when they\'re ready.', '<dl><div><dt>3 evenings</dt><dd>€140</dd></div><div><dt>Clay & firing</dt><dd>Included</dd></div></dl><a class="vs-cta" href="#">See class dates</a>')]),
 ('house-dusk', 'house', 'House at Dusk', 'Scroll from a concrete house reflected in a pool at blue hour, through the glass and past people working, to a door opening onto the city; for a studio or co-working space.', ['video', 'scroll', 'architecture', 'workspace', 'interior'],
  'Atelier Lume', ['Spaces', 'Membership', 'Events'], 'Book a tour',
  [(0, .26, 'tl', 'A quieter office.', 'Twelve desks in a converted villa, ten minutes from the centre.', ''),
   (.34, .6, 'tl', 'Light until late.', 'Floor-to-ceiling glass on three sides, and lamps that dim with the sunset.', ''),
   (.7, 1.01, 'tl', 'Your desk, your key.', 'Fixed desk, 24/7 access, lockers, meeting room hours and the best coffee on the hill.', '<dl><div><dt>Fixed desk</dt><dd>€390/mo</dd></div><div><dt>Day pass</dt><dd>€28</dd></div></dl><a class="vs-cta" href="#">Book a tour</a>')]),
 ('paper-city', 'papercity', 'Paper City', 'Scroll a folded sheet as it opens into a river, then houses, then a full pop-up skyline with a bridge; a three-step product story.', ['video', 'scroll', 'paper', 'story', 'steps'],
  'Plié', ['Kits', 'How it works', 'Gifts'], 'Shop city kits',
  [(0, .24, 'tr', 'One sheet.', 'Every Plié kit starts flat and fits in an envelope.', ''),
   (.3, .56, 'tl', 'Unfold the river.', 'Pre-scored creases, no glue, no scissors. The water comes first.', ''),
   (.64, 1.01, 'tl', 'Then the city rises.', '180 pieces, about two hours, one skyline on your desk.', '<dl><div><dt>Cities</dt><dd>12</dd></div><div><dt>From</dt><dd>€34</dd></div></dl><a class="vs-cta" href="#">Shop city kits</a>')]),
]

def build(v):
    id_, clip, name, desc, tags, brand, links, cta, chs = v
    L = lum(clip)
    ch = ''.join(f'<section class="vs-ch {r}" data-a="{a}" data-b="{b}" data-r="{r}"><h2>{h}</h2><p>{t}</p>{e}</section>' for a, b, r, h, t, e in chs)
    lj = json.dumps(L); ln = ''.join('<a href="#">%s</a>' % l for l in links)
    html = ('<style>' + CSS + '</style>\n<div class="vs" data-dir="media/' + clip + '/" data-lum=\'' + lj + '\'><div class="vs-st">'
            + '<canvas role="img" aria-label="' + desc + '"></canvas><header class="vs-nav"><b>' + brand + '</b><nav>' + ln + '</nav><a class="vs-cta" href="#">' + cta + '</a></header>'
            + ch + '<div class="vs-rail" aria-label="Chapters"></div><span class="vs-hint">Scroll</span></div></div>\n<script>' + JS + '</script>\n')
    (ROOT / 'components' / f'{id_}.html').write_text(html)
    return [id_, name, 'Video', desc, tags, 1]

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    E = [build(v) for v in V if not args or v[0] in args]
    print('built', len(E))
    if '--reg' in sys.argv:
        for e in E: print('  ' + json.dumps(e, ensure_ascii=False) + ',')
