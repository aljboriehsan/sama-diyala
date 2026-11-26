# Fill the old 5511 badge area (to the right image edge) with a real cloud patch from the same image.
# Own Poisson/membrane blend: offset = harmonic field matching the original on the top, bottom and left
# borders, free (zero-gradient) at the image's right edge -> no seams, no glow.
import numpy as np, cv2, sys
import scipy.sparse as sp, scipy.sparse.linalg as spl
from PIL import Image
O=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(np.float64)
x0,y0,x1,y1=1256,469,1600,664
hw,hh=x1-x0,y1-y0
src=O[548:685,1000:1262].astype(np.float32)
s=hh/src.shape[0]; pw=int(round(src.shape[1]*s))
pat=cv2.resize(src,(pw,hh),interpolation=cv2.INTER_CUBIC)[:, (pw-hw)//2:(pw-hw)//2+hw].astype(np.float64)
# unknown grid = interior of the hole (rows 1..hh-2, cols 1..hw-1); border rows/col 0 are Dirichlet
ny,nx=hh-2,hw-1
idx=np.arange(ny*nx).reshape(ny,nx)
rows=[];cols=[];vals=[]
def add(r,c,v): rows.append(r);cols.append(c);vals.append(v)
N=ny*nx
B=np.zeros((N,3))
# Dirichlet values (original - patch) on the hole's outer ring
top=O[y0-1+0,x0:x1]-pat[0]*0  # placeholder (unused)
def dval(yy,xx):   # offset at a boundary pixel given in hole coords
    return O[y0+yy,x0+xx]-pat[yy,xx]
for i in range(ny):
    for j in range(nx):
        k=idx[i,j]; yy,xx=i+1,j+1; deg=0
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
            a,b=yy+dy,xx+dx
            if b>=hw: continue                  # image edge: Neumann
            deg+=1
            if a<=0 or a>=hh-1 or b<=0: B[k]+=dval(a,b)
            else: add(k,idx[a-1,b-1],-1)
        add(k,k,deg)
A=sp.csr_matrix((vals,(rows,cols)),shape=(N,N))
lu=spl.splu(A.tocsc())
off=np.zeros((hh,hw,3))
for c in range(3): off[1:hh-1,1:,c]=lu.solve(B[:,c]).reshape(ny,nx)
for yy in (0,hh-1):
    off[yy]=O[y0+yy,x0:x1]-pat[yy]
off[:,0]=O[y0:y1,x0]-pat[:,0]
R=O.copy(); R[y0:y1,x0:x1]=pat+off
Image.fromarray(np.clip(R+.5,0,255).astype(np.uint8)).save(sys.argv[2])
