# Generates five B2B commission posts in the house identity. Run from the repo root.
import re, os
OUT = '09-التصاميم/عمولة الإصدار - خمسة نماذج'
t = open('09-التصاميم/قالب الثقة - ليش تحجز من الوكيل العام/إعلان.html').read()
FONTS = "\n".join(l for l in t.splitlines() if '@font-face' in l).replace('../../07', '../../../07')
HEADCSS = "\n".join(l for l in t.splitlines() if re.match(r'\s*\.(brand|lockup|tag)\b', l) or '.lockup .name' in l
                    or 'transform:translateY(var(--name-dy))' in l or 'white-space:nowrap;text-align:center;opacity:.92' in l)
R = '../../../'
COMMISSION = '6.5%'
WA = '<svg viewBox="0 0 32 32" fill="currentColor"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-4-.5-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.6 5.8 5 2.1.9 3 1 4 .8.7-.1 1.9-.8 2.2-1.6.3-.8.3-1.4.2-1.6-.1-.1-.3-.2-.6-.3z"/></svg>'
EM = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm1 2.4V17h16V7.4l-8 5.3-8-5.3zM5.2 7 12 11.5 18.8 7H5.2z"/></svg>'
PLANE = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.5 15.2v-1.9l-8-5V3.5a1.5 1.5 0 0 0-3 0v4.8l-8 5v1.9l8-2.5v5.3l-2 1.5V21l3.5-1 3.5 1v-1.5l-2-1.5v-5.3z" transform="rotate(-90 12 12)"/></svg>'

def header(dark, top=52):
    logo = 'الرمز - أبيض.svg' if dark else 'الرمز - أخضر.svg'
    col = '#fff' if dark else '#0E4D2C'; tagc = '#fff' if dark else '#2F7A41'
    return f'''<div class="head" style="top:{top}px;color:{col}"><div class="brand" id="brand"><div class="lockup" id="lockup">
<img src="{R}01-الشعار/أحادي بلا الاسم الصغير/{logo}" alt=""><div class="name">سماء ديالى</div></div>
<div class="tag" id="tag" style="color:{tagc}">الوكيــــــل العــــــام للخطــــــوط الجويــــــة العراقيـــــة</div></div></div>'''

def contacts(dark, bottom=86):
    c = '#fff' if dark else '#0E4D2C'; k = 'rgba(233,242,234,.75)' if dark else '#6E8B77'
    icbg = '#C9A44C' if dark else '#2F7A41'; icc = '#0E4D2C' if dark else '#fff'
    return f'''<div class="ct" style="bottom:{bottom}px;color:{c}">
<div class="it"><span class="ic" style="background:{icbg};color:{icc}">{WA}</span><div><div class="k" style="color:{k}">للإصدار والاستفسار</div><div class="v ph">077 0006 9900</div><div class="v ph">077 0756 4440</div></div></div>
<div class="sep"></div>
<div class="it"><span class="ic" style="background:{icbg};color:{icc}">{EM}</span><div><div class="k" style="color:{k}">البريد الإلكتروني</div><div class="v em">samaa_dyala1@yahoo.com</div></div></div></div>'''

BASE = f'''{FONTS}
:root{{--green:#0E4D2C;--mid:#2F7A41;--gold:#C9A44C;--dgold:#A8862F;--light:#E9F2EA;
  --lock-dx:-1.9px; --name-dy:22px; --tag-size:20px; --tag-ws:0.72px; --tag-dx:0.4px;}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
.ad{{position:relative;width:1080px;height:1350px;overflow:hidden}}
{HEADCSS}
.head{{position:absolute;left:0;right:0;display:flex;flex-direction:column;align-items:center;z-index:5}}
.tag{{opacity:1}}
.ct{{position:absolute;left:60px;right:60px;display:flex;align-items:center;justify-content:center;gap:40px;direction:rtl;z-index:5}}
.ct .it{{display:flex;align-items:center;gap:16px}}
.ct .ic{{width:60px;height:60px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none}}
.ct .ic svg{{width:32px;height:32px}}
.ct .k{{font-family:Plex;font-weight:500;font-size:19px;line-height:1.2}}
.ct .v{{font-family:Plex;font-weight:600;font-size:32px;line-height:1.25;direction:ltr;text-align:right}}
.ct .v.ph{{word-spacing:-4px;letter-spacing:1px}}
.ct .v.em{{font-size:25px;font-weight:500}}
.ct .sep{{width:1.5px;height:70px;background:var(--gold);opacity:.7}}
.stripes{{position:absolute;left:50%;bottom:30px;transform:translateX(-50%);display:flex;gap:7px;z-index:5}}
.stripes i{{display:block;width:44px;height:6px;transform:skewX(-35deg);border-radius:1px}}
.stripes i:nth-child(1){{background:var(--gold)}} .stripes i:nth-child(2){{background:var(--mid)}}
.greet{{font-family:Naskh;font-weight:700;line-height:1.15}}
.ttl{{font-family:Naskh;font-weight:700;line-height:1.15}}
.sub{{font-family:Plex;font-weight:500}}
'''
def page(title, css, body):
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{title}</title><style>
{BASE}{css}</style></head><body><div class="ad">
{body}
<div class="stripes"><i></i><i></i></div></div>
<script>document.fonts.ready.then(()=>{{document.body.dataset.ready='1'}})</script></body></html>'''

D = {}
# 2 — our real office with the Iraqi Airways wall
D['2 - المكتب'] = page('المكتب', '''
.ad{background:#0E4D2C;color:#fff}
.bgph{position:absolute;left:-1010px;top:-40px;height:1440px}
.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,40,24,.78) 0%,rgba(8,40,24,.25) 22%,rgba(8,40,24,0) 34%,rgba(8,40,24,.15) 48%,rgba(10,58,33,.88) 64%,#0b4026 78%)}
.txt{position:absolute;top:790px;left:0;right:0;text-align:center}
.greet{font-size:48px;color:var(--gold)} .ttl{font-size:84px} .sub{font-size:30px;color:#E9F2EA;margin-top:4px}
.comm{margin-top:14px;display:inline-flex;align-items:center;gap:18px}
.comm .w{font-family:Naskh;font-weight:700;font-size:58px}
.comm .n{font-family:Plex;font-weight:600;font-size:104px;line-height:1;color:var(--gold);direction:ltr}
''', f'<img class="bgph" src="{R}08-الصور/المكتب - الواجهة (نهائية بإضاءة سينمائية).jpg" alt=""><div class="sh"></div>' + header(True, 46) + f'''
<div class="txt"><div class="greet">صباح الخير</div><div class="ttl">يمكنكم الإصدار الآن</div><div class="sub">تذاكر الخطوط الجوية العراقية</div>
<div class="comm"><span class="w">بعمولة</span><span class="n">{COMMISSION}</span></div></div>
''' + contacts(True, 70))

# 3 — one giant number
D['3 - الرقم الكبير'] = page('الرقم الكبير', '''
.ad{background:radial-gradient(90% 60% at 50% 45%,#1d6a40 0%,#0E4D2C 55%,#083a1f 100%);color:#fff}
.txt{position:absolute;top:236px;left:0;right:0;text-align:center}
.greet{font-size:52px;color:var(--gold)} .ttl{font-size:86px;margin-top:2px}
.big{position:absolute;left:0;right:0;top:500px;text-align:center;font-family:Plex;font-weight:600;font-size:330px;line-height:1;color:var(--gold);direction:ltr;letter-spacing:-4px;
  text-shadow:0 18px 50px rgba(0,0,0,.25)}
.lbl{position:absolute;left:0;right:0;top:860px;text-align:center}
.lbl .a{display:inline-block;font-family:Plex;font-weight:600;font-size:34px;color:#0E4D2C;background:#E9F2EA;border-radius:999px;padding:10px 34px 13px}
.lbl .b{margin-top:16px;font-family:Plex;font-weight:500;font-size:30px;color:#E9F2EA}
.plane{position:absolute;left:610px;top:404px;width:420px;filter:drop-shadow(0 14px 18px rgba(0,0,0,.3))}
.trail{position:absolute;inset:0}
.ring{position:absolute;left:50%;top:675px;width:760px;height:760px;margin:-380px 0 0 -380px;border-radius:50%;border:1.5px solid rgba(201,164,76,.28)}
''', header(True) + f'''
<div class="ring"></div>
<div class="txt"><div class="greet">صباح الخير</div><div class="ttl">يمكنكم الإصدار الآن</div></div>
<div class="big">{COMMISSION}</div>
<div class="lbl"><div class="a">عمولة إصدار</div><div class="b">تذاكر الخطوط الجوية العراقية</div></div>
''' + contacts(True))

# 4 — airport departures board
flap = lambda ch: f'<span class="fl">{ch}</span>'
D['4 - لوحة المغادرة'] = page('لوحة المغادرة', '''
.ad{background:linear-gradient(180deg,#0E4D2C 0%,#0a3a21 100%);color:#fff}
.txt{position:absolute;top:236px;left:0;right:0;text-align:center}
.greet{font-size:52px;color:var(--gold)} .ttl{font-size:86px;margin-top:2px}
.board{position:absolute;left:56px;right:56px;top:520px;background:#06281a;border-radius:24px;padding:30px 34px 36px;box-shadow:inset 0 0 0 2px rgba(201,164,76,.35),0 24px 50px rgba(0,0,0,.35)}
.bh{display:flex;align-items:center;justify-content:space-between;font-family:Plex;font-weight:500;font-size:22px;color:#C9A44C;padding-bottom:16px;border-bottom:1.5px solid rgba(201,164,76,.3)}
.bh b{font-weight:600;letter-spacing:2px;direction:ltr;font-size:20px;color:#9FC2A6}
.bh .t{display:flex;align-items:center;gap:12px}.bh .t svg{width:26px;height:26px}
.row{display:grid;grid-template-columns:1fr auto;align-items:center;padding:40px 4px;border-bottom:1.5px dashed rgba(233,242,234,.14)}
.row:last-child{border-bottom:0}
.row .k{font-family:Plex;font-size:22px;color:#9FC2A6;margin-bottom:6px}
.row .v{font-family:Plex;font-weight:600;font-size:36px}
.flaps{display:flex;gap:8px;direction:ltr}
.fl{width:88px;height:122px;border-radius:10px;background:linear-gradient(180deg,#123f28 0 49%,#0b3320 51% 100%);color:#C9A44C;font-family:Plex;font-weight:600;font-size:88px;
  display:flex;align-items:center;justify-content:center;position:relative;box-shadow:0 4px 0 rgba(0,0,0,.35)}
.fl::after{content:"";position:absolute;left:0;right:0;top:50%;height:2px;background:#03180e}
.st{display:inline-flex;align-items:center;gap:12px;font-family:Plex;font-weight:600;font-size:30px;color:#7ee2a0}
.st i{width:16px;height:16px;border-radius:50%;background:#45d07a;box-shadow:0 0 14px #45d07a}
''', header(True) + f'''
<div class="txt"><div class="greet">صباح الخير</div><div class="ttl">يمكنكم الإصدار الآن</div></div>
<div class="board">
 <div class="bh"><span class="t">{PLANE}الإصدار</span><b>ISSUANCE</b></div>
 <div class="row"><div><div class="k">الناقل</div><div class="v">الخطوط الجوية العراقية</div></div><span class="st"><i></i>متاح الآن</span></div>
 <div class="row"><div><div class="k">العمولة</div><div class="v">على إصدار التذاكر</div></div><div class="flaps">{''.join(flap(c) for c in COMMISSION)}</div></div>
</div>
''' + contacts(True))

# 5 — morning sunrise
D['5 - الشروق'] = page('الشروق', '''
.ad{background:linear-gradient(180deg,#fbf5e6 0%,#f7f1e2 40%,#eef4ee 75%,#e6efe8 100%);color:#0E4D2C}
.sun{position:absolute;left:50%;top:560px;width:520px;height:520px;margin:-260px 0 0 -260px;border-radius:50%;
  background:radial-gradient(circle at 50% 45%,#f3dc9a 0%,#e3c46f 45%,#C9A44C 100%);box-shadow:0 0 120px 40px rgba(232,200,110,.35)}
.r1,.r2{position:absolute;left:50%;top:560px;border-radius:50%;border:1.5px solid rgba(201,164,76,.35)}
.r1{width:680px;height:680px;margin:-340px 0 0 -340px}.r2{width:840px;height:840px;margin:-420px 0 0 -420px;border-color:rgba(201,164,76,.2)}
.plane{position:absolute;left:70px;top:430px;width:940px;filter:drop-shadow(0 24px 26px rgba(14,77,44,.22))}
.greet{position:absolute;left:0;right:0;top:218px;text-align:center;font-size:104px;color:#0E4D2C}
.txt{position:absolute;top:860px;left:0;right:0;text-align:center}
.ttl{font-size:70px} .sub{font-size:30px;color:#2F7A41;margin-top:4px}
.comm{margin-top:22px;display:inline-flex;align-items:center;gap:18px;background:#0E4D2C;color:#fff;border-radius:999px;padding:8px 44px 12px}
.comm .w{font-family:Naskh;font-weight:700;font-size:46px}
.comm .n{font-family:Plex;font-weight:600;font-size:74px;line-height:1.1;color:#C9A44C;direction:ltr}
''', header(False) + f'''
<div class="r2"></div><div class="r1"></div><div class="sun"></div>
<div class="greet">صباح الخير</div>
<img class="plane" src="{R}08-الصور/طائرة العراقية YI-ASU (مفرغة).png" alt="">
<div class="txt"><div class="ttl">يمكنكم الإصدار الآن</div><div class="sub">تذاكر الخطوط الجوية العراقية</div>
<div class="comm"><span class="w">بعمولة</span><span class="n">{COMMISSION}</span></div></div>
''' + contacts(False))

for name, html in D.items():
    d = f'{OUT}/{name}'; os.makedirs(d, exist_ok=True)
    import importlib.util as _u
    _sp = _u.spec_from_file_location('tj', '07-أدوات/tajawal.py'); _tj = _u.module_from_spec(_sp); _sp.loader.exec_module(_tj)
    html = _tj.convert(html, '../../../07-أدوات/خطوط', 1.15)   # house font Tajawal (from 23 Nov 2026)
    open(f'{d}/إعلان.html', 'w').write(html)
print('\n'.join(D))
