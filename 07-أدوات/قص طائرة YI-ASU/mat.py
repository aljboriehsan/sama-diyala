import numpy as np, cv2, time
from PIL import Image
from pymatting import estimate_alpha_cf, estimate_foreground_ml
src='/home/user/sama-diyala/08-الصور/طائرة العراقية YI-ASU (سماء زرقاء).jpg'
I=np.asarray(Image.open(src).convert('RGB')).astype(np.float64)/255
d=np.load('d.npy'); B=np.load('B.npy')/255
y0,y1,x0,x1=300,920,95,1915
I=I[y0:y1,x0:x1]; d=d[y0:y1,x0:x1]; B=B[y0:y1,x0:x1]
fg=(d>42).astype(np.uint8)
# keep fg components attached to the plane (largest), drop specks
n,lab,st,_=cv2.connectedComponentsWithStats(fg,8)
keep=np.zeros_like(fg)
for i in range(1,n):
    if st[i,4]>400: keep[lab==i]=1
fg=cv2.erode(keep,np.ones((3,3),np.uint8),1)
bg=(d<9).astype(np.uint8)
bg=cv2.erode(bg,np.ones((3,3),np.uint8),1)
tri=np.full(d.shape,0.5); tri[bg==1]=0; tri[fg==1]=1
print('unknown px',(tri==0.5).sum())
t=time.time(); a=estimate_alpha_cf(I,tri); print('cf',time.time()-t)
a=np.clip(a,0,1)
# remove isolated low-alpha noise in sky
a[(d<12)&(a<0.35)]=0
F=estimate_foreground_ml(I,a)
np.save('a.npy',a); np.save('F.npy',F)
