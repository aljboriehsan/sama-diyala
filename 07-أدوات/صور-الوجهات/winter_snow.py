# Raouche in winter: more (and more physical) snow + a colder grade. Input: levelled photo.
import cv2,numpy as np,sys
src,out=sys.argv[1],sys.argv[2]
HZ=383
im=cv2.imread(src); H,W=im.shape[:2]
f=im.astype(np.float32)/255
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
fs=cv2.GaussianBlur(f,(0,0),1.5); Bs,Gs,Rs=fs[...,0],fs[...,1],fs[...,2]; Ls=fs.mean(2); L=f.mean(2)
rock=(((Rs-Bs>0.08)|((Ls<0.32)&(Rs-Bs>0.01)))&(yy>465)&(yy<1180)&~((xx>1120)&(yy<550))).astype(np.uint8)
rock=cv2.morphologyEx(rock,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
rock=cv2.morphologyEx(rock,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(rock,8)
keep=np.zeros_like(rock)
for i in range(1,n):
    if st[i,4]>6000: keep[lab==i]=1
rock=keep
inner=cv2.GaussianBlur(cv2.erode(rock,np.ones((7,7),np.uint8)).astype(np.float32),(0,0),1.5)
top=np.full(W,H,np.float32); bot=np.zeros(W,np.float32)
for x in range(W):
    ys=np.where(rock[:,x])[0]
    if len(ys): top[x]=ys[0]; bot[x]=ys[-1]
top=cv2.GaussianBlur(top.reshape(1,-1),(0,0),1.2).ravel(); bot=cv2.GaussianBlur(bot.reshape(1,-1),(0,0),3).ravel()
dtop=yy-top[None,:]; rel=np.clip(dtop/np.maximum(bot-top,1)[None,:],0,1)   # 0 at top of rock, 1 at waterline
def sn(sig,seed):
    r=np.random.default_rng(seed).random((H,W)).astype(np.float32); r=cv2.GaussianBlur(r,(0,0),sig)
    return (r-r.min())/(r.max()-r.min())
nA=sn(4,1)*0.5+sn(12,2)*0.35+sn(30,4)*0.15
nF=sn(1.2,3)
# 1) plateau / top surfaces: thick, nearly continuous, bushes poking through
depth=np.where(xx<300,40,np.where(xx<960,95,48)).astype(np.float32); depth=cv2.GaussianBlur(depth,(0,0),25)
capw=np.clip(1.15-dtop/depth,0,1)
nB=sn(1.5,7)
bush=np.clip((0.24-L)/0.08,0,1)*np.clip((nB-0.5)*5,0,1)
cap=np.clip(capw*1.35-0.2+(nA-0.5)*0.7,0,1)*(1-0.85*bush)*(0.82+0.18*nA)
# 2) strata ledges: snow line just above each dark seam (shadow under a ledge)
bh=cv2.morphologyEx(Ls,cv2.MORPH_BLACKHAT,cv2.getStructuringElement(cv2.MORPH_RECT,(1,7)))
gx=cv2.Sobel(Ls,cv2.CV_32F,1,0,ksize=3); gy=cv2.Sobel(Ls,cv2.CV_32F,0,1,ksize=3)
horiz=np.clip((np.abs(gy)-np.abs(gx)*0.8)*12,0,1)
seam=np.clip(bh*14,0,1)*cv2.GaussianBlur(horiz,(0,0),1)
ledge=np.roll(seam,-2,axis=0)                                  # sits on top of the seam
ledge=cv2.GaussianBlur(ledge,(0,0),sigmaX=1.6,sigmaY=0.5)
lvl=np.clip(1.05-rel*1.25,0,1)**1.2                            # more snow higher up, none near the water
ledge=np.clip(ledge*2.8*lvl*(0.45+0.8*nA)*np.clip((nF-0.3)*4,0,1),0,1)*0.8
# 3) shrubs on the faces hold snow on their upper side
veg=cv2.GaussianBlur((Ls<0.30).astype(np.float32),(0,0),1.2)
vegtop=np.clip((veg-np.roll(veg,5,axis=0))*2.2,0,1)
vegdust=np.clip(veg*(nF-0.55)*3.5,0,1)*0.6
shrub=np.clip(vegtop*0.9+vegdust,0,1)*lvl*(0.5+0.5*nA)
amt=np.clip(np.maximum.reduce([cap,ledge,shrub]),0,1)*inner*np.clip((0.86-rel)*8,0,1)
amt=cv2.GaussianBlur(amt,(0,0),0.55)
# snow colour: lit by an overcast sky -> blue-grey in shade, near white on top
lum=cv2.GaussianBlur(L,(0,0),5)
det=Ls-cv2.GaussianBlur(Ls,(0,0),6)
light=np.clip(0.70+0.55*lum+0.18*np.clip(1-dtop/60,0,1)+1.6*det,0.62,1.03)[...,None]
snowc=np.array([0.985,0.955,0.925],np.float32)*light           # BGR, cool
snowc+= (nF[...,None]-0.5)*0.04
f=f*(1-amt[...,None])+snowc*amt[...,None]
# ---- colder grade
f=f*np.array([1.07,1.0,0.90],np.float32)                       # strong cool WB
hsv=cv2.cvtColor(np.clip(f,0,1).astype(np.float32),cv2.COLOR_BGR2HSV); hsv[...,1]*=0.72; f=cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
f=np.clip(f,0,1)**1.05
s=1/(1+np.exp(-(f-0.5)*6)); s=(s-s.min())/(s.max()-s.min()); f=f*0.85+s*0.15
sea=(yy>HZ)&(rock==0); seaw=cv2.GaussianBlur(sea.astype(np.float32),(0,0),3)[...,None]
f=f*(1-0.30*seaw)+(f*np.array([1.0,0.97,0.88],np.float32)*0.93)*0.30*seaw
cv2.imwrite(out,np.clip(f*255,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,96])
cv2.imwrite(out.replace('.jpg','_z.jpg'),cv2.imread(out)[440:1150,:])
