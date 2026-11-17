#!/usr/bin/env python3
"""Email templates: table layout, 600px, system fonts, bulletproof buttons, dark-mode media query.
Classes are used for readability in the library; run the HTML through an inliner (juice, premailer) before sending.
Run: python3 src/gen_email.py [ids] [--reg]"""
import sys, json, pathlib
ROOT = pathlib.Path('/root/kiln')
CSS = '''
.em-bg{background:#eeede9;padding:32px 12px;min-height:100vh;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:#1c1c1a}
.em-bg table{border-collapse:collapse}.em-bg img{border:0;display:block}
.em-w{width:100%;max-width:600px;margin:0 auto}
.em-pre{display:none;max-height:0;overflow:hidden;opacity:0}
.em-hd td{padding:8px 4px 20px;font-size:15px;font-weight:700;letter-spacing:-.01em}.em-hd .mk{display:inline-block;width:22px;height:22px;border-radius:6px;background:var(--a);vertical-align:-5px;margin-right:8px}
.em-c{background:#ffffff;border-radius:12px}.em-c>tbody>tr>td{padding:36px 40px}
.em-c h1{margin:0 0 14px;font-size:24px;line-height:1.25;letter-spacing:-.02em;font-weight:700;color:#1c1c1a}
.em-c p{margin:0 0 14px;font-size:15px;line-height:1.6;color:#3a3a37}.em-c .mu{color:#6b6b66;font-size:13px}
.em-btn td{border-radius:8px;background:var(--a)}.em-btn a{display:inline-block;padding:13px 22px;font-size:15px;font-weight:600;color:#fff;text-decoration:none;border-radius:8px}
.em-hr{border-top:1px solid #e7e6e1;height:1px;line-height:1px;font-size:0;margin:24px 0}
.em-ft td{padding:20px 8px;font-size:12px;line-height:1.6;color:#7a7a74;text-align:center}.em-ft a{color:#7a7a74}
.em-tb{width:100%;font-size:14px}.em-tb td{padding:10px 0;border-bottom:1px solid #eeede9;color:#3a3a37}.em-tb td.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}.em-tb tr.tot td{font-weight:700;color:#1c1c1a;border-bottom:0;padding-top:14px}
.em-code{font:600 32px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.3em;padding:18px 0;text-align:center;background:#f4f3ef;border-radius:8px;color:#1c1c1a}
.em-box{background:#f4f3ef;border-radius:8px;padding:16px 18px}
.em-a{color:var(--a)}
@media (max-width:620px){.em-c>tbody>tr>td{padding:28px 22px!important}.em-c h1{font-size:21px!important}.em-st td{display:block!important;width:100%!important}}
@media (prefers-color-scheme:dark){.em-bg{background:#121211!important;color:#ecebe6}.em-c{background:#1d1d1b!important}.em-c h1{color:#f2f1ec!important}.em-c p,.em-tb td{color:#c9c8c2!important}.em-c .mu,.em-ft td,.em-ft a{color:#97968f!important}.em-hr{border-color:#33332f!important}.em-tb td{border-color:#2c2c29!important}.em-tb tr.tot td{color:#f2f1ec!important}.em-code,.em-box{background:#262623!important;color:#f2f1ec!important}.em-hd td{color:#ecebe6}}
'''
import random
def _qr(n=25,seed=7):
    r=random.Random(seed);c=[]
    fin=lambda x,y:(x<7 and y<7) or (x>n-8 and y<7) or (x<7 and y>n-8)
    for y in range(n):
        for x in range(n):
            if fin(x,y):
                lx,ly=x%(n-7) if x>n-8 else x,y%(n-7) if y>n-8 else y
                on=lx in(0,6) or ly in(0,6) or (2<=lx<=4 and 2<=ly<=4)
            else: on=r.random()>.5 and not (x<8 and y<8) and not (x>n-9 and y<8) and not (x<8 and y>n-9)
            if on:c.append(f'M{x} {y}h1v1h-1z')
    return f'<svg width="120" height="120" viewBox="0 0 {n} {n}" style="display:block" role="img" aria-label="Ticket QR code"><rect width="{n}" height="{n}" fill="#fff"/><path d="{"".join(c)}" fill="#1c1c1a"/></svg>'
QR=_qr()
def btn(t, href='#'):
    return f'<table role="presentation" class="em-btn"><tr><td><a href="{href}">{t}</a></td></tr></table>'
HR = '<div class="em-hr"></div>'
def shell(brand, accent, pre, body, foot):
    return (f'<div class="em-bg" style="--a:{accent}"><div class="em-pre">{pre}</div><table role="presentation" class="em-w" width="600" align="center">'
            f'<tr><td><table role="presentation" class="em-hd" width="100%"><tr><td><span class="mk"></span>{brand}</td></tr></table></td></tr>'
            f'<tr><td><table role="presentation" class="em-c" width="100%"><tr><td>{body}</td></tr></table></td></tr>'
            f'<tr><td><table role="presentation" class="em-ft" width="100%"><tr><td>{foot}</td></tr></table></td></tr></table></div>')
FOOT = lambda who, why: f'{who}<br>{why} <a href="#">Email preferences</a> · <a href="#">Unsubscribe</a>'
def items(rows, total):
    return '<table role="presentation" class="em-tb">' + ''.join(f'<tr><td>{a}</td><td class="r">{b}</td></tr>' for a, b in rows) + f'<tr class="tot"><td>{total[0]}</td><td class="r">{total[1]}</td></tr></table>'

E = [
 ('mail-welcome', 'Welcome Email', 'A welcome email that gets someone to their first useful moment: one clear next step, three short setup tasks with time estimates, and a reply-to-a-human line.', ['email', 'welcome', 'onboarding'],
  shell('Ledgerly', '#166534', 'Your account is ready. One thing to do first.',
   '<h1>Welcome, Mira. Your pots are ready.</h1><p>Most people start by connecting their salary account, so Ledgerly can split the next payday for you. It takes about two minutes.</p>' + btn('Connect my salary account') + HR +
   '<p><b>Then, when you have a moment</b></p><table role="presentation" class="em-tb"><tr><td>1. Name your first savings pot</td><td class="r">30 s</td></tr><tr><td>2. Order your physical card</td><td class="r">1 min</td></tr><tr><td>3. Turn on spending alerts</td><td class="r">20 s</td></tr></table>' +
   '<p style="margin-top:20px">Questions? Reply to this email. A person on our team reads every one.</p><p class="mu">Ines, customer support</p>',
   FOOT('Ledgerly Bank, 12 Harbour St, Dublin', 'You get this because you opened an account.'))),
 ('mail-receipt', 'Receipt Email', 'A transactional receipt: order number, itemised lines with VAT, payment method, billing address and an invoice PDF link, readable in light and dark mail clients.', ['email', 'receipt', 'transactional', 'invoice'],
  shell('Mossware', '#4d7c0f', 'Receipt for order #A-20419, €118.90',
   '<p class="mu">Order #A-20419 · 13 November 2026</p><h1>Thanks for your order</h1><p>Here is your receipt. We\'ll send tracking when it ships, usually within one working day.</p>' +
   items([('Stoneware mug, Moss × 2', '€48.00'), ('Linen apron, Rust × 1', '€62.00'), ('Shipping, tracked', '€8.90'), ('Of which VAT (21%)', '€20.64')], ('Total paid', '€118.90')) + HR +
   '<table role="presentation" width="100%" class="em-st"><tr><td width="50%" style="vertical-align:top;padding-bottom:12px"><p class="mu" style="margin:0 0 4px">Paid with</p><p style="margin:0">Visa ending 4242</p></td><td style="vertical-align:top"><p class="mu" style="margin:0 0 4px">Ships to</p><p style="margin:0">Ana Novak<br>Keizersgracht 210<br>1016 DZ Amsterdam</p></td></tr></table><p style="margin-top:20px"><a class="em-a" href="#">Download invoice (PDF)</a></p>',
   FOOT('Mossware, Rapenburg 8, Leiden', 'Receipts are sent for every order.'))),
 ('mail-reset', 'Password Reset Email', 'A password reset email with the button, expiry time, the device and location that asked, and a clear “this wasn\'t me” path.', ['email', 'password', 'reset', 'security'],
  shell('Quill', '#4338ca', 'Reset link, valid for 30 minutes.',
   '<h1>Reset your password</h1><p>Someone asked to reset the password for <b>lena@studio.example</b>. If it was you, use the button below. The link works once and expires in 30 minutes.</p>' + btn('Choose a new password') +
   '<div class="em-box" style="margin-top:24px"><p class="mu" style="margin:0 0 4px">Requested from</p><p style="margin:0">Chrome on macOS · Hamburg, Germany · 14:32 CET</p></div><p style="margin-top:20px">Didn\'t ask for this? You can ignore this email, your password won\'t change. If you keep getting these, <a class="em-a" href="#">secure your account</a>.</p>',
   'Quill Software GmbH, Hamburg<br>This is a security email, you can\'t unsubscribe from it.')),
 ('mail-digest', 'Weekly Digest Email', 'A weekly activity digest: a headline number with the change, three highlights with small inline bars, and items waiting on you, kept short enough to read on a phone.', ['email', 'digest', 'weekly', 'summary'],
  shell('Tally', '#2563eb', '8,214 visitors this week, up 12%.',
   '<p class="mu">Week of 3–9 November · example.com</p><h1>8,214 visitors, up 12%</h1><p>Your best week since August, mostly thanks to one blog post.</p>' +
   '<table role="presentation" class="em-tb"><tr><td>/blog/cookieless-analytics<div style="height:6px;width:82%;background:#2563eb;border-radius:3px;margin-top:6px"></div></td><td class="r">2,140</td></tr><tr><td>/pricing<div style="height:6px;width:61%;background:#2563eb;opacity:.7;border-radius:3px;margin-top:6px"></div></td><td class="r">1,590</td></tr><tr><td>news.ycombinator.com (referrer)<div style="height:6px;width:40%;background:#2563eb;opacity:.5;border-radius:3px;margin-top:6px"></div></td><td class="r">1,044</td></tr></table>' + HR +
   '<p><b>Waiting on you</b></p><p>Goal “Signup” hasn\'t fired in 3 days. The button may have changed. <a class="em-a" href="#">Check the goal</a></p>' + btn('Open the dashboard'),
   FOOT('Tally Analytics, Berlin', 'You get this every Monday.'))),
 ('mail-invite', 'Team Invite Email', 'A workspace invitation from a named person: who invited you, what the workspace is, the role you\'ll have, an accept button and an expiry date.', ['email', 'invite', 'team', 'collaboration'],
  shell('Beacon', '#b45309', 'Jonas invited you to Northwind Design on Beacon.',
   '<h1>Jonas Lind invited you to Northwind Design</h1><p>Northwind Design uses Beacon to plan projects. You\'ll join as an <b>Editor</b>, so you can create and change projects.</p><div class="em-box" style="margin:20px 0"><p style="margin:0 0 4px"><b>“Sam, this is where the Kestrel launch lives. Start with the timeline board.”</b></p><p class="mu" style="margin:0">Jonas</p></div>' + btn('Accept invitation') + '<p class="mu" style="margin-top:20px">This invite expires on 20 November. Not expecting it? You can ignore this email.</p>',
   'Beacon, 1 Market Sq, Copenhagen<br>You got this because Jonas entered your address.')),
 ('mail-shipping', 'Shipping Update Email', 'A shipped notification with a progress strip, the carrier and tracking number, the delivery window as a date, and what to do if nobody is home.', ['email', 'shipping', 'tracking', 'delivery'],
  shell('Mossware', '#4d7c0f', 'Arriving Monday 16 November.',
   '<p class="mu">Order #A-20419</p><h1>Your order is on its way</h1><p>Expected <b>Monday 16 November, 9:00–13:00</b>.</p>' +
   '<table role="presentation" width="100%" style="margin:18px 0 8px"><tr><td width="25%" style="padding-right:4px"><div style="height:5px;border-radius:3px;background:#4d7c0f"></div></td><td width="25%" style="padding-right:4px"><div style="height:5px;border-radius:3px;background:#4d7c0f"></div></td><td width="25%" style="padding-right:4px"><div style="height:5px;border-radius:3px;background:#4d7c0f;opacity:.35"></div></td><td width="25%"><div style="height:5px;border-radius:3px;background:#dad9d3"></div></td></tr><tr><td class="mu" style="font-size:12px;padding-top:6px">Ordered</td><td class="mu" style="font-size:12px;padding-top:6px">Shipped</td><td class="mu" style="font-size:12px;padding-top:6px">Out for delivery</td><td class="mu" style="font-size:12px;padding-top:6px">Delivered</td></tr></table>' +
   '<div class="em-box" style="margin:18px 0"><p class="mu" style="margin:0 0 4px">PostNL tracking</p><p style="margin:0;font-family:ui-monospace,Menlo,monospace">3SMOS0042719</p></div>' + btn('Track parcel') + '<p style="margin-top:20px">Not home? The courier leaves it with a neighbour or at the PostNL point on Breestraat 12.</p>',
   FOOT('Mossware, Rapenburg 8, Leiden', 'Shipping emails are sent for every order.'))),
 ('mail-newsletter', 'Newsletter Email', 'An editorial newsletter issue: issue number, a lead essay with a hero photo, two shorter links with reading times and a short sign-off, built for long reads in a mail client.', ['email', 'newsletter', 'editorial'],
  shell('Field Notes', '#9a3412', 'No. 214: Why every manhole cover in Tokyo is different.',
   '<p class="mu">No. 214 · Sunday 9 November</p><img src="media/pics/c/1047.jpg" width="520" alt="A narrow street between brick buildings" style="width:100%;height:auto;border-radius:8px;margin-bottom:20px"><h1 style="font-family:Georgia,serif;font-weight:400;font-size:28px">Why every manhole cover in Tokyo is different</h1><p>In 1985 a sewer official in Tokyo had a problem: nobody wanted sewers built in their street. His fix was to make the lids beautiful. Forty years later there are over 6,000 designs.</p><p><a class="em-a" href="#"><b>Read the essay (7 min)</b></a></p>' + HR +
   '<p><b>Also this week</b></p><p><a class="em-a" href="#">The 400-year-old reason your street bends</a><br><span class="mu">11 min · from the archive</span></p><p><a class="em-a" href="#">Reading a city from its power lines</a><br><span class="mu">9 min</span></p>' + HR + '<p>Until next Sunday,<br>Hanne</p>',
   FOOT('Field Notes, Oslo', 'You subscribed at fieldnotes.example.'))),
 ('mail-ticket', 'Event Ticket Email', 'An e-ticket email: event name, date with add-to-calendar, venue with map link, a scannable code block, seat and gate, and the entry rules people actually ask about.', ['email', 'ticket', 'event', 'qr'],
  shell('Edgecase', '#7c2d12', 'Your ticket for Edgecase 2027, 22 April.',
   '<h1>You\'re going to Edgecase 2027</h1><table role="presentation" width="100%" class="em-st"><tr><td width="58%" style="vertical-align:top;padding-bottom:16px"><p class="mu" style="margin:0 0 4px">When</p><p style="margin:0 0 12px"><b>Thu 22 – Fri 23 April 2027</b><br>Doors 08:30</p><p class="mu" style="margin:0 0 4px">Where</p><p style="margin:0"><b>Kulturhuset</b><br>Sergels torg, Stockholm<br><a class="em-a" href="#">Open in maps</a></p></td><td style="vertical-align:top;text-align:center"><div style="display:inline-block;padding:10px;background:#fff;border:1px solid #e7e6e1;border-radius:8px">'+QR+'</div><p class="mu" style="margin:6px 0 0;font-family:ui-monospace,Menlo,monospace">EC27-4418-KV</p></td></tr></table>' +
   '<div class="em-box"><table role="presentation" width="100%"><tr><td class="mu" style="font-size:12px">Ticket</td><td class="mu" style="font-size:12px">Holder</td><td class="mu" style="font-size:12px">Entrance</td></tr><tr><td><b>Two-day pass</b></td><td><b>Sam Rivera</b></td><td><b>Gate B</b></td></tr></table></div>' + HR + btn('Add to calendar') + '<p class="mu" style="margin-top:20px">Bring this email or the PDF. Tickets are transferable until 15 April from your account.</p>',
   FOOT('Edgecase Conferences AB, Stockholm', 'You bought a ticket.'))),
 ('mail-trial-ending', 'Trial Ending Email', 'A trial-ending reminder that is honest: the exact end date, what happens to data if you do nothing, a usage recap of what they\'d lose, and both the upgrade and the downgrade path.', ['email', 'trial', 'billing', 'lifecycle'],
  shell('Quill', '#4338ca', 'Your trial ends Friday. Nothing is deleted.',
   '<h1>Your trial ends on Friday</h1><p>On <b>Friday 20 November</b> your workspace moves to the free plan. Nothing gets deleted: anything above the free limits becomes read-only.</p><div class="em-box" style="margin:18px 0"><p class="mu" style="margin:0 0 8px">In 14 days your team</p><table role="presentation" class="em-tb"><tr><td>Created documents</td><td class="r">48</td></tr><tr><td>Used version history</td><td class="r">12 times</td></tr><tr><td>Invited guests</td><td class="r">3</td></tr></table></div><p>Version history and guests are Pro features. Keep them for €8 per person a month.</p>' + btn('Keep Pro') + '<p style="margin-top:20px">Free plan is fine? You don\'t need to do anything.</p>',
   FOOT('Quill Software GmbH, Hamburg', 'You started a trial on 6 November.'))),
 ('mail-security-alert', 'Security Alert Email', 'A new sign-in alert with device, approximate location, time in the reader\'s zone and IP, a “yes, it was me” no-action note and a prominent “secure my account” path.', ['email', 'security', 'alert', 'login'],
  shell('Atlas', '#b91c1c', 'New sign-in from Windows in Vienna.',
   '<h1>New sign-in to your account</h1><p>Your account <b>rafael@example.com</b> was just used to sign in on a new device.</p><div class="em-box" style="margin:18px 0"><table role="presentation" class="em-tb"><tr><td>Device</td><td class="r">Windows · Edge 131</td></tr><tr><td>Location</td><td class="r">Vienna, Austria (approx.)</td></tr><tr><td>Time</td><td class="r">13 Nov, 21:14 CET</td></tr><tr><td>IP address</td><td class="r">81.217.xx.xx</td></tr></table></div><p><b>Was this you?</b> Then there\'s nothing to do.</p><p><b>Not you?</b> Change your password now and we\'ll sign out every other device.</p>' + btn('Secure my account'),
   'Atlas Inc.<br>Security alerts are always sent. They can\'t be turned off.')),
 ('mail-nps', 'Feedback Survey Email', 'A one-question feedback email with a 0–10 scale as tappable links (each one records the score), sized for thumbs, plus why it matters and a promise about length.', ['email', 'survey', 'nps', 'feedback'],
  shell('Pocket', '#be123c', 'One question, takes 5 seconds.',
   '<h1>How likely are you to recommend Pocket to a friend?</h1><p>Tap a number. That\'s the whole survey, and it goes straight to the people who build the app.</p><table role="presentation" width="100%" style="margin:20px 0 6px;table-layout:fixed"><tr>' +
   ''.join(f'<td style="padding:0 2px"><a href="#" style="display:block;text-align:center;padding:12px 0;border:1px solid #dad9d3;border-radius:6px;font-weight:600;color:#1c1c1a;text-decoration:none;font-size:14px">{i}</a></td>' for i in range(11)) +
   '</tr></table><table role="presentation" width="100%"><tr><td class="mu" style="font-size:12px">Not likely</td><td class="mu" style="font-size:12px;text-align:right">Very likely</td></tr></table><p class="mu" style="margin-top:20px">We ask each person at most twice a year.</p>',
   FOOT('Pocket Finance Ltd, London', 'You use Pocket.'))),
 ('mail-verify-code', 'Verification Code Email', 'A sign-in code email designed for speed: the code in the preview text and subject-ready, large monospace digits, expiry, and the request context for safety.', ['email', 'otp', 'code', 'verification'],
  shell('Sprout', '#15803d', 'Your code is 482 913',
   '<h1>Your sign-in code</h1><p>Enter this code in the Sprout app to finish signing in.</p><div class="em-code">482913</div><p class="mu" style="margin-top:14px">Expires in 10 minutes. Requested from iPhone · Lisbon at 09:41.</p>' + HR + '<p>Didn\'t try to sign in? Someone may have typed your email by mistake. You can ignore this, nobody gets in without the code.</p>',
   'Sprout Plants, Lisbon<br>Security email, sent because a code was requested.')),
]

def build(e):
    id_, name, desc, tags, html = e
    (ROOT / 'components' / f'{id_}.html').write_text(f'<style>{CSS}</style>\n{html}\n')
    return [id_, name, 'Emails', desc, tags, 1]
if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    R = [build(e) for e in E if not args or e[0] in args]
    print('built', len(R))
    if '--reg' in sys.argv:
        for r in R: print('  ' + json.dumps(r, ensure_ascii=False) + ',')
