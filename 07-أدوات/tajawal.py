# Converts a design page from the old fonts (Noto Naskh + IBM Plex) to the house font Tajawal, scaled up.
# Usage: python3 tajawal.py <page.html> [scale=1.15]   (writes the page in place; keeps "<name> - الخط القديم.html" once)
import sys, os, re, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, '07-أدوات', 'خطوط')
WEIGHT = {400: 500, 500: 500, 600: 700, 700: 800, 800: 800}
FIT = '''<script>
// stretch the agent line to the exact width of logo + name (Tajawal widths differ from the old measured setup)
document.fonts.ready.then(()=>{const t=document.getElementById('tag'),l=document.getElementById('lockup');
 if(t&&l){t.style.transform='none';let ws=0;for(let i=0;i<60;i++){const d=l.getBoundingClientRect().width-t.getBoundingClientRect().width;if(Math.abs(d)<0.5)break;ws+=d/5*0.9;t.style.wordSpacing=ws+'px';}}
 document.body.dataset.ready='1'});
</script>'''

def faces(rel):
    out = ''
    for fam, pairs in (('Tajawal', {700: 800}), ('TajawalT', {400: 500, 500: 500, 600: 700, 700: 800, 800: 800})):
        for cw, fw in pairs.items():
            out += (f'@font-face{{font-family:{fam};font-weight:{cw};src:url("{rel}/tajawal-arabic-{fw}-normal.woff2");unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF,U+200C-200E}}\n'
                    f'@font-face{{font-family:{fam};font-weight:{cw};src:url("{rel}/tajawal-latin-{fw}-normal.woff2");unicode-range:U+0000-00FF,U+2000-206F}}\n')
    return out

def convert(s, rel, scale=1.15):
    if 'tajawal-arabic' in s:
        return s
    s = re.sub(r'[ \t]*@font-face\{[^}]*\}\n?', '', s)
    s = s.replace('<style>', '<style>\n' + faces(rel), 1)
    s = re.sub(r'font-family:\s*"?Naskh"?', 'font-family:Tajawal', s)
    s = re.sub(r'font-family:\s*"?Plex"?', 'font-family:TajawalT', s)
    a, b = s.index('<style>'), s.index('</style>')
    css = re.sub(r'font-size:(\d+(?:\.\d+)?)px', lambda m: f'font-size:{float(m.group(1)) * scale:.0f}px', s[a:b])
    css = re.sub(r'--tag-size:\s*[\d.]+px', '--tag-size:23px', css)
    css = re.sub(r'--name-dy:\s*[\d.]+px', '--name-dy:4px', css)
    s = s[:a] + css + '.tag{margin-top:10px !important}\n' + s[b:]
    s = re.sub(r"<script>\s*document\.fonts\.ready\.then\(\(\)=>\{\s*document\.body\.dataset\.ready='1'\s*\}\)\s*</script>", FIT, s)
    return s

if __name__ == '__main__':
    p = os.path.abspath(sys.argv[1]); sc = float(sys.argv[2]) if len(sys.argv) > 2 else 1.15
    rel = os.path.relpath(FONTS, os.path.dirname(p))
    old = p[:-5] + ' - الخط القديم.html'
    if not os.path.exists(old):
        shutil.copy(p, old)
    src = open(p).read()
    open(p, 'w').write(convert(src, rel, sc))
    print('ok', os.path.basename(os.path.dirname(p)))
