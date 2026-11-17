# Generates the Backgrounds category: one shared WebGL shell + per-background shader body.
# python3 src/gen_bg.py  -> components/<id>.html
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(os.path.dirname(__file__), "..", "components")

COMMON = r"""precision highp float;uniform vec2 r,m,us;uniform float t,ld;uniform sampler2D u;uniform vec3 k0,k1,k2;
float h(vec2 p){vec3 q=fract(vec3(p.xyx)*.1031);q+=dot(q,q.yzx+33.33);return fract((q.x+q.y)*q.z);}
vec2 h2(vec2 p){vec3 q=fract(vec3(p.xyx)*vec3(.1031,.103,.0973));q+=dot(q,q.yzx+33.33);return fract((q.xx+q.yz)*q.zy);}
float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+1.),f.x),f.y);}
float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<5;i++){v+=a*n(p);p=mat2(.8,.6,-.6,.8)*p*2.03+1.7;a*=.5;}return v;}
vec2 cover(vec2 q){float ra=r.x/r.y,ia=us.x/us.y;vec2 s=ra>ia?vec2(1.,ia/ra):vec2(ra/ia,1.);return (q-.5)*s+.5;}
vec3 img(vec2 q){return texture2D(u,clamp(q,.001,.999)).rgb;}
float lum(vec3 c){return dot(c,vec3(.299,.587,.114));}
"""

SHELL = """<style>
.{c}{{position:relative;min-height:100vh;display:flex;flex-direction:column;overflow:hidden;--ink:{ink};--fb:{fb};--ink2:var(--ink);background:var(--fb);color:var(--ink);isolation:isolate;font:16px/1.5 Geist,system-ui,sans-serif}}
.{c} canvas,.{c}>img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-1}}
.{c}>img{{display:none;filter:{imgf}}}
.{c}.nogl canvas{{display:none}}.{c}.nogl>img{{display:block}}
.{c}-nav{{display:flex;align-items:center;gap:28px;padding:20px clamp(16px,4vw,48px)}}
.{c}-nav nav{{display:flex;gap:22px}}
.{c}-nav b{{font-weight:600;font-size:16px;letter-spacing:-.01em}}
.{c}-nav a{{color:inherit;text-decoration:none;font-size:14px;opacity:.72;transition:opacity .15s ease-out}}.{c}-nav a:hover{{opacity:1}}
.{c}-main{{flex:1;display:grid;padding:clamp(24px,5vw,64px) clamp(16px,4vw,48px) clamp(32px,6vw,72px)}}
.{c}-eye{{margin:0;font:500 11px/1.4 "Geist Mono",ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;opacity:.72}}
.{c}-sub{{font-size:17px;line-height:1.55;max-width:44ch;margin:0;opacity:.8;text-wrap:pretty}}
.{c}-mono{{font:13px "Geist Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums}}
.{c}-btn{{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 22px;border:0;border-radius:10px;background:var(--ink);color:var(--fb);font:600 15px Geist,system-ui,sans-serif;text-decoration:none;cursor:pointer;transition:transform .15s ease-out,opacity .15s ease-out}}
.{c}-btn:active{{transform:scale(.97)}}.{c}-ghost{{background:none;color:inherit;box-shadow:inset 0 0 0 1px color-mix(in oklab,var(--ink) 35%,transparent)}}
.{c}-card{{background:color-mix(in oklab,var(--fb) 84%,transparent);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid color-mix(in oklab,var(--ink) 12%,transparent);border-radius:16px;padding:20px}}
.{c}-card>.{c}-eye:first-child{{margin-bottom:10px}}
.{c}-vh{{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}}
.{c}-pal{{margin-left:auto;display:flex;gap:2px}}
.{c}-pal button{{display:grid;place-items:center;width:44px;height:44px;padding:0;border:0;border-radius:50%;background:none;cursor:pointer}}
.{c}-pal button i{{width:18px;height:18px;border-radius:50%;background:var(--g);box-shadow:0 0 0 1px color-mix(in oklab,var(--ink) 30%,transparent);transition:transform .15s ease-out}}
.{c}-pal button[aria-pressed=true] i{{box-shadow:0 0 0 2px var(--fb),0 0 0 3.5px var(--ink)}}
.{c} :focus-visible{{outline:2px solid currentColor;outline-offset:3px}}
@media (max-width:760px){{.{c}-main{{grid-template-columns:1fr!important;gap:28px!important}}.{c}-nav nav{{display:none}}}}
{pcss}
</style>
<section class="{c}">
  <canvas aria-hidden="true"></canvas>
{imgtag}  <header class="{c}-nav"><b>{brand}</b><nav aria-label="{brand}">{links}</nav>{pal}</header>
  <main class="{c}-main">{phtml}</main>
</section>
<script>
(()=>{{
const S=document.currentScript?document.currentScript.previousElementSibling:document.querySelector(".{c}");
const root=S&&S.classList.contains("{c}")?S:document.querySelector(".{c}");
const cv=root.querySelector("canvas"),gl=cv.getContext("webgl",{{antialias:false}});
const RM=matchMedia("(prefers-reduced-motion: reduce)").matches,IMG={imgjs};
const off=()=>root.classList.add("nogl");
if(!gl)return off();
const FS={fs};
const sh=(ty,s)=>{{const o=gl.createShader(ty);gl.shaderSource(o,s);gl.compileShader(o);return o}};
const P=gl.createProgram();gl.attachShader(P,sh(gl.VERTEX_SHADER,"attribute vec2 a;void main(){{gl_Position=vec4(a,0,1);}}"));gl.attachShader(P,sh(gl.FRAGMENT_SHADER,FS));gl.linkProgram(P);
if(!gl.getProgramParameter(P,gl.LINK_STATUS))return off();
gl.useProgram(P);gl.bindBuffer(gl.ARRAY_BUFFER,gl.createBuffer());gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);gl.enableVertexAttribArray(0);gl.vertexAttribPointer(0,2,gl.FLOAT,false,0,0);
const U={{}};["r","m","us","t","ld","k0","k1","k2"].forEach(k=>U[k]=gl.getUniformLocation(P,k));
const hex=s=>[1,3,5].map(i=>parseInt(s.slice(i,i+2),16)/255);
let fr=0,ready=!IMG,vis=true,raf=0,t0=performance.now(),mx=.5,my=.5,sx=.5,sy=.5,ld=0,ldT=0;
const pal=k=>{{k.split(",").forEach((c,i)=>gl.uniform3fv(U["k"+i],hex(c)));if(RM)draw()}};
if(IMG){{const im=root.querySelector("img"),tx=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,tx);
  [[gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE],[gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE],[gl.TEXTURE_MIN_FILTER,gl.LINEAR],[gl.TEXTURE_MAG_FILTER,gl.LINEAR]].forEach(p=>gl.texParameteri(gl.TEXTURE_2D,...p));
  const go=()=>{{try{{gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL,true);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGB,gl.RGB,gl.UNSIGNED_BYTE,im)}}catch(e){{return off()}}gl.uniform2f(U.us,im.naturalWidth,im.naturalHeight);ready=true;ldT=performance.now();loop()}};
  im.complete&&im.naturalWidth?go():(im.onload=go,im.onerror=off)}}
function size(){{const d=Math.min(devicePixelRatio||1,1.5)*{rs},w=Math.round(cv.clientWidth*d),h=Math.round(cv.clientHeight*d);if(cv.width!==w||cv.height!==h){{cv.width=w;cv.height=h;gl.viewport(0,0,w,h)}}gl.uniform2f(U.r,w,h)}}
function draw(){{if(!ready)return;size();const now=performance.now();sx+=(mx-sx)*.06;sy+=(my-sy)*.06;
  gl.uniform1f(U.t,RM?8:(now-t0)/1000);gl.uniform2f(U.m,sx,sy);gl.uniform1f(U.ld,IMG?Math.min(1,(now-ldT)/900):1);gl.drawArrays(gl.TRIANGLES,0,3)}}
function loop(){{cancelAnimationFrame(raf);if(RM){{draw();if(IMG&&performance.now()-ldT<1000)raf=requestAnimationFrame(loop);return}}if(!vis||document.hidden)return;if(fr++%{skip}===0)draw();raf=requestAnimationFrame(loop)}}
root.addEventListener("pointermove",e=>{{const b=root.getBoundingClientRect();mx=(e.clientX-b.left)/b.width;my=1-(e.clientY-b.top)/b.height}});
root.addEventListener("pointerleave",()=>{{mx=.5;my=.5}});
new IntersectionObserver(([e])=>{{vis=e.isIntersecting;loop()}}).observe(root);
document.addEventListener("visibilitychange",loop);
new ResizeObserver(()=>{{if(RM)draw()}}).observe(root);
root.querySelectorAll("[data-tg]").forEach(b=>b.addEventListener("click",()=>b.setAttribute("aria-pressed",b.getAttribute("aria-pressed")!=="true")));
root.querySelectorAll("[data-one]").forEach(b=>b.addEventListener("click",()=>b.parentNode.querySelectorAll("[data-one]").forEach(x=>x.setAttribute("aria-pressed",x===b))));
const btns=[...root.querySelectorAll("[data-k]")];
btns.forEach(b=>b.onclick=()=>{{btns.forEach(x=>x.setAttribute("aria-pressed",x===b));pal(b.dataset.k);const s=root.style;["ink","fb"].forEach(k=>b.dataset[k]?s.setProperty("--"+k,b.dataset[k]):s.removeProperty("--"+k))}});
pal({k0});loop();
}})();
</script>
"""

from bg_pages import P as PAGES
BG = []
def bg(id, name, desc, tags, eye, h1, sub, cta, pals, ink, fb, body, img=None, imgf="none", rs=1, skip=1):
    BG.append(dict(id=id, name=name, desc=desc, tags=tags, eye=eye, h1=h1, sub=sub, cta=cta, pals=pals, ink=ink, fb=fb, body=body, img=img, imgf=imgf, rs=rs, skip=skip))

# ---------- shaders (all define main) ----------
bg("felt-texture","Felt Texture","Pressed wool felt drawn in WebGL: thousands of tangled fibres, soft lumps and a light that follows the cursor across the nap.",["webgl","texture","background","felt"],
 "Background · Felt","Made soft,<br><em>on purpose.</em>","A tactile backdrop for products that want to feel handmade rather than rendered.","Browse the shop",
 [("Clay","#3a1d14,#8a4a32,#d49a76"),("Moss","#1f2a1c,#3d5236,#7f9668"),("Slate","#191c22,#363d4a,#7c8698")],"#f6ece4","#4a2418",r"""
float fib(vec2 p){float v=0.;for(int i=0;i<5;i++){float a=float(i)*1.256+.3;mat2 R=mat2(cos(a),sin(a),-sin(a),cos(a));v+=n(R*p*vec2(26.,2.2)+float(i)*7.);}return v/5.;}
float H(vec2 p){return fbm(p*2.2)*.55+fib(p*4.)*.35+n(p*90.)*.1;}
void main(){vec2 p=gl_FragCoord.xy/r.y;float e=1./r.y;
float c=H(p),dx=H(p+vec2(e*2.,0))-c,dy=H(p+vec2(0,e*2.))-c;vec3 N=normalize(vec3(-dx*60.,-dy*60.,1.));
vec3 L=normalize(vec3((m-.5)*vec2(2.4,2.)-(gl_FragCoord.xy/r-.5)*.8,.9));float d=max(dot(N,L),0.);
vec3 col=mix(k0,k1,smoothstep(.25,.7,c));col=mix(col,k2,smoothstep(.62,.95,c)*.5);col*=.62+.55*d;
col+=(h(gl_FragCoord.xy+fract(t))-.5)*.03;vec2 v=gl_FragCoord.xy/r-.5;col*=1.-.5*dot(v,v);gl_FragColor=vec4(col,1);}""")

bg("water-ripples","Water Ripples","Sunlit pool water seen from above: animated caustics, a sky-coloured surface and rings that spread wherever the cursor touches.",["webgl","water","caustics","background"],
 "Background · Water","Cool down<br><em>the whole page.</em>","Animated caustics that never loop visibly. Move across the water to stir it.","Plan a swim",
 [("Pool","#063a4f,#2a9bb4,#e9fbff"),("Lagoon","#043a33,#1fa58a,#f0fff6"),("Dusk","#1c1440,#5b4bb3,#ffe9d6")],"#ffffff","#0b4b5e",r"""
float caus(vec2 p,float T){vec2 i=p;float c=1.,inten=.005;for(int j=0;j<5;j++){float tt=T*(1.-(3.5/float(j+1)));i=p+vec2(cos(tt-i.x)+sin(tt+i.y),sin(tt-i.y)+cos(tt+i.x));c+=1./length(vec2(p.x/(sin(i.x+tt)/inten),p.y/(cos(i.y+tt)/inten)));}c/=5.;c=1.17-pow(c,1.4);return pow(abs(c),8.);}
void main(){vec2 uv=gl_FragCoord.xy/r,p=(gl_FragCoord.xy-.5*r)/r.y;vec2 mp=(m-.5)*vec2(r.x/r.y,1.);float d=length(p-mp);
p+=normalize(p-mp+1e-4)*sin(d*40.-t*5.)*.012*exp(-d*3.5);
float T=t*.35+23.;float c=caus(mod(p*5.,6.2831)-250.,T);
vec3 col=mix(k0,k1,.35+.45*uv.y+.2*fbm(p*2.+t*.05));col+=k2*clamp(c,0.,1.)*.55;col+=k2*smoothstep(.75,1.,fbm(p*3.-t*.08))*.08;
gl_FragColor=vec4(col,1);}""")

bg("speckled-graphite","Speckled Graphite","Dark graphite stone with mineral flecks at three sizes and a metallic sheen that slides as the cursor moves. Ideal behind dark product UI.",["webgl","stone","texture","background","dark"],
 "Background · Graphite","Built for<br><em>the dark mode.</em>","A quiet, heavy surface with just enough sparkle to stop it looking like a flat hex code.","Request access",
 [("Graphite","#121314,#2a2c2f,#c9ccd1"),("Basalt","#0f1112,#1d2a2a,#9fd3c6"),("Ink","#0c0d16,#1e2140,#b9c2ff")],"#eef0f2","#17181a",r"""
float sp(vec2 p,float sc,float th){vec2 c=floor(p*sc),f=fract(p*sc);vec2 o=h2(c);float k=h(c+3.1);float d=length(f-o);return step(th,k)*smoothstep(.22,.05,d)*(.4+.6*h(c+7.));}
void main(){vec2 uv=gl_FragCoord.xy/r,p=gl_FragCoord.xy/r.y;
float b=fbm(p*1.6)*.6+fbm(p*9.)*.25;vec3 col=mix(k0,k1,b);
float s=sp(p,180.,.86)*.55+sp(p,70.,.93)*.8+sp(p+.3,26.,.975);
float sheen=pow(max(0.,1.-abs(dot(uv-m,normalize(vec2(1,.6))))*1.8),6.);
col+=k2*s*(.25+.9*sheen+.1*sin(t*.8+h(floor(p*180.))*6.28));col+=k2*sheen*.06;
col+=(h(gl_FragCoord.xy+fract(t*7.))-.5)*.025;gl_FragColor=vec4(col,1);}""")

bg("grass-texture","Grass Texture","A dense lawn of individually drawn blades swaying in a wind field. The cursor parts the grass as it passes.",["webgl","nature","grass","background"],
 "Background · Grass","Touch grass,<br><em>digitally.</em>","Thousands of blades in layers of depth, one gentle breeze. Sweep the cursor through it.","Go outside",
 [("Spring","#0e2410,#3f8a2c,#c9ec7a"),("Summer","#1d2a0c,#7a8f23,#e9d77a"),("Frost","#0f1f22,#4f7f7a,#e6f4ef")],"#fbfff2","#2e5a24",r"""
void main(){vec2 p=gl_FragCoord.xy/r.y;float ar=r.x/r.y;vec3 col=k0*.5;float mx=m.x*ar;
for(int l=0;l<8;l++){float L=float(l);float yb=1.08-L*.16;float H=.34+L*.012;float k=(p.y-yb)/H;if(k<0.||k>1.)continue;
float d=90.-L*6.;float wind=(n(vec2(p.x*1.6+t*.4,L*3.))-.5)*.1+sin(t*1.3+p.x*3.+L)*.008;float dx=p.x-mx;float push=exp(-dx*dx*60.)*sign(dx)*.07*exp(-abs(p.y-m.y)*3.);
float x=p.x-k*k*(wind+push)+L*.37;float id=floor(x*d);float hr=.55+.45*h(vec2(id,L));float f=fract(x*d)-.5-(h(vec2(id,L+9.))-.5)*.5;
float kk=k/hr;float w=.42*(1.-kk);if(kk<1.&&abs(f)<w){float sh=.55+.45*L/7.;vec3 b=mix(k0,k1,.3+.5*kk)*mix(.8,1.15,h(vec2(id,L+3.)));b=mix(b,k2,pow(kk,3.)*.55);b*=sh*(.6+.4*kk);b*=.85+.3*smoothstep(0.,w,w-abs(f));col=b;}}
gl_FragColor=vec4(col,1);}""")

bg("dithered-image","Dithered Image","A photo rendered in two colours with an 8×8 Bayer ordered dither, the old-Mac way. The cursor opens a lens of real colour.",["webgl","dither","photo","retro","background"],
 "Background · Dither","Two colours.<br><em>Every detail.</em>","Ordered dithering turns any photo into a crisp two-tone print. Hover to see what it was.","See the archive",
 [("Paper","#1b1a17,#efe9dc,#efe9dc"),("Blueprint","#0d2a6b,#dfe8ff,#dfe8ff"),("Phosphor","#04140a,#5cff8a,#5cff8a")],"#1b1a17","#efe9dc",r"""
float b2(vec2 a){a=floor(a);return fract(a.x/2.+a.y*a.y*.75);}
float b8(vec2 a){return b2(.25*a)*.0625+b2(.5*a)*.25+b2(a);}
void main(){float px=3.;vec2 cell=floor(gl_FragCoord.xy/px)*px+px*.5;vec2 q=cover(cell/r);
float l=lum(img(q));l=clamp((l-.5)*1.25+.52,0.,1.);float d=step(b8(gl_FragCoord.xy/px)/1.33,l);
vec3 col=mix(k0,k1,d);vec2 a=(gl_FragCoord.xy/r-m)*vec2(r.x/r.y,1.);float lens=smoothstep(.16,.15,length(a));
col=mix(col,img(cover(gl_FragCoord.xy/r)),lens);col=mix(k1,col,ld);gl_FragColor=vec4(col,1);}""",
 img="media/pics/w/1036.jpg", imgf="grayscale(1) contrast(1.2)")

bg("paper-texture","Paper Texture","Heavy cotton paper with visible fibres, deckle grain and two soft folds, lit from the cursor so the surface catches the light.",["webgl","paper","texture","background","light"],
 "Background · Paper","Write it down<br><em>like it matters.</em>","A warm, printed-feeling surface for editorial pages, letters and invitations.","Read the letter",
 [("Cotton","#efe8da,#d9cfbb,#fffaf0"),("Kraft","#c9a47a,#a98257,#e8cba3"),("Night","#24252b,#1a1b20,#3a3c45","#ece6da","#24252b")],"#2a241c","#efe8da",r"""
float fib(vec2 p){float v=0.;for(int i=0;i<4;i++){float a=float(i)*1.7;mat2 R=mat2(cos(a),sin(a),-sin(a),cos(a));v+=n(R*p*vec2(60.,5.));}return v/4.;}
float H(vec2 p){float f=fbm(p*6.)*.5+fib(p*3.)*.3+n(p*260.)*.2;f+=.6*(1.-smoothstep(0.,.18,abs(p.x*.9-p.y*.15-.62)))*.5;f-=.5*(1.-smoothstep(0.,.25,abs(p.y-p.x*.08-.38)))*.4;return f;}
void main(){vec2 p=gl_FragCoord.xy/r.y;float e=1./r.y;float c=H(p);vec3 N=normalize(vec3(-(H(p+vec2(e,0))-c)*90.,-(H(p+vec2(0,e))-c)*90.,1.));
vec3 L=normalize(vec3((m-gl_FragCoord.xy/r)*1.6,.8));float d=dot(N,L);vec3 col=mix(k1,k0,.55+.45*fbm(p*3.));col*=.86+.22*d;col=mix(col,k2,smoothstep(.85,1.,d)*.25);
col+=(h(gl_FragCoord.xy)-.5)*.02;gl_FragColor=vec4(col,1);}""")

bg("cloud-sky","Cloud Sky","An endless drifting sky of soft cumulus, shaded towards a sun you move with the cursor. Never repeats.",["webgl","sky","clouds","background"],
 "Background · Sky","Head in<br><em>the clouds.</em>","Layered noise clouds lit from a sun that follows you. Calm enough to read over.","Start dreaming",
 [("Noon","#2f6fcf,#a9d1ff,#ffffff"),("Golden","#3b4d8f,#ffb27a,#fff3e2"),("Storm","#232a35,#6a7684,#d9dee5")],"#0c2340","#dcebff",r"""
float cl(vec2 p){float v=0.,a=.55;for(int i=0;i<6;i++){v+=a*n(p);p=mat2(.8,.6,-.6,.8)*p*2.1;a*=.5;}return v;}
void main(){vec2 uv=gl_FragCoord.xy/r,p=gl_FragCoord.xy/r.y;vec2 w=vec2(t*.025,0.);
vec3 sky=mix(k1,k0,pow(uv.y,.8));vec2 sun=m*vec2(r.x/r.y,1.);float sd=length(p-sun);sky+=k2*exp(-sd*5.)*.35;
float d=cl(p*1.6+w)+.35*cl(p*4.+w*2.)-.1;float cov=smoothstep(.48,.85,d+(uv.y-.5)*.15);
vec2 dir=normalize(sun-p+1e-4);float lit=clamp((d-(cl((p+dir*.04)*1.6+w)+.35*cl((p+dir*.04)*4.+w*2.)-.1))*4.+.6,0.,1.);
vec3 cc=mix(mix(k1,k0,.5)*.75,k2,lit);gl_FragColor=vec4(mix(sky,cc,cov),1);}""")

bg("lens-distortion","Lens Distortion","A photograph seen through drifting glass orbs. Each orb magnifies and bends the scene with a little chromatic fringe; one follows the cursor.",["webgl","lens","glass","photo","background"],
 "Background · Lens","Look closer.<br><em>It bends.</em>","Refracting glass orbs over a photo, with real barrel distortion and colour fringing on the rims.","Explore",
 [("Clear","#ffffff,#ffffff,#ffffff"),("Amber","#ffd6a8,#ffffff,#ffffff"),("Ice","#c9e9ff,#ffffff,#ffffff")],"#ffffff","#7a3a1c",r"""
vec2 orb(vec2 p,vec2 c,float R,inout float hit,inout float rim){vec2 d=p-c;float l=length(d);if(l<R){float k=l/R;hit=max(hit,1.);rim=max(rim,smoothstep(.75,1.,k));float z=sqrt(1.-k*k);return c+d*(.45+.55*k*k)-d*(1.-z)*.1;}return p;}
void main(){vec2 uv=gl_FragCoord.xy/r,a=vec2(r.x/r.y,1.);vec2 p=uv*a;float hit=0.,rim=0.;
vec2 q=p;q=orb(q,vec2(.28*a.x+.06*sin(t*.3),.62+.05*cos(t*.37)),.2,hit,rim);q=orb(q,vec2(.76*a.x+.05*cos(t*.25),.3+.06*sin(t*.31)),.15,hit,rim);q=orb(q,m*a,.17,hit,rim);
vec2 o=(q-p)*.06;vec3 col;col.r=img(cover((q+o)/a)).r;col.g=img(cover(q/a)).g;col.b=img(cover((q-o)/a)).b;
col*=mix(1.,1.08,hit);col=mix(col,k0,rim*.18);col+=pow(rim,6.)*.25;col=mix(vec3(.12),col,ld);gl_FragColor=vec4(col,1);}""",
 img="media/pics/w/564.jpg")

bg("stippled-gradient","Stippled Gradient","A slow, domain-warped gradient rendered as ink stipple on paper: every dot sized by the tone underneath, like a pen-and-ink engraving that moves.",["webgl","stipple","gradient","print","background"],
 "Background · Stipple","Gradients,<br><em>by hand.</em>","Thousands of jittered dots replace the smooth blend. It reads as print, not pixels.","Get the print",
 [("Ink","#f1ece1,#1c1b2e,#b8361f"),("Riso","#f4efe4,#2a49c9,#ff5b7a"),("Night","#121318,#e9e4d6,#e2a33a","#e9e4d6","#121318")],"#1c1b2e","#f1ece1",r"""
void main(){vec2 p=(gl_FragCoord.xy-.5*r)/r.y;float sz=4.;vec2 g=floor(gl_FragCoord.xy/sz);vec2 f=fract(gl_FragCoord.xy/sz);
vec2 cp=(g+.5)*sz;vec2 cq=(cp-.5*r)/r.y+(m-.5)*.15;float T=t*.05;vec2 w=vec2(fbm(cq*1.3+T),fbm(cq*1.3+4.-T));float v=fbm(cq*1.2+2.5*w);
float tone=smoothstep(.25,.75,v);vec2 o=h2(g)*.5+.25;float rad=.62*sqrt(tone)*(.75+.5*h(g+9.));float dot_=smoothstep(rad,rad-.12,length(f-o));
vec3 ink=mix(k1,k2,smoothstep(.45,.9,length(w)));gl_FragColor=vec4(mix(k0,ink,dot_),1);}""")

bg("square-dot-grid","Square Dot Grid","A field of tiny squares whose size follows interfering waves and a slow noise swell. They bloom and tint around the cursor.",["webgl","grid","dots","background","generative"],
 "Background · Grid","Order,<br><em>with a pulse.</em>","A strict square grid that breathes. Precise enough for dev tools, alive enough for a launch.","Read the docs",
 [("Mono","#0b0b0c,#4a4a52,#ff5a1f"),("Paper","#f3f1ea,#b9b5a8,#1d4ed8","#111114","#f3f1ea"),("Matrix","#050a07,#1d4a2c,#5cff8a")],"#f4f3ef","#0b0b0c",r"""
void main(){float sz=14.;vec2 g=floor(gl_FragCoord.xy/sz),f=fract(gl_FragCoord.xy/sz)-.5;vec2 c=(g+.5)*sz/r.y;vec2 mp=m*vec2(r.x/r.y,1.);float dm=length(c-mp);
float w=.5+.25*sin(length(c-vec2(.2,.3))*14.-t*1.2)+.25*sin(c.x*6.+c.y*4.+t*.7);w=w*.6+.4*fbm(c*2.+t*.05);float near=exp(-dm*dm*18.);
float s=mix(.06,.42,clamp(w*.8+near*.7,0.,1.));vec2 q=abs(f)-s;float box=1.-smoothstep(0.,.08,max(q.x,q.y));
vec3 col=mix(k0,mix(k1,k2,near*.9),box);gl_FragColor=vec4(col,1);}""")

bg("iridescent-shapes","Iridescent Shapes","Raymarched glossy shapes with a thin-film coating: colours shift through cyan, magenta and gold as the forms turn and as the cursor tilts them.",["webgl","3d","iridescent","raymarch","background"],
 "Background · Iridescent","Thin film,<br><em>thick impact.</em>","A soap-bubble coating on slowly orbiting forms. Tilt them with the cursor.","Shop the drop",
 [("Pearl","#eceae6,#c9c6c0,#ffffff"),("Onyx","#0d0d10,#26262c,#ffffff","#f4f3ef","#0d0d10"),("Blush","#f3e3e3,#d9b9bd,#ffffff")],"#141416","#eceae6",r"""
mat2 rot(float a){return mat2(cos(a),sin(a),-sin(a),cos(a));}
float smin(float a,float b,float k){float hh=clamp(.5+.5*(b-a)/k,0.,1.);return mix(b,a,hh)-k*hh*(1.-hh);}
float map(vec3 p){p.xz*=rot(t*.25+(m.x-.5)*1.5);p.yz*=rot(.5+(m.y-.5)*1.2);vec3 q=p;q.xy*=rot(t*.2);
float tor=length(vec2(length(q.xz)-1.,q.y))-.32;float s1=length(p-vec3(sin(t*.5)*1.1,.5,cos(t*.4)*.6))-.38;float s2=length(p+vec3(cos(t*.37)*.9,.6,sin(t*.41)*.5))-.28;return smin(tor,smin(s1,s2,.4),.45);}
vec3 film(float x){return .5+.5*cos(6.2831*(x+vec3(0.,.33,.67)));}
void main(){vec2 p=(gl_FragCoord.xy-.5*r)/r.y;p.x-=clamp((r.x/r.y-1.)*.55,0.,.6);p.y+=r.x<r.y?-.25:0.;vec3 ro=vec3(0,0,4.2),rd=normalize(vec3(p,-1.6));float d=0.,hit=0.;
for(int i=0;i<72;i++){float s=map(ro+rd*d);if(s<.002){hit=1.;break;}d+=s;if(d>9.)break;}
vec3 bgc=mix(k1,k0,smoothstep(-.6,.6,p.y+.2));vec3 col=bgc;
if(hit>0.){vec3 P=ro+rd*d;vec2 e=vec2(.002,0);vec3 N=normalize(vec3(map(P+e.xyy)-map(P-e.xyy),map(P+e.yxy)-map(P-e.yxy),map(P+e.yyx)-map(P-e.yyx)));
float fr=pow(1.-max(dot(N,-rd),0.),2.);vec3 R=reflect(rd,N);vec3 ir=mix(vec3(.93,.92,.95),film(dot(N,-rd)*1.1+R.y*.25+t*.03),.38);
col=mix(ir*mix(.62,.95,.5+.5*N.y),k2,smoothstep(.6,1.,R.y)*.5)+fr*film(fr*.8+.2)*.22;col+=pow(max(dot(R,normalize(vec3(.5,.8,.6))),0.),40.)*.9;col=mix(col,bgc,.08);}
gl_FragColor=vec4(col,1);}""")

bg("impressionist-painting","Impressionist Painting","A landscape photo repainted live as thick oil brush strokes: each dab takes its colour from the scene, oriented along the image's edges, and slowly shimmers.",["webgl","painterly","photo","brush","background"],
 "Background · Painting","Every page<br><em>a canvas.</em>","Directional brush strokes rebuilt from a photo in real time. No AI filter, just a shader.","Enter the gallery",
 [("Oil","#000000,#000000,#000000")],"#ffffff","#3d5a2b",r"""
void main(){vec2 px=gl_FragCoord.xy,uv=px/r;vec2 p=px/r.y;
float a=fbm(p*2.2+t*.015)*6.2831;vec2 dir=vec2(cos(a),sin(a));vec2 cell=floor(p*38.+dir*2.);float jit=h(cell);
vec3 acc=vec3(0);for(int i=-3;i<=3;i++){float f=float(i)/3.;acc+=img(cover(uv+dir*f*.018*vec2(r.y/r.x,1.)+(jit-.5)*.004));}acc/=7.;
acc=mix(vec3(lum(acc)),acc,1.35);acc=floor(acc*7.+jit*.6)/7.;
vec2 rd=mat2(dir.x,-dir.y,dir.y,dir.x)*p;float bristle=n(vec2(rd.x*8.,rd.y*160.));float dab=n(p*38.+jit*9.);
vec3 col=acc*(.86+.22*bristle)*(.95+.1*dab);col+=(n(px*.9)-.5)*.04;
col=mix(vec3(.85,.82,.75),col,ld);gl_FragColor=vec4(col,1);}""",
 img="media/pics/w/1039.jpg", imgf="saturate(1.3) contrast(1.05)", rs=.75, skip=2)

bg("single-hue-landscape","Single-Hue Landscape","A landscape photo remapped into one hue, from deep shadow to pale highlight, with a slow parallax drift. Pick the hue from the switcher.",["webgl","duotone","photo","landscape","background"],
 "Background · Landscape","One colour,<br><em>whole world.</em>","Monochrome landscapes keep the drama of a photo without fighting your brand colour.","Plan the trip",
 [("Sage","#0f1d14,#5f8a68,#e7f2e4"),("Terracotta","#2a0f08,#b5532f,#ffe6d6"),("Cobalt","#060d2a,#2c4fc4,#e3eaff")],"#ffffff","#2f4a36",r"""
void main(){vec2 uv=gl_FragCoord.xy/r;vec2 q=cover((uv-.5)*.94+.5+(m-.5)*.03+vec2(sin(t*.05),cos(t*.04))*.008);float l=lum(img(q));l=smoothstep(.05,.95,l);
vec3 col=l<.5?mix(k0,k1,l*2.):mix(k1,k2,(l-.5)*2.);col+=(h(gl_FragCoord.xy+fract(t))-.5)*.05;col*=1.-.35*pow(length(uv-.5),2.);col=mix(k0,col,ld);gl_FragColor=vec4(col,1);}""",
 img="media/pics/w/1018.jpg", imgf="grayscale(1)")

def render(b):
    c = "bg-" + "".join(w[0] for w in b["id"].split("-")) + "x"
    pg = PAGES[b["id"]]
    pals = [tuple(x) + (None,) * (4 - len(x)) for x in b["pals"]]
    pal = "" if len(pals) < 2 else "<div class=\"%s-pal\" role=\"group\" aria-label=\"Colour\">%s</div>" % (c, "".join(
        '<button type="button" aria-pressed="%s" data-k="%s"%s style="--g:linear-gradient(135deg,%s,%s)" aria-label="%s"><i></i></button>' % (
            "true" if i == 0 else "false", k, (' data-ink="%s" data-fb="%s"' % (ink, fb)) if ink else "", k.split(",")[0], k.split(",")[1], nm) for i, (nm, k, ink, fb) in enumerate(pals)))
    return SHELL.format(c=c, fb=b["fb"], ink=b["ink"], imgf=b["imgf"], imgtag=('  <img src="%s" alt="" crossorigin="anonymous">\n' % b["img"]) if b["img"] else "",
        brand=pg[0], links="".join('<a href="#">%s</a>' % l for l in pg[1]), pcss=pg[2].replace("$", c), phtml=pg[3].replace("$", c), pal=pal, imgjs="true" if b["img"] else "false",
        fs=json.dumps(COMMON + b["body"]), rs=b["rs"], skip=b["skip"], k0=json.dumps(pals[0][1]))

if __name__ == "__main__":
    import sys
    for b in BG:
        open(os.path.join(D, b["id"] + ".html"), "w").write(render(b))
    if "--reg" in sys.argv:
        for b in BG:
            print("  " + json.dumps([b["id"], b["name"], "Backgrounds", b["desc"], b["tags"], 1], ensure_ascii=False) + ",")
    print(" ".join(b["id"] for b in BG), file=sys.stderr)
