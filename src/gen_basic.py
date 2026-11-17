#!/usr/bin/env python3
"""Ordinary components. src/basic/<id>.html: line 1 <!--Name|Category|Description|tags-->, then markup + <style> + <script>.
Root element must be <div class="k" …>. @I(name[,size]) icons come from gen_mobile. Run: python3 src/gen_basic.py [ids] [--reg]"""
import re, sys, json, pathlib, subprocess
sys.path.insert(0, '/root/kiln/src'); from gen_mobile import icon
ROOT = pathlib.Path('/root/kiln'); SRC = ROOT / 'src/basic'
BASE = r'''@TOKENS(.k)
.k{min-height:100vh;min-height:100dvh;display:grid;place-items:center;padding:48px 16px;background:var(--sf);font-size:14px}
.k :where(button,input,select,textarea){font:inherit;color:inherit}
.k :where(button){cursor:pointer;background:none;border:0;padding:0}
.k [hidden]{display:none!important}
.k .i{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}
.k .card{background:var(--bg);border:1px solid var(--line);border-radius:16px;box-shadow:var(--shadow)}
.k .b{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:40px;padding:0 16px;border-radius:10px;border:1px solid transparent;font-size:14px;font-weight:550;background:var(--fg);color:var(--bg);white-space:nowrap;transition:background .15s,border-color .15s,transform .1s}
.k .b:active{transform:translateY(1px)}.k .b:disabled{opacity:.45;cursor:not-allowed}
.k .b.sec{background:var(--bg);color:var(--fg);border-color:var(--line)}.k .b.sec:hover{background:var(--sf)}
.k .b.ac{background:var(--ac);color:var(--ac-fg)}.k .b.ac:hover{background:var(--ac-h)}
.k .b.gh{background:none;color:var(--fg)}.k .b.gh:hover{background:var(--sf)}
.k .b.sm{height:32px;padding:0 12px;font-size:13px;border-radius:8px}
.k .ibt{width:32px;height:32px;border-radius:8px;display:inline-grid;place-items:center;color:var(--mu);transition:background .15s,color .15s}.k .ibt:hover{background:var(--sf);color:var(--fg)}
.k .av{width:40px;height:40px;border-radius:50%;flex:none;display:grid;place-items:center;font-weight:600;color:#fff;background:var(--c,#6b7280)}
.k .mu{color:var(--mu)}.k .tn{font-variant-numeric:tabular-nums}
.k .vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.k .in{height:40px;width:100%;padding:0 12px;border-radius:10px;border:1px solid var(--ctl);background:var(--bg);font-size:14px;outline:0;transition:border-color .15s,box-shadow .15s}
.k .in:focus{border-color:var(--ac);box-shadow:0 0 0 3px color-mix(in srgb,var(--ac) 20%,transparent)}
.k .in[aria-invalid=true]{border-color:var(--err)}
.k .lbl{display:block;margin-bottom:6px;font-size:13px;font-weight:550}
.k .pill{display:inline-flex;align-items:center;gap:4px;height:22px;padding:0 8px;border-radius:11px;font-size:12px;font-weight:600;background:var(--sf2);color:var(--mu)}
.k .pill.ok{background:var(--ok-sf);color:var(--ok)}.k .pill.warn{background:var(--warn-sf);color:var(--warn)}.k .pill.err{background:var(--err-sf);color:var(--err)}.k .pill.info{background:var(--info-sf);color:var(--info)}
'''
PG = r'''
.k.pg{display:block;place-items:normal;padding:0;background:var(--bg);font-size:16px;min-height:0}
.pg .w{width:min(1180px,100% - 32px);margin-inline:auto;min-width:0}
.pg{overflow-x:clip}
.pg img{display:block;max-width:100%}
.pg h1,.pg h2,.pg h3,.pg p{margin:0}
.pg .ser{font-family:'Instrument Serif',Georgia,serif;font-weight:400;letter-spacing:-.01em}
.pg .h1{font-size:clamp(40px,7vw,84px);line-height:1;letter-spacing:-.035em;font-weight:650;text-wrap:balance}
.pg .h2{font-size:clamp(30px,4.4vw,52px);line-height:1.05;letter-spacing:-.03em;font-weight:620;text-wrap:balance}
.pg .h3{font-size:19px;line-height:1.3;font-weight:620;letter-spacing:-.01em}
.pg .lead{font-size:clamp(17px,1.6vw,20px);line-height:1.5;color:var(--mu);text-wrap:pretty;max-width:60ch}
.pg .eb{font:500 12px/1 'Geist Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--mu)}
.pg .sec{padding:clamp(64px,10vw,128px) 0}
.pg .b.lg{height:48px;padding:0 22px;font-size:15px;border-radius:12px}
.pg .ph{width:100%;height:100%;object-fit:cover}
.pg .top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.pg .top .w{display:flex;align-items:center;gap:24px;height:64px}
.pg .logo{white-space:nowrap;font-weight:700;letter-spacing:-.02em;font-size:17px;display:flex;align-items:center;gap:8px;color:inherit;text-decoration:none}
.pg .links{display:flex;gap:24px;margin-left:auto;font-size:14px}.pg .links a{color:var(--mu);text-decoration:none}.pg .links a:hover{color:var(--fg)}
.pg .menu{display:none;margin-left:auto;width:44px;height:44px;place-items:center;border-radius:10px}
.pg .foot{border-top:1px solid var(--line);padding:32px 0;font-size:13px;color:var(--mu)}.pg .foot .w{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
@media (max-width:760px){.pg .links{display:none;position:absolute;top:64px;left:0;right:0;flex-direction:column;gap:0;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 16px}.pg .links a{padding:12px 0;font-size:16px}.pg .top.open .links{display:flex}.pg .menu{display:grid}.pg .top .b{display:none}}
'''
DB = r'''
.k.db{display:grid;grid-template-columns:232px 1fr;padding:0;place-items:stretch;background:var(--sf);min-height:100dvh;font-size:14px}
.db-side{background:var(--bg);border-right:1px solid var(--line);padding:16px 12px;display:flex;flex-direction:column;gap:2px;position:sticky;top:0;height:100dvh;overflow:auto}
.db-brand{display:flex;gap:10px;align-items:center;font-weight:700;padding:6px 8px 18px;font-size:15px}.db-brand i{width:28px;height:28px;border-radius:8px;background:var(--fg);color:var(--bg);display:grid;place-items:center;font-style:normal;font-size:13px}
.db-side a{display:flex;gap:10px;align-items:center;height:36px;padding:0 10px;border-radius:8px;color:var(--mu);text-decoration:none;font-weight:500}.db-side a:hover{background:var(--sf);color:var(--fg)}.db-side a[aria-current=page]{background:var(--sf2);color:var(--fg)}.db-side a em{margin-left:auto;font-style:normal;font-size:11px;font-weight:650;background:var(--sf2);border-radius:999px;padding:1px 7px}
.db-side .db-sec{font-size:11px;font-weight:600;color:var(--mu);text-transform:uppercase;letter-spacing:.06em;padding:16px 10px 6px}
.db-user{margin-top:auto;display:flex;gap:10px;align-items:center;padding:10px 8px;border-top:1px solid var(--line)}.db-user .av{width:32px;height:32px;font-size:12px}.db-user div{display:grid;font-size:13px;min-width:0}.db-user span{color:var(--mu);font-size:12px;overflow:hidden;text-overflow:ellipsis}
.db-main{min-width:0;display:flex;flex-direction:column;overflow-x:clip}
.db-top{display:flex;align-items:center;gap:12px;height:60px;padding:0 24px;border-bottom:1px solid var(--line);background:var(--bg);position:sticky;top:0;z-index:5}.db-top h1{font-size:17px;margin:0;font-weight:650;letter-spacing:-.01em}.db-top .sp{flex:1}
.k .db-mb{display:none}
.db-body{padding:24px;display:grid;gap:16px;align-content:start}
.db-kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.db-kpi{background:var(--bg);border:1px solid var(--line);border-radius:14px;padding:16px;display:grid;gap:4px}.db-kpi span{color:var(--mu);font-size:13px}.db-kpi b{font-size:26px;letter-spacing:-.02em;font-variant-numeric:tabular-nums}.db-kpi small{font-size:12px;font-weight:600}.db-up{color:var(--ok)}.db-dn{color:var(--err)}
.db-card{background:var(--bg);border:1px solid var(--line);border-radius:14px;padding:18px;min-width:0}.db-card>h2,.db-ch h2{margin:0;font-size:15px;font-weight:650}.db-ch{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:14px}
.db-tbl{width:100%;border-collapse:collapse;font-size:13.5px}.db-tbl th{text-align:left;font-weight:550;color:var(--mu);font-size:12px;padding:8px 10px;border-bottom:1px solid var(--line);white-space:nowrap}.db-tbl td{padding:10px;border-bottom:1px solid var(--line);vertical-align:middle}.db-tbl tr:last-child td{border-bottom:0}.db-tbl tbody tr:hover{background:var(--sf)}.db-tw{overflow-x:auto;position:relative}
@media (max-width:900px){.k.db{grid-template-columns:1fr}.db-side{position:fixed;inset:0 auto 0 0;width:260px;z-index:30;transform:translateX(-100%);transition:transform .25s var(--ease);box-shadow:var(--shadow)}.k.db.nav .db-side{transform:none}.k .db-mb{display:grid}.db-kpis{grid-template-columns:1fr 1fr}.db-body{padding:16px}.db-top{padding:0 12px 0 4px}}
'''
DBJS = "document.querySelectorAll('.db-mb').forEach(b=>b.addEventListener('click',()=>{const k=b.closest('.k');const o=k.classList.toggle('nav');b.setAttribute('aria-expanded',o)}));document.addEventListener('click',e=>{const k=document.querySelector('.k.db.nav');if(k&&!e.target.closest('.db-side,.db-mb'))k.classList.remove('nav')});"
PGJS = "document.querySelectorAll('.pg .menu').forEach(m=>m.addEventListener('click',()=>{const t=m.closest('.top');const o=t.classList.toggle('open');m.setAttribute('aria-expanded',o)}));"
def unpack():
    for p in sorted((ROOT / 'src/packs').glob('*.txt')):
        for blk in re.split(r'^=== ', p.read_text(), flags=re.M)[1:]:
            id_, body = blk.split('\n', 1); (SRC / f'{id_.strip()}.html').write_text(body.rstrip() + '\n')
PACK_IDS = {l[4:].strip() for f in (ROOT / 'src/packs').glob('*.txt') for l in f.read_text().splitlines() if l.startswith('=== ')}
NEWCSS = '.k .card{box-shadow:0 1px 2px color-mix(in srgb,var(--fg) 7%,transparent)}\n'
def build(id_):
    src = (SRC / f'{id_}.html').read_text(); head, body = src.split('\n', 1)
    name, cat, desc, tags = re.match(r'<!--(.*?)\|(.*?)\|(.*?)\|(.*?)-->', head).groups()
    css = '\n'.join(re.findall(r'<style>([\s\S]*?)</style>', body)).strip()
    js = '\n'.join(re.findall(r'<script>([\s\S]*?)</script>', body)).strip()
    body = re.sub(r'<(style|script)>[\s\S]*?</\1>', '', body).strip()
    body = re.sub(r'@I\((\w+)(?:,(\d+))?\)', lambda m: icon(m.group(1), m.group(2)), body)
    f = ROOT / 'components' / f'{id_}.html'
    if id_ in PACK_IDS: css = NEWCSS + css
    js = re.sub(r'@I\((\w+)(?:,(\d+))?\)', lambda m: icon(m.group(1), m.group(2)), js)
    if 'class="k db' in body: css = DB + css; js = (DBJS + '\n' + js).strip()
    pg = 'class="k pg' in body
    if pg: css = PG + css; js = (PGJS + '\n' + js).strip() if 'class="menu' in body else js
    f.write_text(f'<style>\n{BASE}\n{css}\n</style>\n{body}\n' + (f'<script>\n{js}\n</script>\n' if js else ''))
    subprocess.run(['python3', str(ROOT / 'src/tokens.py'), str(f)], check=True)
    return [id_, name, cat, desc, [t.strip() for t in tags.split(',')], 1]
if __name__ == '__main__':
    if '--packs' in sys.argv: unpack()
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    E = [build(i) for i in (args or sorted(p.stem for p in SRC.glob('*.html')))]
    print('built', len(E))
    if '--reg' in sys.argv:
        for e in E: print('  ' + json.dumps(e, ensure_ascii=False) + ',')
