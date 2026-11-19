# square poster -> 1080x1350: stretch the clouds above the minaret tips by EXT frame px, mirror the floor at the bottom if needed
import cv2,numpy as np,sys
src,out,EXTF=sys.argv[1],sys.argv[2],int(sys.argv[3])
OH=int(sys.argv[4]) if len(sys.argv)>4 else 1350
im=cv2.imread(src).astype(np.float32); H,W=im.shape[:2]; s=1080/W
Y0=270; EXT=int(round(EXTF/s))
newh=Y0+EXT; t=np.linspace(0,1,newh); w=0.25+0.75*t
src_rows=np.cumsum(w); src_rows=(src_rows-src_rows[0])/(src_rows[-1]-src_rows[0])*Y0
sky=cv2.remap(im[:Y0+2],np.tile(np.arange(W,dtype=np.float32),(newh,1)),np.repeat(src_rows[:,None],W,1).astype(np.float32),cv2.INTER_CUBIC)
sky+=cv2.GaussianBlur(np.random.default_rng(1).normal(0,2.5,sky.shape).astype(np.float32),(0,0),0.7)
full=np.concatenate([sky,im[Y0:]],0)
full=cv2.resize(full,(1080,int(round(full.shape[0]*s))),interpolation=cv2.INTER_AREA)
if full.shape[0]<OH:
    n=OH-full.shape[0]
    if n<=60: full=np.concatenate([full,full[-n-1:-1][::-1]*0.85],0)
    else:   # long gap (story): fade the floor into a dark base instead of mirroring the scene
        last=full[-40:].mean((0,1)); dark=np.array([24,10,5],np.float32)   # BGR deep navy
        t=np.linspace(0,1,n)[:,None,None]; base=last*(1-t)+dark*t
        tail=np.repeat(base,full.shape[1],1)+np.random.default_rng(5).normal(0,2,(n,full.shape[1],3))
        k=np.linspace(1,0,min(80,n))[:,None,None]; tail[:len(k)]=full[-1:]*k+tail[:len(k)]*(1-k)
        full=np.concatenate([full,tail],0)
full=full[:OH]
cv2.imwrite(out,np.clip(full,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,95]); print(full.shape)
