import cv2,numpy as np,sys
im=cv2.imread(sys.argv[1]); H,W=im.shape[:2]
f=im.astype(np.float32); B,G,R=f[...,0],f[...,1],f[...,2]; L=f.mean(2)
hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV); s=hsv[...,1]/255.
sky=((B-R>12)&(L>110))|((L>175)&(s<0.22))
sky=sky.astype(np.uint8)
# texture: buildings have edges
gx=cv2.Sobel(cv2.GaussianBlur(L,(0,0),1),cv2.CV_32F,1,0); gy=cv2.Sobel(cv2.GaussianBlur(L,(0,0),1),cv2.CV_32F,0,1)
tex=cv2.GaussianBlur(np.hypot(gx,gy),(0,0),3)
sky[tex>28]=0
# per column skyline: first row from top (below y=600) where non-sky run of >=6 px starts
sl=np.zeros(W,int)
for x in range(W):
    col=sky[600:1350,x]; run=0; y0=None
    for i,v in enumerate(col):
        if v==0:
            run+=1
            if run>=6: y0=600+i-5; break
        else: run=0
    sl[x]=y0 if y0 is not None else 1300
# remove outliers: median filter small, but keep minarets (narrow up spikes) -> use min of median and raw only where raw is part of a 3+px wide group
med=cv2.medianBlur(sl.astype(np.uint8 if sl.max()<256 else np.uint16).reshape(1,-1) if False else sl.astype(np.float32).reshape(1,-1),5).ravel() if False else sl
mask=np.zeros((H,W),np.uint8)
for x in range(W): mask[:sl[x],x]=255
mask=cv2.GaussianBlur(mask,(0,0),1.2)
cv2.imwrite(sys.argv[2],mask)
vis=im.copy(); vis[mask>128]=(vis[mask>128]*0.4+np.array([0,0,255])*0.6).astype(np.uint8)
cv2.imwrite(sys.argv[3],cv2.resize(vis[700:1350],None,fx=1,fy=1))
print(sl.min(),sl.max(),np.percentile(sl,[5,50,95]))
# --- refine: walk down from sl-14 until colour departs from the local sky colour
sm=cv2.GaussianBlur(f,(0,0),0.8)
sl2=sl.copy()
for x in range(W):
    a=max(0,sl[x]-26); ref=np.median(f[a:sl[x]-14, max(0,x-3):x+4].reshape(-1,3),0)
    y=sl[x]-14
    while y<sl[x]+10 and np.abs(sm[y,x]-ref).max()<22: y+=1
    sl2[x]=y
# keep narrow spires: if neighbours differ a lot keep min
mask=np.zeros((H,W),np.uint8)
for x in range(W): mask[:sl2[x],x]=255
mask=cv2.GaussianBlur(mask,(0,0),0.9)
cv2.imwrite(sys.argv[2],mask)
np.save(sys.argv[2]+'.npy',sl2)
vis=im.copy(); vis[mask>128]=(vis[mask>128]*0.4+np.array([0,0,255])*0.6).astype(np.uint8)
cv2.imwrite(sys.argv[3],cv2.resize(vis[780:1100,300:900],None,fx=2,fy=2))
print('refined',np.percentile(sl2-sl,[5,50,95]))
# --- geodesic grow into sky-coloured pixels (fixes the gaps beside the minarets)
m0=(mask>128).astype(np.uint8)
small=cv2.resize(im,(W//4,H//4)); msk=cv2.resize(255-m0*255,(W//4,H//4),interpolation=cv2.INTER_NEAREST)
est=cv2.resize(cv2.inpaint(small,msk,9,cv2.INPAINT_TELEA),(W,H)).astype(np.float32)
skylike=(np.abs(sm-est).max(2)<20).astype(np.uint8)
skylike[1060:]=0
g=m0.copy(); k=np.ones((3,3),np.uint8)
for _ in range(30): g=cv2.dilate(g,k)&(skylike|m0)
mask=cv2.GaussianBlur(g*255,(0,0),0.8)
cv2.imwrite(sys.argv[2],mask)
vis=im.copy(); vis[mask>128]=(vis[mask>128]*0.4+np.array([0,0,255])*0.6).astype(np.uint8)
cv2.imwrite(sys.argv[3],cv2.resize(vis[780:1100,300:900],None,fx=2,fy=2))
