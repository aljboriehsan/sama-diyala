import sys,numpy as np
from PIL import Image
kl,fl=float(sys.argv[1]),float(sys.argv[2]); B='/tmp/claude-0/-home-user-sama-diyala/ac5234ca-4a29-5f40-9e89-18987c0271f8/scratchpad/bp/'
def right(path,left):
    a=np.array(Image.open(path).convert('L'))>80; xs=np.where(a.any(0))[0]; return left+(xs.max()+1)/4
k=right(B+'k.png',kl); f=right(B+'f.png',fl); print(round(k,2),round(f,2),'dx',round(f-k,2))
