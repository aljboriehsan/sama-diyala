# Builds the profile picture: the symbol on brand green, centred optically inside the circular crop.
# Usage: python3 profile_picture.py <out_dir>
import re,sys,io,cairosvg,cv2,numpy as np
from PIL import Image
OUT=sys.argv[1]; N=2048; R_FILL=0.40          # symbol's enclosing circle = 40% of canvas width (radius)
src=open('01-الشعار/SVG/الرمز - على الأخضر.svg').read()
vb=[float(v) for v in re.search(r'viewBox="([^"]+)"',src).group(1).split()]
paths=re.findall(r'<path [^>]+/>',src)
def build(keep_inner_text):
    ps=paths if keep_inner_text else paths[:4]
    # 1) render shapes alone to find their minimum enclosing circle
    probe=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" width="{N}" height="{N}">{"".join(ps)}</svg>'
    a=np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=probe.encode()))).split()[-1])
    pts=cv2.findNonZero((a>8).astype(np.uint8)); (cx,cy),r=cv2.minEnclosingCircle(pts)
    # 2) map that circle onto the canvas centre with radius R_FILL*N
    s=(R_FILL*N)/r; ux=vb[2]/N                    # user units per probe pixel
    ucx,ucy=vb[0]+cx*ux, vb[1]+cy*ux; ur=r*ux
    half=ur/R_FILL/2                              # half side of the new viewBox in user units
    nvb=(ucx-half,ucy-half,2*half,2*half)
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{nvb[0]:.2f} {nvb[1]:.2f} {nvb[2]:.2f} {nvb[3]:.2f}" width="{N}" height="{N}">'
         f'<rect x="{nvb[0]:.2f}" y="{nvb[1]:.2f}" width="{nvb[2]:.2f}" height="{nvb[3]:.2f}" fill="#0E4D2C"/>{"".join(ps)}</svg>')
    return svg
for keep,name in [(False,'صورة البروفايل'),(True,'صورة البروفايل - مع الاسم الصغير')]:
    svg=build(keep)
    open(f'{OUT}/{name}.svg','w').write(svg)
    cairosvg.svg2png(bytestring=svg.encode(),write_to=f'{OUT}/{name} - 2048.png')
    print('ok',name)
