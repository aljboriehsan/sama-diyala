# Remove the wall fan (and its bracket and cords) above the desks.
import cv2,numpy as np,sys
src,out,S=sys.argv[1],sys.argv[2],sys.argv[3]
im=cv2.imread(src); H,W=im.shape[:2]
m=np.zeros((H,W),np.uint8)
grille=np.array([(1064,512),(1080,529),(1102,524),(1137,502),(1162,480),(1163,456),(1150,452),(1118,460),(1088,478),(1068,498)],np.int32)
cv2.fillPoly(m,[grille],255)
cv2.rectangle(m,(1084,452),(1118,494),255,-1)    # motor
cv2.rectangle(m,(1056,470),(1074,532),255,-1)    # bracket
cv2.rectangle(m,(1068,478),(1096,498),255,-1)    # arm
cv2.rectangle(m,(1058,528),(1071,586),255,-1)    # cords
m=cv2.dilate(m,np.ones((5,5),np.uint8))
f=im.astype(np.float32); rng=np.random.default_rng(3)
EDGE0,EDGE1=1126,1135
M=(m>0)
def colcopy(sel,yref_fn,rowref=None):
    for x in np.where(sel.any(0))[0]:
        ys=np.where(sel[:,x])[0]; yr=yref_fn(x)
        base=np.median(f[yr-2:yr+3,x],0)
        for y in ys:
            adj=(rowref(y)-rowref(yr)) if rowref is not None else 0
            f[y,x]=base+adj+rng.normal(0,1.0,3)
ref=lambda y: np.median(f[y,1168:1176],0)
below=lambda x: int(np.where(~M[:,x] & (np.arange(H)>480))[0][0])+3
# 1) wall right of the pillar and the pillar's right edge: copy each column from just below the fan
sel=M.copy(); sel[:, :EDGE0]=False; colcopy(sel,below,ref)
# 2) pillar front strip and the panel's left edge: copy each column from just above the bracket,
#    shifting brightness row by row to follow the visible part of the pillar front
_fr=np.median(f[:,1041:1050],1); _fr=cv2.GaussianBlur(_fr[None],(0,0),sigmaX=0.1,sigmaY=0)[0]
_fr=np.stack([np.convolve(np.pad(_fr[:,c],12,mode='edge'),np.ones(25)/25,'valid') for c in range(3)],1)
fr=lambda y: _fr[y]
sel=M.copy(); sel[:, :1048]=False; sel[:, 1083:]=False; sel[526:]=False; colcopy(sel,lambda x:449,fr)
# 2b) cords over the poster's left margin: copy from just below them
sel=M.copy(); sel[:541]=False; sel[:, 1083:]=False; colcopy(sel,lambda x:593)
done=M.copy(); done[:, EDGE0:]=False
keep=np.zeros_like(done); keep[:526,1048:1080]=True; keep[541:,1048:1080]=True
done&=~keep          # inpaint the panel, the strip where pillar meets poster, and the seam at x~1080
# 3) wood and poster: inpaint, then restore a little vertical grain on the wood
rest=done
tmp=np.clip(f,0,255).astype(np.uint8)
inp=cv2.inpaint(tmp,rest.astype(np.uint8)*255,7,cv2.INPAINT_TELEA).astype(np.float32)
grain=cv2.GaussianBlur(rng.normal(0,1,(1,W)).astype(np.float32),(0,0),1.2)*5
wood=rest.copy(); wood[530:]=False
inp[wood]+=np.repeat(grain,H,0)[wood][:,None]
f[rest]=inp[rest]
blk=np.zeros((H,W),np.float32); blk[452:527,1046:1084]=1
blk=cv2.GaussianBlur(blk,(0,0),2.5)*(M>0)
f=f*(1-blk[...,None])+cv2.GaussianBlur(f,(0,0),1.2)*blk[...,None]*0+f*blk[...,None]*1
res=np.clip(f,0,255).astype(np.uint8)
cv2.imwrite(out,res,[cv2.IMWRITE_JPEG_QUALITY,97])
cv2.imwrite(S+'/fan/cmp.png',np.hstack([cv2.resize(im[420:610,1010:1200],None,fx=3,fy=3,interpolation=cv2.INTER_CUBIC),cv2.resize(res[420:610,1010:1200],None,fx=3,fy=3,interpolation=cv2.INTER_CUBIC)]))
