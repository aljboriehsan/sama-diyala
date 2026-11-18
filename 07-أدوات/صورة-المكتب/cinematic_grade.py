# Cinematic, clean grade for the office photo (see CLAUDE.md): brighter mids with whites kept,
# firm contrast, green-tinted shadows and warm highlights, warm key light on the counter,
# glow on the ceiling lights and the green LED strips, soft vignette.
import cv2,numpy as np,sys
src,out=sys.argv[1],sys.argv[2]
G=float(sys.argv[3]) if len(sys.argv)>3 else 0.70     # gamma (<1 brightens mids); used: 0.70
C=float(sys.argv[4]) if len(sys.argv)>4 else 0.42     # S-curve strength; used: 0.42
im=cv2.imread(src).astype(np.float32)/255.0
H,W=im.shape[:2]
ref=np.median(im[560:640,1300:1500].reshape(-1,3),0)
im=np.clip(im*(ref.mean()/ref),0,1)                    # neutral walls
im=im**G                                               # brighten mids, whites stay put
s=1/(1+np.exp(-(im-0.5)*8)); s=(s-s.min())/(s.max()-s.min())
im=im*(1-C)+s*C                                        # contrast
L=im.mean(2,keepdims=True)
sh=np.clip(1-L/0.5,0,1); hl=np.clip((L-0.6)/0.4,0,1)
im=im+sh*np.array([0.010,0.022,-0.004],np.float32)*1.0   # BGR: green-teal shadows
im=im*(1+hl*np.array([-0.035,0.0,0.03],np.float32))      # warm highlights
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
key=np.exp(-(((xx-1480)/600)**2+((yy-740)/420)**2))[...,None]
im=im*(1+0.10*key)*(1+key*np.array([-0.035,0.0,0.03],np.float32))
# glow
mx=im.max(2,keepdims=True)
br=np.clip((mx-0.86)/0.14,0,1)*im
gr=((im[...,1:2]-im[...,2:3])>0.08)*np.clip((im[...,1:2]-0.45)/0.4,0,1)*im   # green LED light
glow=cv2.GaussianBlur(br,(0,0),10)*0.8+cv2.GaussianBlur(br,(0,0),35)*0.6+cv2.GaussianBlur(gr,(0,0),22)*0.9
im=1-(1-np.clip(im,0,1))*(1-np.clip(glow,0,1)*0.6)
# vignette
v=1-0.20*(((xx-1350)/1200)**2+((yy-640)/800)**2)
im*=np.clip(v,0.74,1)[...,None]
im=im.astype(np.float32)
blur=cv2.GaussianBlur(im,(0,0),20); im=im+0.15*(im-blur)
hsv=cv2.cvtColor(np.clip(im,0,1),cv2.COLOR_BGR2HSV); hsv[...,1]=np.clip(hsv[...,1]*1.08,0,1); im=cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
cv2.imwrite(out,np.clip(im*255,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,96])
