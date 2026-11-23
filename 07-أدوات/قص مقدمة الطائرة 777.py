import cv2,numpy as np
im=cv2.imread('/home/user/sama-diyala/08-الصور/طائرة العراقية (الأصل).jpg'); f=im.astype(np.float32); H,W=im.shape[:2]
def cr(pts,n=12):   # Catmull-Rom through points
    P=np.array(pts,np.float32); P=np.vstack([P[0],P,P[-1]]); out=[]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for t in np.linspace(0,1,n,endpoint=False):
            out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t**3))
    out.append(P[-2]); return np.array(out)
X1=708
top=cr([(129,624),(130,615),(134,608),(140,603),(150,598),(160,594),(170,590),(185,578),(200,566),(250,555),(300,546),(350,541),(400,539.5),(450,540),(500,542),(550,545),(600,548),(650,550.5),(X1,553)])
bot=cr([(129,627),(133,633),(140,638),(150,645),(170,654),(200,665),(230,676),(262,686),(300,694.5),(360,702),(420,708),(500,712),(600,717.5),(X1,722)])
poly=np.vstack([top,bot[::-1]])
S=4; big=np.zeros((H*S,W*S),np.uint8)
cv2.fillPoly(big,[np.round(poly*S).astype(np.int32)],255,lineType=cv2.LINE_AA)
door=np.array([(251,676),(297,686),(298,703),(245,700)],np.float32)
cv2.fillPoly(big,[np.round(door*S).astype(np.int32)],255,lineType=cv2.LINE_AA)
m=cv2.resize(big.astype(np.float32)/255,(W,H),interpolation=cv2.INTER_AREA)
lum=cv2.GaussianBlur(f,(0,0),0.8).mean(-1); sky=np.median(lum[740:780,320:420])
gear=(lum<sky-16).astype(np.uint8); z=np.zeros_like(gear); z[698:778,258:310]=1; gear*=z
gear=cv2.morphologyEx(gear,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
n,l,st,_=cv2.connectedComponentsWithStats(gear); gm=np.zeros_like(gear)
for i in range(1,n):
    if st[i,4]>25: gm[l==i]=1
gm=cv2.resize(cv2.resize(gm.astype(np.float32),(W*4,H*4),interpolation=cv2.INTER_LINEAR),(W,H),interpolation=cv2.INTER_AREA)
gm=cv2.GaussianBlur(gm,(0,0),0.6)
a=np.clip(np.maximum(m,gm),0,1)
# shrink the traced edge by ~0.6px so no sky line survives on the rim
a=np.clip((a-0.25)/0.75,0,1)
ys,xs=np.where(a>0.02); x0,y0,x1,y1=xs.min()-2,ys.min()-2,xs.max()+3,ys.max()+3
rgba=np.dstack([f,a*255]).clip(0,255).astype(np.uint8)[y0:y1,x0:x1]
cv2.imwrite('/home/user/sama-diyala/08-الصور/طائرة العراقية 777 - المقدمة (مفرغة).png',rgba); print(rgba.shape,(x0,y0))
for name,bgc in [('n_light.jpg',(242,247,243)),('n_dark.jpg',(44,77,14))]:
    al=rgba[...,3:]/255.; c=(rgba[...,:3]*al+np.array(bgc,np.float32)*(1-al)).astype(np.uint8)
    cv2.imwrite(name,cv2.resize(c,None,fx=1.5,fy=1.5,interpolation=cv2.INTER_CUBIC))
