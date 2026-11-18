# fit the photo to 1080x1350: scale to width, extend the plain sky upward so the rocks sit below the header
import cv2,numpy as np,sys
src,out,ext=sys.argv[1],sys.argv[2],int(sys.argv[3])
im=cv2.imread(src).astype(np.float32); H,W=im.shape[:2]
s=1080/W; im=cv2.resize(im,(1080,int(round(H*s))),interpolation=cv2.INTER_AREA)
h=im.shape[0]
top=im[:80]; rowmean=top.mean(1)                       # 80 x 3
y=np.arange(80); k=np.polyfit(y,rowmean,1)             # per-channel linear trend
yy=np.arange(-ext,0)[:,None]
grad=(k[0][None,:]*yy+k[1][None,:])                    # extrapolate
grad=grad*0.6+rowmean[:10].mean(0)*0.4                 # keep it gentle
colvar=(top-rowmean[:,None,:]).mean(0)                 # horizontal variation of the top rows
add=np.repeat(grad[:,None,:],1080,1)+colvar[None]
rng=np.random.default_rng(2); noise=top-cv2.GaussianBlur(top,(0,0),2)
tile=np.concatenate([noise]*(ext//80+1),0)[:ext]
add+=tile*0.9
full=np.concatenate([add,im],0)[:1350]
cv2.imwrite(out,np.clip(full,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,96])
print('scaled h',h,'total',ext+h)
