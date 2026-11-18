# Light grade for destination photos that are already right (no time-of-day change):
# gentle contrast, a little lift in the shadows, mild saturation, slight local contrast.
import cv2,numpy as np,sys
src,out=sys.argv[1],sys.argv[2]
im=cv2.imread(src).astype(np.float32)/255
im=np.clip(im,0,1)**0.94                                  # lift mids/shadows slightly
s=1/(1+np.exp(-(im-0.5)*6)); s=(s-s.min())/(s.max()-s.min())
im=im*0.82+s*0.18                                          # gentle contrast
blur=cv2.GaussianBlur(im,(0,0),18); im=im+0.12*(im-blur)    # local contrast
hsv=cv2.cvtColor(np.clip(im,0,1).astype(np.float32),cv2.COLOR_BGR2HSV)
hsv[...,1]=np.clip(hsv[...,1]*1.06,0,1)
im=cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
cv2.imwrite(out,np.clip(im*255,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,95])
