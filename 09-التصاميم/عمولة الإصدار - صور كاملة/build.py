# Replacements for the B2B "صباح الخير" posts whose planes were cut out, partial or motion-blurred
# (management note, 25 Nov 2026): every plane here is a whole aircraft in its own real photo.
# Built from the light template (عمولة الإصدار - فاتح). Run from the repo root.
import re, os, sys
sys.path.insert(0, '07-أدوات')
OUT = '09-التصاميم/عمولة الإصدار - صور كاملة'
T = open('09-التصاميم/عمولة الإصدار - فاتح/إعلان.html').read()
T = re.sub(r'  <svg class="deco".*?</svg>\n  <img class="plane"[^>]*>\n', '', T, flags=re.S)
PH = '../../08-الصور/لقطات طائرات العراقية (من المقاطع)/'
COMMISSION = '6.5%'

def dark(t):
    """white header/text over a dark photo, gold contact icons"""
    t = t.replace('أحادي بلا الاسم الصغير/الرمز - أخضر.svg" alt="">\n        <div class="name">',
                  'أحادي بلا الاسم الصغير/الرمز - أبيض.svg" alt="">\n        <div class="name">')
    t = t.replace('<svg viewBox="0 0 32 32" fill="#fff">', '<svg viewBox="0 0 32 32" fill="#0E4D2C">')
    t = t.replace('<svg viewBox="0 0 24 24" fill="#fff">', '<svg viewBox="0 0 24 24" fill="#0E4D2C">')
    return t + '''<style>
.ad{color:#fff}.tag{color:#fff !important}.greet{color:var(--gold) !important}.sub{color:#E9F2EA !important}
.ct .ic{background:var(--gold) !important}.ct .k{color:rgba(233,242,234,.78) !important}
</style>'''

def page(name, css, inner, is_dark=False, keep_ticket=True):
    t = T.replace('../../', '../../../') if False else T
    t = t.replace('<div class="ad">\n  <div class="head">', '<div class="ad">\n' + inner + '\n  <div class="head">', 1)
    if not keep_ticket:
        t = re.sub(r'  <div class="tk">[^\n]*\n', '', t)
    t = t.replace('</style></head>', css + '\n</style></head>', 1)
    if is_dark:
        t = dark(t).replace('</style></head>', '', 0)
        # move the dark overrides inside <head>
        extra = t[t.rindex('<style>'):]; t = t[:t.rindex('<style>')]
        t = t.replace('</style></head>', extra.replace('<style>', '').replace('</style>', '') + '</style></head>', 1)
    t = t.replace('<title>', '<title>').replace('../../08-الصور', '../../08-الصور')
    d = os.path.join(OUT, name); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'إعلان.html'), 'w').write(t.replace('../../', '../../../'))
    print('ok', name)

COMM_LINE = f'<div class="comm"><span class="w">بعمولة</span><span class="n">{COMMISSION}</span></div>'
COMM_CSS = '''.comm{margin-top:12px;display:inline-flex;align-items:center;gap:18px}
.comm .w{font-family:Tajawal;font-weight:700;font-size:66px}
.comm .n{font-family:TajawalT;font-weight:600;font-size:118px;line-height:1;color:var(--gold);direction:ltr}'''

# 2 — Iraqi Airways 777 by the control tower (Baghdad airport), photo on top, text on green below
page('2 - برج المراقبة', f'''
.ad{{background:#0E4D2C}}
.bgp{{position:absolute;left:0;top:0;width:1080px;height:1010px;background:url("{PH}777 قرب برج المراقبة في مطار بغداد.png") 50% -500px/1080px auto no-repeat}}
.sh{{position:absolute;left:0;top:0;width:1080px;height:1010px;background:linear-gradient(180deg,rgba(8,40,24,.55) 0%,rgba(8,40,24,.15) 20%,rgba(8,40,24,0) 32%,rgba(8,40,24,0) 56%,rgba(14,77,44,.85) 78%,#0E4D2C 96%)}}
.txt{{top:760px !important}}
.greet{{font-size:50px !important}} .ttl{{font-size:86px !important}} .sub{{font-size:30px !important}}
{COMM_CSS}
.ct{{bottom:74px !important}}
''', '  <div class="bgp"></div><div class="sh"></div>', is_dark=True, keep_ticket=False)

# 3 — light: the whole YI-ASU in its blue sky, as a framed photo card
page('3 - فاتح', '''
.card{position:absolute;left:70px;top:478px;width:940px;height:500px;border-radius:30px;overflow:hidden;
  background:url("../../08-الصور/طائرة العراقية YI-ASU (سماء زرقاء).jpg") 50% 50%/cover no-repeat;box-shadow:0 22px 44px rgba(14,77,44,.18)}
.frame{position:absolute;left:56px;top:464px;width:968px;height:528px;border-radius:38px;border:2px solid rgba(201,164,76,.55)}
.tk{top:916px !important}
''', '  <div class="frame"></div><div class="card"></div>')

# 4 — light: the 777 climbing out, whole plane in an open sky that fills the post
page('4 - الإقلاع', f'''
.ad{{background:#cfdbe6}}
.bgp{{position:absolute;inset:0;background:url("{PH}777 تقلع كاملة في السماء.png") 50% -150px/1080px auto no-repeat}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,255,255,.72) 0%,rgba(255,255,255,.55) 30%,rgba(255,255,255,0) 44%,rgba(255,255,255,0) 64%,rgba(255,255,255,.55) 80%,rgba(255,255,255,.8) 100%)}}
.tk{{top:930px !important}}
''', '  <div class="bgp"></div><div class="sh"></div>')

# 5 — the 777 small and whole in a wide sky after take-off, dark green mood
page('5 - في السماء', f'''
.ad{{background:#0b2a1a}}
.bgp{{position:absolute;inset:0;background:url("{PH}777 في السماء بعد الإقلاع (صغيرة كاملة).png") 50% -260px/1080px auto no-repeat}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,30,20,.70) 0%,rgba(10,30,20,.55) 22%,rgba(10,30,20,0) 34%,rgba(10,30,20,0) 58%,rgba(8,40,24,.82) 74%,#0b3a22 90%)}}
.txt{{top:900px !important}}
.greet{{display:none}}
.ttl{{font-size:84px !important}} .sub{{font-size:30px !important}}
.morning{{position:absolute;left:0;right:0;top:232px;text-align:center;font-family:Tajawal;font-weight:700;font-size:96px;color:var(--gold);text-shadow:0 4px 30px rgba(0,0,0,.35)}}
{COMM_CSS}
.ct{{bottom:74px !important}}
''', '  <div class="bgp"></div><div class="sh"></div><div class="morning">صباح الخير</div>', is_dark=True, keep_ticket=False)

# 9 — "القوس": cream post, the whole 777 (high-res photo) inside an arch window
page('9 - القوس', f'''
.ad{{background:linear-gradient(180deg,#fbf5e6 0%,#f7f1e2 45%,#eef4ee 100%)}}
.arch{{position:absolute;left:110px;top:330px;width:860px;height:560px;border-radius:430px 430px 26px 26px;overflow:hidden;
  background:url("../../08-الصور/طائرة العراقية (الأصل).jpg") 50% 50%/cover no-repeat;box-shadow:0 22px 44px rgba(168,134,47,.25)}}
.archf{{position:absolute;left:92px;top:312px;width:896px;height:596px;border-radius:448px 448px 36px 36px;border:2px solid rgba(201,164,76,.6)}}
.txt{{top:208px !important}}
.ttl,.sub{{display:none}}
.greet{{font-size:96px !important;color:var(--green) !important}}
.low{{position:absolute;left:0;right:0;top:922px;text-align:center}}
.low .t{{font-family:Tajawal;font-weight:700;font-size:74px;line-height:1.15}}
.low .s{{font-family:TajawalT;font-weight:500;font-size:30px;color:var(--mid);margin-top:2px}}
.pill{{margin-top:14px;display:inline-flex;align-items:center;gap:16px;background:#0E4D2C;color:#fff;border-radius:999px;padding:6px 44px 10px}}
.pill .w{{font-family:Tajawal;font-weight:700;font-size:46px}} .pill .n{{font-family:TajawalT;font-weight:600;font-size:72px;line-height:1.1;color:var(--gold);direction:ltr}}
.ct{{bottom:70px !important}}
''', f'''  <div class="archf"></div><div class="arch"></div>
  <div class="low"><div class="t">يمكنكم الإصدار الآن</div><div class="s">تذاكر الخطوط الجوية العراقية</div><div class="pill"><span class="w">بعمولة</span><span class="n">{COMMISSION}</span></div></div>''', keep_ticket=False)

# the inline commission line goes under the subtitle in 2 and 5
for n in ('2 - برج المراقبة', '5 - في السماء'):
    p = os.path.join(OUT, n, 'إعلان.html'); s = open(p).read()
    s = s.replace('<div class="sub">تذاكر الخطوط الجوية العراقية</div>\n  </div>', '<div class="sub">تذاكر الخطوط الجوية العراقية</div>\n    ' + COMM_LINE + '\n  </div>', 1)
    open(p, 'w').write(s)
