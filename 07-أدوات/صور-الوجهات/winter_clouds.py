# winter sky: broken soft clouds over a cool grey-blue sky, in perspective, above a known horizon
import cv2,numpy as np,sys
src,out,HZ=sys.argv[1],sys.argv[2],int(sys.argv[3])
im=cv2.imread(src).astype(np.float32)/255; H,W=im.shape[:2]
rng=np.random.default_rng(int(sys.argv[4]) if len(sys.argv)>4 else 21)
TW,TH=3000,3000
def fbm(base_w,base_h,octs,pers):
    t=np.zeros((TH,TW),np.float32); a=1; tot=0
    for o in range(octs):
        g=rng.random((base_h*2**o,base_w*2**o)).astype(np.float32)
        t+=cv2.resize(g,(TW,TH),interpolation=cv2.INTER_CUBIC)*a; tot+=a; a*=pers
    t/=tot; return (t-t.min())/(t.max()-t.min())
n=fbm(7,7,5,0.5)
wx=fbm(4,4,3,0.5); wy=fbm(4,4,3,0.5)
gx,gy=np.meshgrid(np.arange(TW,dtype=np.float32),np.arange(TH,dtype=np.float32))
n=cv2.remap(n,gx+(wx-0.5)*300,gy+(wy-0.5)*300,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
y=np.arange(HZ,dtype=np.float32); d=HZ-y+12
F=1500.0; h=0.75*(HZ+12)                       # ~0.75 texture px per screen px at the top edge
v=h*F/d; v=v-v.min()+200
u_s=h/d
mapy=np.repeat(v[:,None],W,1).astype(np.float32)
xs=np.arange(W,dtype=np.float32)
mapx=((xs[None,:]-W/2)*u_s[:,None]+TW/2).astype(np.float32)
c=cv2.remap(n,mapx,np.mod(mapy,2*TH-2),cv2.INTER_AREA if False else cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
cover=cv2.GaussianBlur(np.clip((c-0.41)/0.24,0,1)**1.2,(0,0),1.4)
dens=cv2.GaussianBlur(cover,(0,0),5)
shade=np.clip((dens-np.roll(dens,-14,axis=0))*2.2,-1,1)      # lit tops (cloud above is thinner)
t=(y/HZ)[:,None,None]
sky_b=np.array([0.79,0.72,0.65])*(1-t)+np.array([0.86,0.82,0.78])*t        # BGR cool grey-blue
cl_top=np.array([0.95,0.94,0.93]); cl_base=np.array([0.70,0.67,0.65])
cl=cl_base+(cl_top-cl_base)*np.clip(0.55+0.9*shade,0,1)[...,None]
sky=sky_b*(1-cover[...,None])+cl*cover[...,None]
haze=np.clip(1-d/170,0,1)[:,None,None]
sky=sky*(1-haze*0.75)+np.array([0.87,0.85,0.83])*haze*0.75
w=np.ones((HZ,W,1),np.float32); w[-6:]=np.linspace(1,0,6)[:,None,None]
orig=im[:HZ]; grain=orig-cv2.GaussianBlur(orig,(0,0),1.5)
im[:HZ]=orig*(1-w)+(sky+grain*0.8)*w
cv2.imwrite(out,np.clip(im*255,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,96])
# final cool push on the whole frame
im2=cv2.imread(out).astype(np.float32)/255
im2=im2*np.array([1.03,1.0,0.955],np.float32)
cv2.imwrite(out,np.clip(im2*255,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,96])
