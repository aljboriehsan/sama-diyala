# Builds the 3-photo slanted collage for a boarding-pass ad (as in the Jordan ad).
# Usage: python3 collage_pass.py <ad html> <out dir for parts> <config.json>
# config: {"sky":[src, y0, y1], "panels":[[src, cx, y0, y1] x3 left->right]}  (fractions of the source)
import sys,json,re,os
from PIL import Image,ImageEnhance
html,outd,cfg=sys.argv[1],sys.argv[2],json.load(open(sys.argv[3]))
os.makedirs(outd,exist_ok=True)
def crop(src,cx,y0,y1,size=(460,1000)):
    im=Image.open(src).convert('RGB'); W,H=im.size
    h=(y1-y0)*H; w=h*size[0]/size[1]
    if w>W: w=W; h=w*size[1]/size[0]
    x=min(max(cx*W-w/2,0),W-w); y=y0*H
    return im.crop((int(x),int(y),int(x+w),int(y+h))).resize(size,Image.LANCZOS)
names=['p1','p2','p3']
for n,(src,cx,y0,y1) in zip(names,cfg['panels']):
    ImageEnhance.Contrast(crop(src,cx,y0,y1)).enhance(1.04).save(f'{outd}/{n}.jpg',quality=94)
s_src,s0,s1=cfg['sky']; im=Image.open(s_src).convert('RGB'); W,H=im.size
sky=im.crop((0,int(s0*H),W,int(s1*H))); sky=sky.resize((1080,int(sky.height*1080/W)),Image.LANCZOS); sky.save(f'{outd}/sky.jpg',quality=94)
rel=os.path.relpath(outd,os.path.dirname(html))+'/'
s=open(html).read()
s=re.sub(r'\.photo\{[^}]*\}',f'.photo{{position:absolute;left:0;top:0;width:1080px;height:{sky.height}px;background:url("{rel}sky.jpg") 0 0/1080px {sky.height}px no-repeat}}',s,count=1,flags=re.S)
if '.collage{' not in s:
    s=re.sub(r'\.shade-top\{[^}]*\}','.shade-top{position:absolute;inset:0 0 auto 0;height:640px;\n             background:linear-gradient(180deg,rgba(6,24,44,.50) 0%,rgba(6,24,44,.38) 60%,rgba(6,24,44,.10) 100%)}\n  .collage{position:absolute;inset:0;display:block}',s,count=1,flags=re.S)
s=re.sub(r'\s*<svg class="collage".*?</svg>\n','\n',s,flags=re.S)
def y(x,y0=600,dy=60): return y0-dy*x/1080
L,M1,M2,R=(367,337),(377,347),(733,703),(743,713)
svg=f'''  <svg class="collage" viewBox="0 0 1080 1350" width="1080" height="1350">
    <defs>
      <clipPath id="cA"><polygon points="0,{y(0)} {L[0]},{y(L[0])} {L[1]},1350 0,1350"/></clipPath>
      <clipPath id="cB"><polygon points="{M1[0]},{y(M1[0])} {M2[0]},{y(M2[0])} {M2[1]},1350 {M1[1]},1350"/></clipPath>
      <clipPath id="cC"><polygon points="{R[0]},{y(R[0])} 1080,{y(1080)} 1080,1350 {R[1]},1350"/></clipPath>
    </defs>
    <polygon points="0,{y(0)} 1080,{y(1080)} 1080,1350 0,1350" fill="#C9A44C"/>
    <image href="{rel}p1.jpg" x="-10" y="{y(0)-60}" width="392" height="{1350-y(0)+60}" preserveAspectRatio="xMidYMin slice" clip-path="url(#cA)"/>
    <image href="{rel}p2.jpg" x="330" y="{y(377)-20}" width="420" height="{1350-y(377)+20}" preserveAspectRatio="xMidYMin slice" clip-path="url(#cB)"/>
    <image href="{rel}p3.jpg" x="700" y="{y(743)-30}" width="390" height="{1350-y(743)+30}" preserveAspectRatio="xMidYMin slice" clip-path="url(#cC)"/>
    <polygon points="0,{y(0)-18} 1080,{y(1080)-18} 1080,{y(1080)-10} 0,{y(0)-10}" fill="#2F7A41"/>
    <polygon points="0,{y(0)-10} 1080,{y(1080)-10} 1080,{y(1080)-4} 0,{y(0)-4}" fill="#C9A44C"/>
  </svg>
'''
s=s.replace('  <div class="shade-top"></div>\n','  <div class="shade-top"></div>\n'+svg,1)
open(html,'w').write(s)
print('ok',sky.size)
