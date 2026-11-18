# Single-colour symbol without the small inner "Samaa Diyala", tight viewBox. Used in offer ads.
import re,io,cairosvg,numpy as np
from PIL import Image
src=open('01-الشعار/SVG/الرمز - على الأخضر.svg').read()
vb=[float(v) for v in re.search(r'viewBox="([^"]+)"',src).group(1).split()]
paths=re.findall(r'<path [^>]+/>',src)[:4]          # bars, arc, plane, SD
N=2000
probe=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" width="{N}" height="{N}">{"".join(paths)}</svg>'
a=np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=probe.encode()))).split()[-1])
ys,xs=np.where(a>4); u=vb[2]/N
x0,y0,x1,y1=vb[0]+xs.min()*u,vb[1]+ys.min()*u,vb[0]+(xs.max()+1)*u,vb[1]+(ys.max()+1)*u
import os; os.makedirs('01-الشعار/أحادي بلا الاسم الصغير',exist_ok=True)
for name,col in [('أبيض','#FFFFFF'),('أخضر','#0E4D2C'),('ذهبي','#C9A44C')]:
    body=''.join(re.sub(r'fill="[^"]+"',f'fill="{col}"',p) for p in paths)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {x1-x0:.2f} {y1-y0:.2f}">{body}</svg>'
    open(f'01-الشعار/أحادي بلا الاسم الصغير/الرمز - {name}.svg','w').write(svg)
    cairosvg.svg2png(bytestring=svg.encode(),write_to=f'01-الشعار/أحادي بلا الاسم الصغير/الرمز - {name}.png',output_width=1200)
print('aspect',(x1-x0)/(y1-y0))
