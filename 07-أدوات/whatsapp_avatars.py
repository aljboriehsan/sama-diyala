# Five distinct WhatsApp profile pictures for staff numbers, same symbol and proportions as the approved
# profile picture (symbol's enclosing circle = 30% of the width, centred for the circular crop).
# Usage (repo root): python3 07-أدوات/whatsapp_avatars.py <out_dir>
import re, sys, io, os, cairosvg, cv2, numpy as np
from PIL import Image, ImageDraw
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True); N = 2048; R_FILL = 0.30
src = open('01-الشعار/SVG/الرمز - على الأخضر.svg').read()
vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', src).group(1).split()]
paths = re.findall(r'<path [^>]+/>', src)          # 0-2 gold (plane, ring, speed lines), 3-4 white (SD, Samaa Diyala)
probe = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" width="{N}" height="{N}">{"".join(paths)}</svg>'
a = np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=probe.encode()))).split()[-1])
(cx, cy), r = cv2.minEnclosingCircle(cv2.findNonZero((a > 8).astype(np.uint8)))
ux = vb[2] / N; ucx, ucy = vb[0] + cx * ux, vb[1] + cy * ux; half = r * ux / R_FILL / 2
X, Y, S = ucx - half, ucy - half, 2 * half          # square viewBox in symbol units
def recol(gold, white):
    out = []
    for i, p in enumerate(paths):
        out.append(re.sub(r'fill="[^"]*"', f'fill="{gold if i < 3 else white}"', p))
    return ''.join(out)
G, M, GD, DG, LG, W = '#0E4D2C', '#2F7A41', '#C9A44C', '#A8862F', '#E9F2EA', '#FFFFFF'
def u(f): return f'{X + f*S:.2f}'            # fraction of the canvas -> user units (x)
def v(f): return f'{Y + f*S:.2f}'
def L(f): return f'{f*S:.2f}'
VARIANTS = {
 # 1 — white: gold mark, green letters
 '1 - أبيض': (f'<rect x="{u(0)}" y="{v(0)}" width="{L(1)}" height="{L(1)}" fill="{W}"/>', recol(GD, G)),
 # 2 — gold: white mark, green letters
 '2 - ذهبي': (f'<rect x="{u(0)}" y="{v(0)}" width="{L(1)}" height="{L(1)}" fill="{GD}"/>', recol(W, G)),
 # 3 — green with a soft light centre and a thin gold ring inside the circular crop
 '3 - أخضر بحلقة ذهبية': (
   f'<defs><radialGradient id="g" cx="50%" cy="50%" r="60%"><stop offset="0" stop-color="#1f6b42"/><stop offset="1" stop-color="{G}"/></radialGradient></defs>'
   f'<rect x="{u(0)}" y="{v(0)}" width="{L(1)}" height="{L(1)}" fill="url(#g)"/>'
   f'<circle cx="{u(.5)}" cy="{v(.5)}" r="{L(.445)}" fill="none" stroke="{GD}" stroke-width="{L(.006)}"/>', recol(GD, W)),
 # 4 — light green: mid-green mark, dark green letters
 '4 - أخضر فاتح': (f'<rect x="{u(0)}" y="{v(0)}" width="{L(1)}" height="{L(1)}" fill="{LG}"/>'
   f'<circle cx="{u(.5)}" cy="{v(.5)}" r="{L(.445)}" fill="none" stroke="{M}" stroke-opacity=".35" stroke-width="{L(.004)}" stroke-dasharray="{L(.012)} {L(.012)}"/>', recol(DG, G)),
 # 5 — split: gold lower-left / green upper-right along the brand's slant, white mark and letters
 '5 - أخضر وذهبي مائل': (f'<rect x="{u(0)}" y="{v(0)}" width="{L(1)}" height="{L(1)}" fill="{G}"/>'
   f'<polygon points="{u(0)},{v(.80)} {u(1)},{v(1.02)} {u(1)},{v(1)} {u(0)},{v(1)}" fill="{GD}"/>'
   f'<polygon points="{u(0)},{v(.765)} {u(1)},{v(.985)} {u(1)},{v(1.005)} {u(0)},{v(.785)}" fill="{M}"/>', recol(GD, W)),
}
tiles = []
for name, (bg, mark) in VARIANTS.items():
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{X:.2f} {Y:.2f} {S:.2f} {S:.2f}" width="{N}" height="{N}">{bg}{mark}</svg>'
    open(f'{OUT}/{name}.svg', 'w').write(svg)
    png = f'{OUT}/{name}.png'; cairosvg.svg2png(bytestring=svg.encode(), write_to=png)
    im = Image.open(png).convert('RGB').resize((420, 420), Image.LANCZOS)
    m = Image.new('L', (420, 420), 0); ImageDraw.Draw(m).ellipse((0, 0, 419, 419), fill=255)
    t = Image.new('RGB', (420, 420), (240, 242, 245)); t.paste(im, (0, 0), m); tiles.append(t)
sheet = Image.new('RGB', (5 * 450 + 30, 480), (240, 242, 245))
for i, t in enumerate(tiles): sheet.paste(t, (30 + i * 450, 30))
sheet.save(f'{OUT}/معاينة بالقص الدائري.png'); print('ok', len(tiles))
