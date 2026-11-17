import json, re, cairosvg
p=json.load(open('final_paths.json'))
def tf(d,s,dx,dy):
    nums=re.findall(r'-?\d+\.?\d*',d); it=iter(nums); out=[]
    def rep(m):
        return m.group(0)
    toks=re.findall(r'[MLCQZ]|-?\d+\.?\d*',d); res=[]; buf=[]
    for t in toks:
        if t in 'MLCQZ': res.append(t); continue
        buf.append(float(t))
        if len(buf)==2:
            x,y=buf; res.append(f'{x*s+dx:.2f} {y*s+dy:.2f}'); buf=[]
    return ' '.join(res)
# inner text = name glyphs scaled
s_in=16.5/70.6
p['small2']=tf(p['name'],s_in,327-323.4*s_in,280-445*s_in)
# horizontal layout parts (symbol unchanged coords; text block moved)
t=1.3; X0=512; top=208-(519.1-374.4)*t/2
for k in ['name','tagline']:
    p['h_'+k]=tf(p[k],t,X0-(-0.2)*t,top-374.4*t)
def svg(vb,parts,bg=None,w=2000):
    x,y,W,H=vb
    r=f'<rect x="{x}" y="{y}" width="{W}" height="{H}" fill="{bg}"/>' if bg else ''
    body=''.join(f'<path fill-rule="{ "nonzero" if k in ("arc","plane","bars","sd") else "evenodd"}" fill="{c}" d="{p[k]}"/>' for k,c in parts)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {W} {H}" width="{w}" height="{round(w*H/W)}">{r}{body}</svg>'
G,GOLD,GOLDT,W='#0E4D2C','#C9A44C','#A8862F','#FFFFFF'
FULL=(-30,-25,707,575); SYM=(31,-59,460,460)
hw=X0+647*t+30; HOR=(21,-30,hw-21,402)
def parts(mark,tag,which):
    sym=[('bars',GOLD),('arc',GOLD),('plane',GOLD),('sd',mark),('small2',mark)]
    if which=='full': return sym+[('name',mark),('tagline',tag)]
    if which=='hor': return sym+[('h_name',mark),('h_tagline',tag)]
    return sym
V={}
for which,vb in [('full',FULL),('sym',SYM),('hor',HOR)]:
    V[f'{which}_primary']=svg(vb,parts(G,GOLDT,which))
    V[f'{which}_green']=svg(vb,parts(W,GOLD,which),G)
    V[f'up_{which}_primary']=svg(vb,parts(G,GOLDT,which))
    V[f'up_{which}_white']=svg(vb,parts(W,GOLD,which))
for k,sv in V.items():
    open(k+'.svg','w').write(sv)
    if not k.startswith('up_'): cairosvg.svg2png(bytestring=sv.encode(),write_to=k+'.png')
print('hor vb',HOR)
