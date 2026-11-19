# square poster -> 1080x1350: stretch the clouds above the minaret tips by EXT frame px, mirror the floor at the bottom if needed
import cv2,numpy as np,sys
src,out,EXTF=sys.argv[1],sys.argv[2],int(sys.argv[3])
im=cv2.imread(src).astype(np.float32); H,W=im.shape[:2]; s=1080/W
Y0=270; EXT=int(round(EXTF/s))
newh=Y0+EXT; t=np.linspace(0,1,newh); w=0.25+0.75*t
src_rows=np.cumsum(w); src_rows=(src_rows-src_rows[0])/(src_rows[-1]-src_rows[0])*Y0
sky=cv2.remap(im[:Y0+2],np.tile(np.arange(W,dtype=np.float32),(newh,1)),np.repeat(src_rows[:,None],W,1).astype(np.float32),cv2.INTER_CUBIC)
sky+=cv2.GaussianBlur(np.random.default_rng(1).normal(0,2.5,sky.shape).astype(np.float32),(0,0),0.7)
full=np.concatenate([sky,im[Y0:]],0)
full=cv2.resize(full,(1080,int(round(full.shape[0]*s))),interpolation=cv2.INTER_AREA)
if full.shape[0]<1350:
    n=1350-full.shape[0]; full=np.concatenate([full,full[-n-1:-1][::-1]*0.85],0)
full=full[:1350]
cv2.imwrite(out,np.clip(full,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,95]); print(full.shape)
