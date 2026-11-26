import numpy as np, cv2
from PIL import Image
a=np.load('a.npy'); F=np.load('F.npy').copy()
a=np.clip((a-0.12)/0.83,0,1)               # slight choke: crisp edge, no sky veil
core=(a>0.98).astype(np.uint8)
inner=cv2.erode(core,np.ones((3,3),np.uint8),iterations=4)
rim=(a>0)&(inner==0)                        # outer 4-5 px band
r,g,b=F[...,0],F[...,1],F[...,2]
mx=np.maximum(r,g)
ex=np.clip(b-mx-0.01,0,None)
# despill the rim: remove blue excess, push to neutral luminance
b2=np.where(rim,b-ex,b)
F[...,2]=b2
# also darken-navy rim pixels -> neutral grey of same luminance
L=0.3*r+0.59*g+0.11*F[...,2]
navy=rim&(b-mx>0.02)
for c in range(3): F[...,c]=np.where(navy,L,F[...,c])
a=cv2.GaussianBlur(a.astype(np.float32),(0,0),0.6)
a[a<0.02]=0
rgba=np.dstack([np.clip(F,0,1),a])
ys,xs=np.nonzero(a>0.01); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
rgba=rgba[max(0,y0-4):y1+4,max(0,x0-4):x1+4]
im=Image.fromarray((rgba*255+.5).astype(np.uint8),'RGBA')
im.save('plane.png'); print(im.size, 'rim px',rim.sum(),'navy',navy.sum())
G=np.array([14,77,44])/255
C=rgba[...,:3]*rgba[...,3:]+G*(1-rgba[...,3:])
ci=Image.fromarray((C*255).astype(np.uint8))
for n,(x,y,w,h) in {'z1':(850,370,520,240),'z2':(10,110,420,220),'z3':(1290,240,520,330),'z4':(470,10,400,320)}.items():
  ci.crop((x,y,x+w,y+h)).resize((w*2,h*2),Image.LANCZOS).save(n+'.png')
ci.save('comp.png')
