# Shared "Kiln Core" tokens injected into every core component at the @TOKENS(selector) marker.
# Contrast (checked): fg/bg > 15:1, muted text >= 6:1 both themes, control borders (--ctl) >= 3:1 (WCAG 1.4.11),
# accent text >= 4.5:1, focus ring >= 3:1 against bg in both themes.
import re,sys,pathlib
T='''SEL{color-scheme:light dark;--bg:light-dark(#ffffff,#0f0f11);--sf:light-dark(#f6f6f4,#18181b);--sf2:light-dark(#ececea,#26262b);--fg:light-dark(#18181b,#f4f4f5);--mu:light-dark(#5b5b66,#a1a1aa);--line:light-dark(#e4e4e1,#2a2a2f);--ctl:light-dark(#8a8a94,#71717a);--ac:light-dark(#c2410c,#ff8a4c);--ac-h:light-dark(#9a3412,#ffa36e);--ac-fg:light-dark(#ffffff,#1a0a03);--ac-sf:light-dark(#fff1e8,#2a1409);--focus:light-dark(#1d4ed8,#93c5fd);--ok:light-dark(#15803d,#4ade80);--ok-sf:light-dark(#ecfdf3,#0b2a17);--warn:light-dark(#a16207,#facc15);--warn-sf:light-dark(#fefce8,#2a2306);--err:light-dark(#b91c1c,#f87171);--err-sf:light-dark(#fef2f2,#2c1010);--info:light-dark(#1d4ed8,#93c5fd);--info-sf:light-dark(#eff6ff,#0f1b33);--shadow:light-dark(0 1px 2px #0000000d\\,0 8px 24px -8px #00000026,0 1px 2px #0006\\,0 12px 32px -8px #000a);--r1:6px;--r2:10px;--r3:14px;--ease:cubic-bezier(.2,.8,.2,1);font:16px/1.5 Geist,system-ui,sans-serif;color:var(--fg);background:var(--bg);-webkit-font-smoothing:antialiased}
SEL :focus-visible{outline:2px solid var(--focus);outline-offset:2px}
SEL ::selection{background:var(--ac);color:var(--ac-fg)}
@media (prefers-reduced-motion:reduce){SEL *,SEL *::before,SEL *::after{animation-duration:.01ms!important;transition-duration:.01ms!important}}'''
T=T.replace('\\\\,',',')
for f in sys.argv[1:]:
    p=pathlib.Path(f);s=p.read_text()
    s=re.sub(r'@TOKENS\(([^)]+)\)',lambda m:T.replace('SEL',m.group(1)),s);p.write_text(s)
