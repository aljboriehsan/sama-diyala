# Low-res Petra photo -> 1080x1350: careful upscale, light sharpening and grain, sky extended a little at the top.
import cv2,numpy as np,sys
src,out,TOP=sys.argv[1],sys.argv[2],int(sys.argv[3])
im=cv2.imread(src); h,w=im.shape[:2]
s=1080/w
up=cv2.resize(im,(1080,int(round(h*s))),interpolation=cv2.INTER_LANCZOS4).astype(np.float32)/255
den=cv2.bilateralFilter((up*255).astype(np.uint8),5,18,5).astype(np.float32)/255     # tame upscale artefacts
bl=cv2.GaussianBlur(den,(0,0),1.6); up=den+0.55*(den-bl)                               # unsharp
rng=np.random.default_rng(3)
# extend the sky by mirroring the top rows (keeps stars and Milky Way texture), slightly darker and softer upward
mir=up[1:TOP+1][::-1].copy()
k=np.linspace(1.0,0.0,TOP)[:,None,None]                     # 1 at the very top
mir=mir*(1-0.25*k)
soft=cv2.GaussianBlur(mir,(0,0),1.2); mir=mir*(1-0.5*k)+soft*(0.5*k)
full=np.concatenate([mir,up],0)
full+=cv2.GaussianBlur(rng.normal(0,0.012,full.shape).astype(np.float32),(0,0),0.6)   # film grain hides softness
full=full[:1350]
cv2.imwrite(out,np.clip(full*255,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,95]); print(full.shape)
