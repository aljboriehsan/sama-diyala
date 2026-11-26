import numpy as np, cv2
from PIL import Image
from pymatting import estimate_foreground_ml
src='/home/user/sama-diyala/08-الصور/طائرة العراقية (الأصل).jpg'
I=np.asarray(Image.open(src).convert('RGB').crop((100,350,1960,890))).astype(np.float64)/255
m=np.maximum(np.load('m_full.npy'),np.load('m2.npy'))
a=np.load('a.npy'); d=np.load('d.npy')
H,W=a.shape
# fuselage top edge from the clean parts of the model mask
xs=[];ys=[]
for x in list(range(200,540,4))+list(range(1260,1420,4)):
    col=m[150:300,x]>0.5
    for i in range(len(col)-8):
        if col[i:i+8].all(): xs.append(x); ys.append(150+i); break
xs=np.array(xs);ys=np.array(ys)
c=np.polyfit(xs,ys,2); print('fit resid',np.abs(np.polyval(c,xs)-ys).mean(), [round(np.polyval(c,x),1) for x in (560,800,1080)])
yy,xx=np.mgrid[0:H,0:W]
top=np.polyval(c,xx)
step=np.clip(yy-top+0.5,0,1)
Z=(xx>=330)&(xx<=1445)&(yy>=120)&(yy<=268)
aZ=np.where(d<11,0,a)
a2=a.copy(); a2[Z]=np.maximum(step,aZ)[Z]
# wing leading edge: straight line fitted on the model mask, light edge strip kept
lx=[];ly=[]
for x in range(960,1390,4):
    col=m[0:260,x]>0.5
    for i in range(len(col)-6):
        if col[i:i+6].all(): lx.append(x); ly.append(i); break
lc=np.polyfit(lx,ly,1); print('lead resid',np.abs(np.polyval(lc,lx)-np.array(ly)).mean(),lc)
lead=np.polyval(lc,xx)
WZ=(xx>=760)&(xx<=1372)&(yy<top-1)
band=WZ&(yy>lead-8)&(yy<lead+7)
wstep=np.clip(yy-lead+0.5,0,1)
a2[band]=np.maximum(np.where(yy<lead+1,0,a2),wstep)[band]
a2[WZ&(yy<lead-0.5)&(d<14)]=0
# vertical fin: straight leading/trailing edges and top from the model mask
L=[];R=[];Ys=[]
for y in range(45,200,3):
    row=np.nonzero(m[y,1440:1780]>0.5)[0]
    if len(row): Ys.append(y); L.append(1440+row[0]); R.append(1440+row[-1])
Ys=np.array(Ys)
cl=np.polyfit(Ys,L,1); cr=np.polyfit(Ys,R,1)
print('fin resid',np.abs(np.polyval(cl,Ys)-L).mean(),np.abs(np.polyval(cr,Ys)-R).mean())
tops=[]
for x in range(1705,1732,2):
    col=np.nonzero(m[0:80,x]>0.5)[0]
    if len(col): tops.append((x,col[0]))
tx,ty=np.array(tops).T; ct=np.polyfit(tx,ty,1)
fin=np.clip(xx-np.polyval(cl,yy)+0.5,0,1)*np.clip(np.polyval(cr,yy)-xx+0.5,0,1)*np.clip(yy-np.polyval(ct,xx)+0.5,0,1)
FZ=(yy<238)&(xx>1432)&(xx<1800)
a2[FZ]=fin[FZ]
rf=np.clip(np.polyval(cr,yy)-xx+0.5,0,1)
FZ2=(yy>=238)&(yy<243)&(xx>np.polyval(cl,yy)+4)&(xx<1800)
a2[FZ2]=np.minimum(a2,rf)[FZ2]
print('top',ct)
np.save('a2.npy',a2)
F=estimate_foreground_ml(I,a2); np.save('F2.npy',F)
G=np.array([14,77,44])/255
C=F*a2[...,None]+G*(1-a2[...,None])
ci=Image.fromarray((C*255).astype(np.uint8)); ci.save('comp2.png')
for n,(x,y,w,h) in {'h1':(480,140,700,160),'h2':(1050,20,420,200),'h3':(780,330,280,200),'h4':(1450,10,400,330)}.items():
  ci.crop((x,y,x+w,y+h)).resize((w*2,h*2),Image.LANCZOS).save(n+'.png')
