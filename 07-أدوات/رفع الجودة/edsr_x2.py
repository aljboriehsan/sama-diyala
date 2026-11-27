import cv2, time, sys
sr=cv2.dnn_superres.DnnSuperResImpl_create(); sr.readModel('EDSR_x2.pb'); sr.setModel('edsr',2)
img=cv2.imread(sys.argv[1]); t=time.time()
# tile to keep memory sane
h,w=img.shape[:2]; T=360; P=16
out=None
import numpy as np
out=np.zeros((h*2,w*2,3),np.uint8)
for y in range(0,h,T):
    for x in range(0,w,T):
        y0,x0=max(0,y-P),max(0,x-P); y1,x1=min(h,y+T+P),min(w,x+T+P)
        r=sr.upsample(img[y0:y1,x0:x1])
        oy,ox=(y-y0)*2,(x-x0)*2; th,tw=min(T,h-y)*2,min(T,w-x)*2
        out[y*2:y*2+th,x*2:x*2+tw]=r[oy:oy+th,ox:ox+tw]
cv2.imwrite(sys.argv[2],out); print('done',time.time()-t,out.shape)
