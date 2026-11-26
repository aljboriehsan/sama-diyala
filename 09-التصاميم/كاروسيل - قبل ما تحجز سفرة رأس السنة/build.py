# Carousel "قبل ما تحجز سفرة رأس السنة… تأكد من هاي الخمسة" — 7 slides 1080×1350, exported ×2.
# Run from the repo root: python3 "09-التصاميم/كاروسيل - قبل ما تحجز سفرة رأس السنة/build.py"
import os, subprocess
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(os.path.dirname(D))
FONTS='''  @font-face{font-family:Tajawal;font-weight:700;src:url("../../07-أدوات/خطوط/tajawal-arabic-800-normal.woff2");unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF,U+200C-200E}
  @font-face{font-family:Tajawal;font-weight:700;src:url("../../07-أدوات/خطوط/tajawal-latin-800-normal.woff2");unicode-range:U+0000-00FF,U+2000-206F}
  @font-face{font-family:TajawalT;font-weight:400;src:url("../../07-أدوات/خطوط/tajawal-arabic-500-normal.woff2");unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF,U+200C-200E}
  @font-face{font-family:TajawalT;font-weight:400;src:url("../../07-أدوات/خطوط/tajawal-latin-500-normal.woff2");unicode-range:U+0000-00FF,U+2000-206F}
  @font-face{font-family:TajawalT;font-weight:500;src:url("../../07-أدوات/خطوط/tajawal-arabic-500-normal.woff2");unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF,U+200C-200E}
  @font-face{font-family:TajawalT;font-weight:500;src:url("../../07-أدوات/خطوط/tajawal-latin-500-normal.woff2");unicode-range:U+0000-00FF,U+2000-206F}
  @font-face{font-family:TajawalT;font-weight:600;src:url("../../07-أدوات/خطوط/tajawal-arabic-700-normal.woff2");unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF,U+200C-200E}
  @font-face{font-family:TajawalT;font-weight:600;src:url("../../07-أدوات/خطوط/tajawal-latin-700-normal.woff2");unicode-range:U+0000-00FF,U+2000-206F}
  @font-face{font-family:TajawalT;font-weight:700;src:url("../../07-أدوات/خطوط/tajawal-arabic-800-normal.woff2");unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF,U+200C-200E}
  @font-face{font-family:TajawalT;font-weight:700;src:url("../../07-أدوات/خطوط/tajawal-latin-800-normal.woff2");unicode-range:U+0000-00FF,U+2000-206F}'''
WA='''<svg viewBox="0 0 32 32" fill="#0E4D2C"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-4-.5-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.6 5.8 5 2.1.9 3 1 4 .8.7-.1 1.9-.8 2.2-1.6.3-.8.3-1.4.2-1.6-.1-.1-.3-.2-.6-.3z"/></svg>'''
LOGO_W='../../01-الشعار/أحادي بلا الاسم الصغير/الرمز - أبيض.svg'
LOGO_G='../../01-الشعار/أحادي بلا الاسم الصغير/الرمز - أخضر.svg'
G='#0E4D2C'; M='#2F7A41'; GOLD='#C9A44C'; DG='#A8862F'
ICONS={
'passport':'<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><rect x="14" y="6" width="36" height="52" rx="5"/><circle cx="32" cy="27" r="9"/><path d="M23 27h18M32 18c-4 5-4 13 0 18M32 18c4 5 4 13 0 18"/><path d="M24 46h16"/></svg>',
'visa':'<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 6h22l12 12v40H16z"/><path d="M38 6v12h12"/><circle cx="31" cy="38" r="10"/><path d="M26 38l4 4 7-8"/></svg>',
'price':'<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="12" width="40" height="40" rx="5"/><path d="M8 24h40M18 6v10M38 6v10"/><path d="M42 50l14-14M46 36h10v10"/></svg>',
'bag':'<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><rect x="12" y="18" width="40" height="36" rx="6"/><path d="M24 18v-6a4 4 0 0 1 4-4h8a4 4 0 0 1 4 4v6"/><path d="M22 58v-4M42 58v-4"/><text x="32" y="42" text-anchor="middle" font-size="13" font-family="Tajawal" font-weight="800" fill="currentColor" stroke="none">KG</text></svg>',
'phone':'<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><rect x="18" y="4" width="28" height="56" rx="6"/><path d="M28 52h8"/><rect x="24" y="14" width="16" height="22" rx="2"/><circle cx="32" cy="23" r="4"/><path d="M27 32c1-3 9-3 10 0"/></svg>',
}
SLIDES=[
 ('passport','الجواز','لازم يكون صالح <b>6 أشهر</b> على الأقل بعد تاريخ رجوعك، وبعض الدول ترجّعك من المطار إذا أقل.'),
 ('visa','الفيزا','شوف وجهتك تحتاج فيزا لو لا، وكم يوم ياخذ إصدارها.','<b>إحنا نسويها إلك</b> ونتابعها لحد ما تطلع.'),
 ('price','الحجز المبكر','أسعار التذاكر والفنادق برأس السنة <b>تصعد كل ما يقرب الموعد</b>، والمقاعد تخلص بسرعة.'),
 ('bag','وزن العفش','اعرف الوزن المسموح بتذكرتك قبل ما تحضّر الجنطة، حتى <b>ما تدفع زيادة</b> بالمطار.'),
 ('phone','نسخة بموبايلك','صوّر الجواز والتذاكر وحجز الفندق واحفظهم بموبايلك، <b>تحتاجهم إذا ضاع شي</b>.'),
]
CSS=FONTS+f'''
:root{{--g:{G};--m:{M};--gold:{GOLD};--dg:{DG}}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
.s{{position:relative;width:1080px;height:1350px;overflow:hidden;direction:rtl}}
.brand{{position:absolute;left:0;right:0;top:70px;display:flex;flex-direction:column;align-items:center}}
.lockup{{display:flex;align-items:center;gap:16px}}
.lockup img{{height:84px;display:block}}
.lockup .nm{{font-family:Tajawal;font-weight:800;font-size:64px;line-height:1;white-space:nowrap;padding-bottom:6px}}
.tag{{margin-top:12px;font-family:TajawalT;font-weight:700;font-size:24px;line-height:1.2;white-space:nowrap}}
.pg{{position:absolute;left:60px;top:84px;font-family:Tajawal;font-weight:700;font-size:26px;letter-spacing:1px;direction:ltr}}
.stripes{{position:absolute;left:-60px;right:-60px;bottom:96px;height:40px;transform:rotate(-4deg)}}
.stripes i{{position:absolute;left:0;right:0;display:block}}
.ft{{position:absolute;left:0;right:0;bottom:44px;display:flex;justify-content:center;align-items:center;gap:12px;direction:ltr;font-family:Tajawal;font-weight:700;font-size:30px;letter-spacing:.5px;word-spacing:-4px}}
.ft .ic{{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center}}
.ft .ic svg{{width:24px;height:24px}}
'''
FIT="""<script>document.fonts.ready.then(()=>{const t=document.getElementById('tag'),l=document.getElementById('lockup');if(t){let f=parseFloat(getComputedStyle(t).fontSize);while(t.getBoundingClientRect().width>l.getBoundingClientRect().width&&f>12){f-=0.25;t.style.fontSize=f+'px';}let ws=0;for(let i=0;i<60;i++){const d=l.getBoundingClientRect().width-t.getBoundingClientRect().width;if(Math.abs(d)<0.5)break;ws+=d/4*0.9;t.style.wordSpacing=ws+'px';}}document.body.dataset.ready='1'})</script>"""
def brand(dark):
    return f'''<div class="brand"><div class="lockup" id="lockup"><img src="{LOGO_W if dark else LOGO_G}" alt=""><div class="nm" style="color:{'#fff' if dark else G}">سماء ديالى</div></div>
<div class="tag" id="tag" style="color:{'#fff' if dark else G}">الوكيل العام للخطوط الجوية العراقية</div></div>'''
def footer(dark, num='077 4177 7500'):
    c='#fff' if dark else G
    wa=WA.replace('fill="#0E4D2C"','fill="'+(G if dark else '#fff')+'"')
    return f'''<div class="stripes"><i style="top:0;height:10px;background:{GOLD}"></i><i style="top:16px;height:18px;background:{M if not dark else '#1c6a3c'}"></i></div>
<div class="ft" style="color:{c}"><span class="ic" style="background:{GOLD if dark else G}">{wa}</span>{num}</div>'''
def page(body, extra_css=''):
    return f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{CSS}{extra_css}</style></head><body>{body}{FIT}</body></html>'

pages=[]
# 1 cover
checks=''.join(f'<div class="ck"><span class="bx"><svg viewBox="0 0 24 24" fill="none" stroke="{G}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span><span>{t}</span></div>' for _,t,*__ in SLIDES)
pages.append(page(f'''<div class="s cov">{brand(True)}
<div class="k">سفرة رأس السنة؟</div>
<div class="t">تأكد من هاي <span>الخمسة</span><br>قبل ما تحجز</div>
<div class="list">{checks}</div>
<div class="sw"><svg viewBox="0 0 48 24" fill="none" stroke="{GOLD}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M44 12H6M14 4l-8 8 8 8"/></svg>اسحب</div>
{footer(True)}</div>''', f'''
.cov{{background:radial-gradient(90% 70% at 50% 30%,#17643c 0%,{G} 55%,#0a3c22 100%);color:#fff}}
.cov .k{{position:absolute;left:0;right:0;top:300px;text-align:center;font-family:Tajawal;font-weight:800;font-size:64px;color:{GOLD}}}
.cov .t{{position:absolute;left:0;right:0;top:390px;text-align:center;font-family:Tajawal;font-weight:800;font-size:98px;line-height:1.2}}
.cov .t span{{color:{GOLD}}}
.cov .list{{position:absolute;left:190px;right:190px;top:650px;display:flex;flex-direction:column;gap:16px}}
.ck{{display:flex;align-items:center;gap:22px;background:rgba(255,255,255,.08);border:2px solid rgba(201,164,76,.45);border-radius:22px;padding:10px 26px;font-family:Tajawal;font-weight:700;font-size:40px}}
.ck .bx{{width:52px;height:52px;border-radius:14px;background:{GOLD};display:flex;align-items:center;justify-content:center;flex:none}}
.ck .bx svg{{width:34px;height:34px}}
.cov .sw{{position:absolute;left:70px;top:1110px;display:flex;align-items:center;gap:12px;font-family:Tajawal;font-weight:700;font-size:30px;color:{GOLD};direction:ltr}}
.cov .sw svg{{width:52px;height:26px}}
'''))
# 2-6 tips
for i,(ic,title,txt,*tip) in enumerate(SLIDES, start=1):
    tipb=f'<div class="tip"><svg viewBox="0 0 24 24" fill="{GOLD}"><path d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7L12 17.3 5.8 20.9l1.6-7L2 9.2l7.1-.6z"/></svg><span>{tip[0]}</span></div>' if tip else ''
    pages.append(page(f'''<div class="s tp">{brand(False)}<div class="pg" style="color:{DG}">{i+1}/7</div>
<div class="wrap"><div class="card"><div class="num">{i}</div><div class="ico">{ICONS[ic]}</div>
<div class="ti">{title}</div><div class="dv"></div><div class="tx">{txt}</div>{tipb}</div></div>
{footer(False)}</div>''', f'''
.tp{{background:linear-gradient(180deg,#FFFFFF 0%,#E9F2EA 100%)}}
.wrap{{position:absolute;left:80px;right:80px;top:250px;bottom:190px;display:flex;align-items:center}}
.card{{position:relative;width:100%;padding-bottom:80px !important;background:#fff;border-radius:44px;box-shadow:0 20px 50px rgba(14,77,44,.12);border:2px solid rgba(14,77,44,.08);display:flex;flex-direction:column;align-items:center;padding:70px 70px 0;text-align:center}}
.num{{position:absolute;top:-46px;right:70px;width:104px;height:104px;border-radius:50%;background:{GOLD};color:{G};display:flex;align-items:center;justify-content:center;font-family:Tajawal;font-weight:800;font-size:60px;box-shadow:0 8px 20px rgba(168,134,47,.35)}}
.ico{{width:220px;height:220px;border-radius:50%;background:#E9F2EA;color:{G};display:flex;align-items:center;justify-content:center}}
.ico svg{{width:130px;height:130px}}
.ti{{margin-top:44px;font-family:Tajawal;font-weight:800;font-size:92px;line-height:1.1;color:{G}}}
.dv{{margin:28px 0 30px;width:110px;height:6px;border-radius:3px;background:{GOLD}}}
.tx{{font-family:TajawalT;font-weight:500;font-size:46px;line-height:1.55;color:#24382c;text-wrap:balance}}
.tx b{{font-weight:800;color:{G}}}
.tip{{margin-top:30px;display:flex;align-items:center;gap:14px;background:#FBF5E6;border:2px solid rgba(201,164,76,.55);border-radius:20px;padding:14px 26px;font-family:TajawalT;font-weight:600;font-size:38px;color:{G}}}
.tip b{{font-weight:800}}
.tip svg{{width:38px;height:38px;flex:none}}
'''))
# 7 closing
pages.append(page(f'''<div class="s end">{brand(True)}
<div class="q">عدك سؤال<br>عن سفرتك؟</div>
<div class="sub">راسلنا، ونرتبلك كلشي من التذكرة للفيزا<br>من أي محافظة</div>
<div class="btn"><span class="ic">{WA.replace('fill="#0E4D2C"','fill="'+GOLD+'"')}</span>077 4177 7500</div>
<div class="ph"><svg viewBox="0 0 24 24" fill="{GOLD}"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>077 0756 4440</div>
<div class="stripes"><i style="top:0;height:10px;background:{GOLD}"></i><i style="top:16px;height:18px;background:#1c6a3c"></i></div></div>''', f'''
.end{{background:radial-gradient(90% 70% at 50% 40%,#17643c 0%,{G} 55%,#0a3c22 100%);color:#fff;text-align:center}}
.end .q{{position:absolute;left:0;right:0;top:340px;font-family:Tajawal;font-weight:800;font-size:110px;line-height:1.18}}
.end .sub{{position:absolute;left:0;right:0;top:640px;text-wrap:balance;font-family:TajawalT;font-weight:500;font-size:44px;line-height:1.5;color:#E9F2EA}}
.end .btn{{position:absolute;left:170px;right:170px;top:840px;height:132px;border-radius:999px;background:{GOLD};color:{G};display:flex;align-items:center;justify-content:center;gap:22px;direction:ltr;font-family:Tajawal;font-weight:800;font-size:66px;letter-spacing:1px;word-spacing:-8px;box-shadow:0 14px 34px rgba(0,0,0,.3)}}
.end .btn .ic{{width:86px;height:86px;border-radius:50%;background:{G};display:flex;align-items:center;justify-content:center}}
.end .btn .ic svg{{width:52px;height:52px}}
.end .ph{{position:absolute;left:0;right:0;top:1010px;display:flex;align-items:center;justify-content:center;gap:14px;direction:ltr;font-family:Tajawal;font-weight:700;font-size:46px;word-spacing:-6px}}
.end .ph svg{{width:40px;height:40px}}
'''))
render=os.path.join(R,'07-أدوات','render_plain.js')
for n,html in enumerate(pages, start=1):
    p=os.path.join(D,f'شريحة {n}.html'); open(p,'w').write(html)
print('ok',len(pages))
