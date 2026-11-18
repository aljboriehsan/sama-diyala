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
top=np.clip(im[:Y0+2],0,255).astype(np.uint8)
Lt=top.mean(2).astype(np.float32); bgL=cv2.medianBlur(top,15).mean(2).astype(np.float32)
fl=((Lt-bgL)>14).astype(np.uint8); fl=cv2.dilate(fl,np.ones((5,5),np.uint8))
clean=cv2.inpaint(top,fl*255,5,cv2.INPAINT_TELEA).astype(np.float32)
flake=np.clip(im[:Y0+2]-clean,0,None)                        # flakes as a light layer
sky=cv2.remap(clean,mapx,mapy,cv2.INTER_CUBIC)
# put the flakes back round, at their stretched positions
inv=np.interp(np.arange(Y0+2),src_rows,np.arange(newh))      # old row -> new row
n,lab,st,cen=cv2.connectedComponentsWithStats(fl,8)
for i in range(1,n):
    x,y,w,h,a=st[i]
    if a>900: continue
    ny=int(round(inv[min(y+h//2,Y0+1)]))-h//2
    if ny<0 or ny+h>newh: continue
    patch=flake[y:y+h,x:x+w]*(lab[y:y+h,x:x+w]==i)[...,None]
    reg=sky[ny:ny+h,x:x+w]/255; l=patch/255
    sky[ny:ny+h,x:x+w]=(1-(1-reg)*(1-l))*255
# restore fine grain lost by stretching
g=np.random.default_rng(3).normal(0,2.0,sky.shape).astype(np.float32)
sky+=cv2.GaussianBlur(g,(0,0),0.6)
full=np.concatenate([sky,im[Y0:]],0)
s=1080/W; full=cv2.resize(full,(1080,int(round(full.shape[0]*s))),interpolation=cv2.INTER_AREA)[:1350]
cv2.imwrite(out,np.clip(full,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,96]); print(full.shape)
