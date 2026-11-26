import numpy as np, cv2
from PIL import Image
src='/home/user/sama-diyala/08-الصور/طائرة العراقية YI-ASU (سماء زرقاء).jpg'
I=np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
H,W,_=I.shape
# conservative sky sample: blue-dominant and close to border-sampled color
b=I[...,2]; r=I[...,0]; g=I[...,1]
cand=(b-np.maximum(r,g)>22)&(b>140)
ys,xs=np.nonzero(cand[::4,::4]); ys*=4; xs*=4
# fit quadratic per channel
X=np.stack([np.ones_like(xs),xs/W,ys/H,(xs/W)**2,(ys/H)**2,xs*ys/(W*H)],1).astype(np.float64)
yy,xx=np.mgrid[0:H,0:W]
XF=np.stack([np.ones(H*W),xx.ravel()/W,yy.ravel()/H,(xx.ravel()/W)**2,(yy.ravel()/H)**2,xx.ravel()*yy.ravel()/(W*H)],1)
B=np.zeros_like(I)
for c in range(3):
    coef,*_=np.linalg.lstsq(X,I[ys,xs,c],rcond=None)
    B[...,c]=(XF@coef).reshape(H,W)
res=np.abs(I[cand]-B[cand]).mean(0); print('sky residual',res, 'sky mean',B[H//2,W//2])
d=np.linalg.norm(I-B,axis=2)
np.save('B.npy',B); np.save('d.npy',d)
cv2.imwrite('d.png',np.clip(d*4,0,255).astype(np.uint8))
print(np.percentile(d[cand],[50,99,99.9]))
