# Fit the approved Beirut photo to the ad template without moving anything:
# stretch the upper clouds (rows above the fireworks) so the firework and the rocks sit below the header.
import cv2,numpy as np,sys
src,out,EXT=sys.argv[1],sys.argv[2],int(sys.argv[3])
im=cv2.imread(src).astype(np.float32); H,W=im.shape[:2]
Y0=318                                   # first firework spark is at ~340
newh=Y0+EXT
t=np.linspace(0,1,newh)
w=0.35+0.65*t                            # stretch strongest at the very top, none at Y0
src_rows=np.cumsum(w); src_rows=(src_rows-src_rows[0])/(src_rows[-1]-src_rows[0])*Y0
mapx=np.tile(np.arange(W,dtype=np.float32),(newh,1)); mapy=np.repeat(src_rows[:,None],W,1).astype(np.float32)
sky=cv2.remap(im[:Y0+2],mapx,mapy,cv2.INTER_CUBIC)
# restore fine grain lost by stretching
g=np.random.default_rng(3).normal(0,2.0,sky.shape).astype(np.float32)
sky+=cv2.GaussianBlur(g,(0,0),0.6)
full=np.concatenate([sky,im[Y0:]],0)
s=1080/W; full=cv2.resize(full,(1080,int(round(full.shape[0]*s))),interpolation=cv2.INTER_AREA)[:1350]
cv2.imwrite(out,np.clip(full,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,96]); print(full.shape)
