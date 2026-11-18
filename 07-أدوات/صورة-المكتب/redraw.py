# Redraw the reflective letters of the wall sign as clean shapes, matching the clean letters' face and border.
import cv2,numpy as np,sys
src,out,S=sys.argv[1],sys.argv[2],sys.argv[3]
im=cv2.imread(src); f=im.astype(np.float32); g=f.mean(2)
Z=4
# --- letter faces (x0,y0,x1,y1) in image pixels ---
R1=[(1905,527,1923,576),(1878,528,1896,576),(1846,569,1896,576),          # ا ل baseline
    (1846,544,1862,576),(1815,544,1862,552),(1841,528,1858,534),          # خ + dot
    (1796,569,1848,577),                                                  # خ→ط
    (1740,530,1757,577),(1740,545,1798,552),(1782,545,1798,577),(1740,567,1798,577),  # ط
    (1720,568,1742,577),                                                  # ط→و
    (1694,545,1728,577),(1710,570,1728,591),                              # و
    (1631,532,1647,579),(1631,546,1684,554),(1671,546,1684,579),(1631,567,1684,579)]  # ط
R2=[(1591,534,1607,579),(1568,535,1585,581),(1500,573,1585,581),          # ا ل baseline
    (1515,550,1556,558),(1541,550,1556,581),(1540,586,1556,592),          # ج + dot
    (1471,551,1502,582),(1486,582,1502,593)]                              # و (edge)
REG=[((1622,519,1933,599),R1),((1497,527,1630,599),R2)]
# --- border profile sampled around clean letters (distance from face) ---
cx0,cy0,cx1,cy1=1385,528,1497,600
cg=g[cy0:cy1,cx0:cx1]; cf=f[cy0:cy1,cx0:cx1]
face=(((cf[:,:,1]-cf[:,:,2]>10)&(cg<90))|(cg<55)).astype(np.uint8)
dist=cv2.distanceTransform(1-face,cv2.DIST_L2,5)
prof=[np.median(cf[(dist>r-0.5)&(dist<=r+0.5)],0) for r in range(0,9)]
facecol=np.median(cf[cv2.erode(face,np.ones((3,3),np.uint8))==1],0)
print('face',facecol); [print(r,p) for r,p in enumerate(prof)]
# --- wall model from clean rows above/below the line ---
def strip(a,b):
    s=np.median(g[a:b],0); return cv2.GaussianBlur(s.reshape(1,-1),(0,0),6).ravel()
s0,s1=strip(503,512),strip(604,614)
tint0=np.median(f[503:512,1300:1950].reshape(-1,3),0)
rng=np.random.default_rng(7)
for (x0,y0,x1,y1),rects in REG:
    W,H=x1-x0,y1-y0
    m=np.zeros((H*Z,W*Z),np.uint8)
    for (a,b,c,d) in rects:
        cv2.rectangle(m,((a-x0)*Z,(b-y0)*Z),((c-x0)*Z-1,(d-y0)*Z-1),1,-1)
    k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4*Z+1,4*Z+1))
    m=cv2.morphologyEx(cv2.morphologyEx(m,cv2.MORPH_CLOSE,k),cv2.MORPH_OPEN,k)
    dd=cv2.distanceTransform(1-m,cv2.DIST_L2,5)/Z          # distance (px) from face
    # colour per pixel at Z scale: face colour inside, border profile outside, wall beyond
    t=np.clip((np.arange(H*Z)/Z+y0-507)/(609-507),0,1)[:,None]
    wl=np.interp(np.arange(W*Z)/Z+x0,np.arange(len(s0)),s0)[None]*(1-t)+np.interp(np.arange(W*Z)/Z+x0,np.arange(len(s1)),s1)[None]*t
    tint=tint0/tint0.mean()
    wallc=wl[...,None]*tint[None,None]
    col=np.where(m[...,None]==1,facecol,wallc)
    wall_ref=np.mean(prof[7:9],0).mean()
    for r in range(1,7):
        sel=(dd>r-1)&(dd<=r)
        # border colour expressed relative to wall so it follows the wall gradient
        rel=prof[r]/wall_ref
        col[sel]=(wl[...,None]*rel)[sel]
    small=cv2.resize(col.astype(np.float32),(W,H),interpolation=cv2.INTER_AREA)
    small+=rng.normal(0,1.3,small.shape)
    # feather the region edge (it lies on plain wall)
    fm=np.zeros((H,W),np.float32); fm[3:-3,3:-3]=1; fm=cv2.GaussianBlur(fm,(0,0),1.5)[...,None]
    f[y0:y1,x0:x1]=f[y0:y1,x0:x1]*(1-fm)+small*fm
res=np.clip(f,0,255).astype(np.uint8)
cv2.imwrite(out,res,[cv2.IMWRITE_JPEG_QUALITY,97])
a=cv2.imread(src)
cv2.imwrite(S+'/sign/cmp1x.png', np.vstack([a[490:710,1150:1980], res[490:710,1150:1980]]))
cv2.imwrite(S+'/sign/cmp3x.png', np.vstack([cv2.resize(a[505:605,1460:1945],None,fx=2.5,fy=2.5,interpolation=cv2.INTER_CUBIC),cv2.resize(res[505:605,1460:1945],None,fx=2.5,fy=2.5,interpolation=cv2.INTER_CUBIC)]))
