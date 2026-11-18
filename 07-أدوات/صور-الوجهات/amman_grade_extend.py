# Amman (Temple of Hercules): warm late-afternoon grade, deeper sky gradient,
# sky extended upward so the columns start below the ad header; framed to 1080x1350.
import cv2,numpy as np,sys
src,out,OFF=sys.argv[1],sys.argv[2],int(sys.argv[3])
im=cv2.imread(src).astype(np.float32)/255; H,W=im.shape[:2]
B,G,R=im[...,0],im[...,1],im[...,2]
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
sky=((B-R>0.18)&(B>0.35)).astype(np.uint8)
sky=cv2.morphologyEx(sky,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(sky,4)
keep=[i for i in range(1,n) if st[i,4]>300]; sky=np.isin(lab,keep).astype(np.float32)
skyw=cv2.GaussianBlur(sky,(0,0),1.2)[...,None]
# --- ground / stone: warm, golden, a bit more contrast, lifted shadows
g=im.copy()
L=g.mean(2,keepdims=True)
g=g*np.array([0.90,1.00,1.10],np.float32)                      # warm WB (BGR)
g=g+np.clip(0.30-L,0,None)*0.25                                # lift deep shadows
hl=np.clip((L-0.55)/0.4,0,1)
g=g*(1+hl*np.array([-0.06,0.0,0.05],np.float32))               # golden highlights
s=1/(1+np.exp(-(g-0.5)*6)); s=(s-s.min())/(s.max()-s.min()); g=g*0.82+s*0.18
hsv=cv2.cvtColor(np.clip(g,0,1).astype(np.float32),cv2.COLOR_BGR2HSV); hsv[...,1]*=1.05; g=cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
# --- sky: smooth late-afternoon gradient (deep blue -> pale warm near the horizon), keep grain
horizon=int(np.percentile(np.where(sky.any(1))[0],99))
def bgr(h): h=h.lstrip('#'); return np.array([int(h[4:6],16),int(h[2:4],16),int(h[0:2],16)],np.float32)/255
top_c,mid_c,hor_c=bgr('#143877'),bgr('#3a6cb0'),bgr('#cfd9e2')
def skygrad(y):   # y in "extended" coordinates, 0 = new top
    t=np.clip(y/(horizon+OFF_s),0,1)
    a=np.clip(t/0.7,0,1)[...,None]; b=np.clip((t-0.7)/0.3,0,1)[...,None]
    c=top_c*(1-a)+mid_c*a
    return c*(1-b)+hor_c*b
OFF_s=int(round(OFF/0.5625))                                   # offset in source pixels
grain=im-cv2.GaussianBlur(im,(0,0),1.5)
lowv=cv2.GaussianBlur(im.mean(2),(0,0),40); lowv=(lowv/np.clip(cv2.GaussianBlur(lowv,(0,0),400),1e-3,None))[...,None]
rnS=cv2.GaussianBlur(np.random.default_rng(2).normal(0,0.012,im.shape).astype(np.float32),(0,0),0.7)
skyc=skygrad(yy+OFF_s)+rnS+grain*0.25
warm=np.exp(-((yy-horizon)/170)**2)[...,None]*0.10             # faint warm haze at the horizon
skyc=skyc*(1-warm)+bgr('#f0d2a8')*warm
outimg=g*(1-skyw)+skyc*skyw
# --- extend the sky upward by OFF_s rows
ext_y=np.arange(OFF_s,dtype=np.float32)[:,None]*np.ones((1,W),np.float32)
ext=skygrad(ext_y)
rn=np.random.default_rng(1).normal(0,0.012,ext.shape).astype(np.float32)
ext=ext+cv2.GaussianBlur(rn,(0,0),0.7)
full=np.concatenate([ext,outimg],0)
full=cv2.resize(full,(1080,int(round(full.shape[0]*0.5625))),interpolation=cv2.INTER_AREA)[:1350]
cv2.imwrite(out,np.clip(full*255,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,96])
print(full.shape,'horizon',horizon)
