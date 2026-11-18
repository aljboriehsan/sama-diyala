import json,sys,numpy as np
from PIL import Image
r=json.loads(sys.argv[1]); a=np.array(Image.open(sys.argv[2]).convert('L')); Z=4
def ink(box,pad=6):
    x0,y0,x1,y1=[int(round(v*Z)) for v in box]; x0-=pad*Z; x1+=pad*Z; y0=max(0,y0-pad*Z); y1+=pad*Z
    sub=a[y0:y1,x0:x1]>60; ys,xs=np.where(sub)
    return np.array([x0+xs.min(),y0+ys.min(),x0+xs.max()+1,y0+ys.max()+1])/Z
L,N,T=ink(r['logo'],0),ink(r['name']),ink(r['tag'])
print('logo',L.round(2)); print('name',N.round(2)); print('tag ',T.round(2))
print('group x',round(min(L[0],N[0]),2),round(max(L[2],N[2]),2),'width',round(max(L[2],N[2])-min(L[0],N[0]),2))
print('tag width',round(T[2]-T[0],2),'dx_left',round(T[0]-min(L[0],N[0]),2),'dx_right',round(T[2]-max(L[2],N[2]),2))
lh=L[3]-L[1]; print('SD center y',round(L[1]+0.588*lh,2),'ring/bars center',round(L[1]+0.68*lh,2),'name center',round((N[1]+N[3])/2,2))
