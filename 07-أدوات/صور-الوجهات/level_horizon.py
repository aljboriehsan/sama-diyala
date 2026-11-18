# level the horizon and crop to the largest clean rectangle
import cv2,numpy as np,sys
src,out,ang=sys.argv[1],sys.argv[2],float(sys.argv[3])
im=cv2.imread(src); H,W=im.shape[:2]
M=cv2.getRotationMatrix2D((W/2,H/2),ang,1.0)
r=cv2.warpAffine(im,M,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT,borderValue=0)
ones=cv2.warpAffine(np.full((H,W),255,np.uint8),M,(W,H),flags=cv2.INTER_NEAREST)
mx,my=0,0
while ones[my:H-my,mx:W-mx].min()==0:
    mx+=1; my=int(round(mx*H/W))
r=r[my+1:H-my-1,mx+1:W-mx-1]
cv2.imwrite(out,r,[cv2.IMWRITE_JPEG_QUALITY,97]); print(r.shape)
g=cv2.GaussianBlur(r.mean(2).astype(np.float32),(0,0),sigmaX=12,sigmaY=1.5); gy=np.diff(g,axis=0)
for x in (40,100,1000,1300,1450):
    if x<r.shape[1]: print(x,330+int(np.argmax(-gy[330:480,x])))
