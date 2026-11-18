# Blue-hour New Year grade for the Istanbul Bosphorus photo + one strip of fireworks.
import cv2,numpy as np,sys
src,maskp,out=sys.argv[1],sys.argv[2],sys.argv[3]
rng=np.random.default_rng(11)
im=cv2.imread(src); H,W=im.shape[:2]
f=im.astype(np.float32)/255; L=f.mean(2)
sky=cv2.imread(maskp,0).astype(np.float32)/255
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
def hexbgr(h): h=h.lstrip('#'); return np.array([int(h[4:6],16),int(h[2:4],16),int(h[0:2],16)],np.float32)/255
# ---- 1) sky: blue-hour gradient keeping the cloud texture
t=np.clip(yy/880,0,1)[...,None]
top,mid,hor=hexbgr('#07122b'),hexbgr('#16305e'),hexbgr('#3e5f93')
grad=np.where(t<0.6, top*(1-t/0.6)+mid*(t/0.6), mid*(1-(t-0.6)/0.4)+hor*((t-0.6)/0.4))
warm=np.exp(-(((xx-120)/520)**2+((yy-880)/260)**2))[...,None]          # faint afterglow where the sun was
grad=grad*(1-0.55*warm)+hexbgr('#b77c78')*0.55*warm
cl=L-cv2.GaussianBlur(L,(0,0),60); cl=cv2.GaussianBlur(cl,(0,0),1.2)    # cloud detail
cloudamt=np.clip((L-0.55)/0.4,0,1)
skyc=grad*(1+1.1*cl[...,None])+ (hexbgr('#5b6f9c')*0.22*cloudamt[...,None])*(1-t*0.3)
# ---- 2) ground: day-for-night
g=f.copy()
gray=g.mean(2,keepdims=True)
g=gray*0.35+g*0.65                                   # desaturate a bit
g=g**1.15*0.30                                       # underexpose
g=g*hexbgr('#7f9bd8')*1.6                            # blue night tint
g=np.clip(g,0,1)
# warm light sources
bld=(1-sky)*(yy<1300)
# windows: darker rectangles in facades
Lb=cv2.GaussianBlur(L,(0,0),0.7)
loc=cv2.blur(Lb,(15,15))
win=((Lb<loc-0.07)&(bld>0.5)).astype(np.uint8)
win=cv2.morphologyEx(win,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(win,4)
lit=np.zeros((H,W),np.float32)
for i in range(1,n):
    x,y,w,h,a=st[i]
    if 6<=a<=160 and w<=22 and h<=24 and rng.random()<0.30:
        lit[lab==i]=rng.uniform(0.35,0.8)
lit=cv2.GaussianBlur(lit,(0,0),0.9)
wcol=hexbgr('#ffc47a')
g=g*(1-lit[...,None])+wcol*lit[...,None]*0.95
g+=cv2.GaussianBlur(lit,(0,0),4)[...,None]*wcol*0.35
# floodlit mosque and waterfront palaces (relight original luminance with warm light)
mosque=np.exp(-(((xx-478)/95)**2+((yy-930)/95)**2))*(1-sky)
palace=np.clip((yy-1095)/40,0,1)*np.clip((1295-yy)/30,0,1)*(1-sky)*(1-0.6*lit)
relight=(Lb[...,None]**1.2)*hexbgr('#ffd9a0')
g=g*(1-0.75*mosque[...,None])+relight*0.9*mosque[...,None]
g=g*(1-0.45*palace[...,None])+relight*0.62*palace[...,None]
# promenade lamps along the shore + boat cabin
lamps=np.zeros((H,W),np.float32)
for x in np.arange(12,W,34)+rng.integers(-4,5,len(np.arange(12,W,34))):
    if 525<x<775: continue
    cv2.circle(lamps,(int(x),1287),2,1.0,-1)
cv2.rectangle(lamps,(560,1288),(640,1300),0.55,-1)
lampg=cv2.GaussianBlur(lamps,(0,0),1.0)+cv2.GaussianBlur(lamps,(0,0),6)*1.6
g+=lampg[...,None]*hexbgr('#ffcf8a')*0.9
boat=((xx>530)&(xx<775)&(yy>1270)&(yy<1340)&(Lb>0.6)).astype(np.float32)
g=g*(1-0.35*cv2.GaussianBlur(boat,(0,0),1)[...,None])
# ---- 3) water: night blue + reflections of the shore lights
water=(yy>1305).astype(np.float32)
wl=L-cv2.GaussianBlur(L,(0,0),8)                      # wave texture
refl=np.zeros((H,W),np.float32)
src_row=np.clip(lampg[1280:1300].max(0)+ (palace[1200:1290]*Lb[1200:1290]).mean(0)*0.8 + (lit[1100:1290]).mean(0)*1.5,0,3)
for x in range(W):
    refl[1306:,x]=src_row[x]
decay=np.exp(-(yy-1306).clip(0)/260)
refl=cv2.GaussianBlur(refl,(0,0),sigmaX=2.2,sigmaY=0.1)*decay*np.clip(0.55+6*wl,0,1.6)
waterc=g*0.6+hexbgr('#0a1934')*0.35
waterc+=refl[...,None]*hexbgr('#ffc47a')*0.55
waterc+=np.clip(wl,0,None)[...,None]*hexbgr('#5f7fbf')*0.35  # sky glints on waves
g=g*(1-water[...,None])+waterc*water[...,None]
# ---- 4) fireworks: one strip of bursts above the skyline
fw=np.zeros((H,W,3),np.float32)
cols=[hexbgr(c) for c in ('#ffcf73','#fff0d2','#ffb35c','#ffe2a8','#a9cfff','#ffcf73','#ffc58a')]
centers=[(92,748,48,0.7),(238,708,80,1.0),(402,762,46,0.65),(560,698,94,1.0),(738,752,56,0.75),(898,712,78,0.95),(1050,760,44,0.6)]
Z=2
for (cx,cy,r,inten),c in zip(centers,cols):
    can=np.zeros((H*Z//1,W*Z//1),np.uint8)
    nray=int(70+r*0.6)
    for k in range(nray):
        th=2*np.pi*k/nray+rng.normal(0,0.04)
        rr=r*rng.uniform(0.78,1.05)
        pts=[]
        for s in np.linspace(0.18,1,14):
            px=cx+np.cos(th)*rr*s; py=cy+np.sin(th)*rr*s+ (s**2)*r*0.16
            pts.append((int(px*Z),int(py*Z)))
        b=rng.uniform(0.5,1)
        for j in range(len(pts)-1):
            v=int(255*b*((j/len(pts))**1.8))
            cv2.line(can,pts[j],pts[j+1],v,1,cv2.LINE_AA)
        cv2.circle(can,pts[-1],1+int(rng.random()<0.4),int(255*b),-1,cv2.LINE_AA)
        if rng.random()<0.5:   # falling sparkle beyond the tip
            ex,ey=pts[-1]; cv2.circle(can,(ex+int(rng.normal(0,3)),ey+int(r*Z*rng.uniform(0.08,0.22))),1,int(180*b),-1,cv2.LINE_AA)
    a=cv2.resize(can,(W,H),interpolation=cv2.INTER_AREA).astype(np.float32)/255
    core=np.exp(-(((xx-cx)/(r*0.35))**2+((yy-cy)/(r*0.35))**2))*0.06
    a=a+core
    glow=cv2.GaussianBlur(a,(0,0),3)*0.6+cv2.GaussianBlur(a,(0,0),r*0.45)*0.7
    fw+= (a[...,None]*1.25*c+glow[...,None]*c**1.8)*inten
fw*=sky[...,None]
# light spill of the fireworks on sky and faint reflection on water
spill=cv2.GaussianBlur(fw,(0,0),60)*0.6
skyc=skyc+spill
frow=cv2.GaussianBlur(fw[600:840].max(0),(0,0),3)
wref=np.zeros_like(fw); wref[1306:]=frow[None]*0.18
wref*=(decay*np.clip(0.4+6*wl,0,1.5))[...,None]
# ---- compose
outimg=skyc*sky[...,None]+g*(1-sky[...,None])
outimg=outimg+fw+wref*water[...,None]
# subtle vignette and grain
v=1-0.25*(((xx-W/2)/(W*0.8))**2+((yy-H*0.55)/(H*0.75))**2)
outimg*=np.clip(v,0.7,1)[...,None]
outimg+=rng.normal(0,0.008,outimg.shape).astype(np.float32)
cv2.imwrite(out,np.clip(outimg*255,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,95])
