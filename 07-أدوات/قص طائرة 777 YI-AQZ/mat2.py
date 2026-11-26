import numpy as np, cv2
from PIL import Image
from pymatting import estimate_alpha_cf, estimate_foreground_ml
src='/home/user/sama-diyala/08-الصور/طائرة العراقية (الأصل).jpg'
full=np.asarray(Image.open(src).convert('RGB'))
x0,y0,x1,y1=100,350,1960,890
I8=full[y0:y1,x0:x1]; I=I8.astype(np.float64)/255
m=np.maximum(np.load('m_full.npy'),np.load('m2.npy'))
# sky estimate: inpaint plane area (generous) at low res
k=np.ones((3,3),np.uint8)
plane=(m>0.03).astype(np.uint8); plane=cv2.dilate(plane,k,iterations=12)
sm=cv2.resize(I8,None,fx=.25,fy=.25,interpolation=cv2.INTER_AREA); pm=cv2.resize(plane,(sm.shape[1],sm.shape[0]),interpolation=cv2.INTER_NEAREST)
Bs=cv2.inpaint(sm,pm*255,15,cv2.INPAINT_TELEA); Bs=cv2.GaussianBlur(Bs,(0,0),6)
B=cv2.resize(Bs,(I8.shape[1],I8.shape[0]),interpolation=cv2.INTER_CUBIC).astype(np.float64)/255
d=np.linalg.norm(I-B,axis=2)*255
np.save('d.npy',d); np.save('B.npy',B)
fg=((m>0.97)&(d>8)).astype(np.uint8); fg=cv2.erode(fg,k,iterations=3)
bg=((m<0.03)|((d<7)&(m<0.9))).astype(np.uint8); bg=cv2.erode(bg,k,iterations=2)
tri=np.full(m.shape,0.5); tri[bg==1]=0; tri[fg==1]=1
print('unknown',(tri==.5).sum())
a=np.clip(estimate_alpha_cf(I,tri),0,1)
F=estimate_foreground_ml(I,a)
np.save('a.npy',a); np.save('F.npy',F)
G=np.array([14,77,44])/255
C=F*a[...,None]+G*(1-a[...,None])
Image.fromarray((C*255).astype(np.uint8)).save('comp.png')
cv2.imwrite('tri.png',(tri*255).astype(np.uint8))
