import numpy as np, cv2
from PIL import Image
from rembg import new_session, remove
from pymatting import estimate_alpha_cf, estimate_foreground_ml
src='/home/user/sama-diyala/08-الصور/طائرة العراقية (الأصل).jpg'
im=Image.open(src).convert('RGB')
x0,y0,x1,y1=100,350,1960,890
cr=im.crop((x0,y0,x1,y1))
s=new_session('isnet-general-use')
# tile-free: run on crop, and on two halves for more resolution, take max
m_full=np.asarray(remove(cr,session=s,only_mask=True)).astype(np.float32)/255
W=cr.width; h=W//2+150
mL=np.asarray(remove(cr.crop((0,0,h,cr.height)),session=s,only_mask=True)).astype(np.float32)/255
mR=np.asarray(remove(cr.crop((W-h,0,W,cr.height)),session=s,only_mask=True)).astype(np.float32)/255
m2=np.zeros_like(m_full); m2[:, :h]=mL; m2[:, W-h:]=np.maximum(m2[:, W-h:],mR)
np.save('m_full.npy',m_full); np.save('m2.npy',m2)
I=np.asarray(cr).astype(np.float64)/255
for n,m in (('full',m_full),('halves',m2)):
    G=np.array([14,77,44])/255
    C=I*m[...,None]+G*(1-m[...,None])
    Image.fromarray((C*255).astype(np.uint8)).save(f'seg_{n}.png')
