import sys, numpy as np, cv2
from PIL import Image
D=sys.argv[1]
B=cv2.cvtColor(np.asarray(Image.open('09-التصاميم/لوحة الخطوط الجوية العراقية - تعديل الرسمية/أساس - سافر بثقة.png').convert('RGB')),cv2.COLOR_RGB2BGR)
y0,y1,x0,x1=490,655,45,268
g=cv2.cvtColor(B,cv2.COLOR_BGR2GRAY).astype(np.float32)
bg=cv2.medianBlur(g.astype(np.uint8),51).astype(np.float32)
sat=(B.max(2).astype(int)-B.min(2).astype(int))
m=(((B.min(2)>140)&(sat<70))|((g-bg>18)&(sat<90)))[y0:y1,x0:x1].astype(np.uint8)
ff=m.copy()*255; h,w=ff.shape; mk=np.zeros((h+2,w+2),np.uint8); cv2.floodFill(ff,mk,(0,0),128)
m=((ff==255)|(ff==0)).astype(np.uint8)
m=cv2.dilate(m,np.ones((3,3),np.uint8),iterations=5)
M=np.zeros(B.shape[:2],bool); M[y0:y1,x0:x1]=m>0
# local streak orientation from structure tensor in a ring around the hole
ring=cv2.dilate(M.astype(np.uint8),np.ones((41,41),np.uint8)).astype(bool)&~cv2.dilate(M.astype(np.uint8),np.ones((5,5),np.uint8)).astype(bool)
gx=cv2.Sobel(g,cv2.CV_32F,1,0,ksize=5); gy=cv2.Sobel(g,cv2.CV_32F,0,1,ksize=5)
Jxx=cv2.GaussianBlur(gx*gx,(0,0),15); Jyy=cv2.GaussianBlur(gy*gy,(0,0),15); Jxy=cv2.GaussianBlur(gx*gy,(0,0),15)
th=0.5*np.arctan2(2*Jxy,Jxx-Jyy)+np.pi/2      # direction along the streaks
# smooth orientation field into the hole by inpainting cos/sin(2θ)
c2=np.cos(2*th); s2=np.sin(2*th)
Mi=M.astype(np.uint8)*255
def fillf(f):
    lo,hi=f.min(),f.max(); u=((f-lo)/(hi-lo)*255).astype(np.uint8)
    return cv2.inpaint(u,Mi,25,cv2.INPAINT_TELEA).astype(np.float32)/255*(hi-lo)+lo
c2=fillf(c2); s2=fillf(s2); th=0.5*np.arctan2(s2,c2)
print('angle deg in hole', np.degrees(np.median(th[M])))
Bf=B.astype(np.float32); R=Bf.copy()
ys,xs=np.nonzero(M)
for y,x in zip(ys,xs):
    dx,dy=np.cos(th[y,x]),np.sin(th[y,x])
    out=[]
    for sgn in (1,-1):
        t=1
        while t<300:
            xx=int(round(x+sgn*t*dx)); yy=int(round(y+sgn*t*dy))
            if not(0<=xx<B.shape[1] and 0<=yy<B.shape[0]): break
            if not M[yy,xx]:
                # average a few pixels just outside to reduce noise
                xs2=np.clip([xx,int(round(xx+sgn*dx)),int(round(xx+2*sgn*dx))],0,B.shape[1]-1)
                ys2=np.clip([yy,int(round(yy+sgn*dy)),int(round(yy+2*sgn*dy))],0,B.shape[0]-1)
                out.append((t,Bf[ys2,xs2].mean(0))); break
            t+=1
    if len(out)==2:
        (t1,c1),(t2,c2_)=out; R[y,x]=(c1*t2+c2_*t1)/(t1+t2)
    elif out: R[y,x]=out[0][1]
# streaks here are long and almost horizontal: smooth the fill along them to remove swirls/mismatched joins
ang=float(np.median(th[M]))
L=91; k=np.zeros((L,L),np.float32); c=L//2
cv2.line(k,(int(c-c*np.cos(ang)),int(c-c*np.sin(ang))),(int(c+c*np.cos(ang)),int(c+c*np.sin(ang))),1,1); k/=k.sum()
Rs=cv2.filter2D(R,-1,k,borderType=cv2.BORDER_REFLECT)
inner=cv2.GaussianBlur(cv2.erode(M.astype(np.uint8),np.ones((5,5),np.uint8)).astype(np.float32),(0,0),3)[...,None]
R=R*(1-inner)+Rs*inner
rng=np.random.default_rng(2); R[M]+=rng.normal(0,1.8,(M.sum(),3))
wt=cv2.GaussianBlur(M.astype(np.float32),(0,0),1.2)[...,None]
R=Bf*(1-wt)+cv2.GaussianBlur(R,(0,0),0.8)*wt
res=np.clip(R,0,255).astype(np.uint8)
Image.fromarray(cv2.cvtColor(res,cv2.COLOR_BGR2RGB)).save(D+'/أساس العراقية - بلا الشعار السفلي.png')
cv2.imwrite('/tmp/claude-0/-home-user-sama-diyala/ac5234ca-4a29-5f40-9e89-18987c0271f8/scratchpad/inp.png',cv2.resize(np.vstack([B[470:620,20:320],res[470:620,20:320]]),None,fx=2,fy=2))
