# Kuala Lumpur photo -> 1080x1350: scale down, widen with mirrored sky/water at the sides, place skyline below the header.
import cv2,numpy as np,sys
src,out,SC,OFF=sys.argv[1],sys.argv[2],float(sys.argv[3]),int(sys.argv[4])
im=cv2.imread(src).astype(np.float32)/255
im=cv2.resize(im,None,fx=SC,fy=SC,interpolation=cv2.INTER_AREA); h,w=im.shape[:2]
pl=(1080-w)//2; pr=1080-w-pl
wide=cv2.copyMakeBorder(im,0,0,pl,pr,cv2.BORDER_REFLECT_101)
x=np.arange(1080,dtype=np.float32); side=np.clip(np.maximum(pl-x,x-(pl+w-1))/max(pl,1),0,1)
wide=wide*(1-0.5*side[None,:,None])+cv2.GaussianBlur(wide,(0,0),4)*(0.5*side[None,:,None])
# extend at the top if the offset leaves a gap
if OFF>0:
    top=np.repeat(wide[:1],OFF,0); wide=np.concatenate([top,wide],0); OFF=0
wide=wide[-OFF:-OFF+1350]
# gentle grade: a touch deeper sky, slight warmth on the city
s=1/(1+np.exp(-(wide-0.5)*6)); s=(s-s.min())/(s.max()-s.min()); wide=wide*0.88+s*0.12
cv2.imwrite(out,np.clip(wide*255,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,95]); print(wide.shape,'img',w,h,'pad',pl)
