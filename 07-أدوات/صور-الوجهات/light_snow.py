# light snow on the Raouche rocks + subtle winter grade
import cv2,numpy as np,sys
src,out=sys.argv[1],sys.argv[2]
HZ=383
im=cv2.imread(src); H,W=im.shape[:2]
f=im.astype(np.float32)/255; B,G,R=f[...,0],f[...,1],f[...,2]; L=f.mean(2)
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
fs=cv2.GaussianBlur(f,(0,0),1.5); Bs,Gs,Rs=fs[...,0],fs[...,1],fs[...,2]; Ls=fs.mean(2)
rock=(((Rs-Bs>0.08)|((Ls<0.32)&(Rs-Bs>0.01)))&(yy>465)&(yy<1180)&~((xx>1120)&(yy<550))).astype(np.uint8)
rock=cv2.morphologyEx(rock,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
rock=cv2.morphologyEx(rock,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(rock,8)
keep=np.zeros_like(rock)
for i in range(1,n):
    if st[i,4]>6000: keep[lab==i]=1
rock=keep
cv2.imwrite(out.replace('.jpg','_mask.jpg'),cv2.resize(rock*255,None,fx=0.4,fy=0.4))
top=np.full(W,H,np.float32)
for x in range(W):
    ys=np.where(rock[:,x])[0]
    if len(ys): top[x]=ys[0]
top=cv2.GaussianBlur(top.reshape(1,-1),(0,0),1.2).ravel()
dtop=yy-top[None,:]
def smooth_noise(sig,seed):
    r=np.random.default_rng(seed).random((H,W)).astype(np.float32)
    r=cv2.GaussianBlur(r,(0,0),sig); return (r-r.min())/(r.max()-r.min())
nA=smooth_noise(5,1)*0.55+smooth_noise(14,2)*0.45
nF=np.random.default_rng(3).random((H,W)).astype(np.float32)
# plateau depth per region (big rock seen from above has a deep top)
depth=np.where(xx<300,34,np.where(xx<960,80,40)).astype(np.float32)
depth=cv2.GaussianBlur(depth,(0,0),25)
inner=cv2.GaussianBlur(cv2.erode(rock,np.ones((9,9),np.uint8)).astype(np.float32),(0,0),2)
capw=np.clip(1-dtop/depth,0,1)**0.7
cap=np.clip((capw-0.30+(nA-0.5)*1.3)*2.4,0,1)*inner
detail=np.clip(0.8+2.0*(Ls-cv2.GaussianBlur(Ls,(0,0),6)),0.55,1)
cap=cap*detail
# flecks on the upper edges of dark patches and on ledge tops
veg=cv2.GaussianBlur((Ls<0.34).astype(np.float32),(0,0),1.5)
vegtop=np.clip(veg-np.roll(veg,4,axis=0),0,1)*2
led=np.clip((Ls-np.roll(Ls,-3,axis=0))*10,0,1)
fleck=np.clip(vegtop*0.8+led*0.35,0,1)*(nF>0.82)*(0.55+0.45*nA)
fleck=cv2.GaussianBlur(fleck,(0,0),0.6)*inner*np.clip(1-(yy-600)/500,0.25,1)
amt=np.clip(np.maximum(cap,fleck*0.8),0,1)
amt=cv2.GaussianBlur(amt,(0,0),0.6)
shade=np.clip(0.62+0.6*cv2.GaussianBlur(L,(0,0),4),0.66,1.03)[...,None]
snow=np.array([0.975,0.96,0.945],np.float32)*shade
f=f*(1-amt[...,None]*0.82)+snow*amt[...,None]*0.82
# winter grade
f=f*np.array([1.035,1.0,0.955],np.float32)
hsv=cv2.cvtColor(np.clip(f,0,1).astype(np.float32),cv2.COLOR_BGR2HSV); hsv[...,1]*=0.88; f=cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
s=1/(1+np.exp(-(f-0.5)*6)); s=(s-s.min())/(s.max()-s.min()); f=f*0.85+s*0.15
sky=cv2.GaussianBlur((yy<HZ).astype(np.float32),(0,0),3)[...,None]
f=f*(1-0.25*sky)+(f*np.array([1.06,1.0,0.93],np.float32))*0.25*sky
cv2.imwrite(out,np.clip(f*255,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,96])
cv2.imwrite(out.replace('.jpg','_z.jpg'),cv2.imread(out)[430:1150,:])
