from itertools import product
from math import sqrt
from collections import defaultdict
import json

FDS=((1.,.5,2.),(.5,1.,2.))
def avg(a): return sum(a)/len(a)
def flux(a,b,fd):
    v,w,c=fd
    return min(v*a,c,w*(6-b))
def local(k,fd): return avg([flux(x,k[(i+1)%4],fd) for i,x in enumerate(k)])
def hom(k,fd): return flux(avg(k),avg(k),fd)
def hist(k,fd): return avg([flux(a,b,fd) for i,a in enumerate(k) for j,b in enumerate(k) if i!=j])
def step(k,fd):
    f=[flux(x,k[(i+1)%4],fd) for i,x in enumerate(k)]
    z=[x+f[i-1]-f[i] for i,x in enumerate(k)]
    assert all(-1e-9<=x<=6+1e-9 for x in z) and abs(sum(k)-sum(z))<1e-8
    return z
def traj(k,fd):
    a=[k]
    for _ in range(8): a.append(step(a[-1],fd))
    return a
def obs(k,m): return [max(0,min(6,x+s)) for x,s in zip(k,m)]
def add(d,key,e):
    a=d[key];a[0]+=1;a[1]+=e;a[2]+=abs(e);a[3]+=e*e;a[4]=max(a[4],abs(e))
def report(d): return {k:dict(n=a[0],signed=a[1],abs=a[2],sq=a[3],max=a[4],bias=a[1]/a[0],MAE=a[2]/a[0],RMSE=sqrt(a[3]/a[0])) for k,a in d.items()}
def b0():
    d=defaultdict(lambda:[0,0.,0.,0.,0.]); truth=forecast=alternate=checks=0
    for k in product((0,2,4,6),repeat=4):
        for i,fd in enumerate(FDS):
            z=traj(k,fd); other=traj(k,FDS[1-i]);truth+=1;alternate+=1
            for t,x in enumerate(z):
                y=local(x,fd)
                for name,p in [('local',y),('mean',hom(x,fd)),('hist',hist(x,fd)),('alternate',local(other[t],FDS[1-i]))]:add(d,'exact/'+name,p-y)
            for ch,ms in [('independent',list(product((-1,1),repeat=4))),('common',[(-1,)*4,(1,)*4])]:
                for m in ms:
                    p=traj(obs(k,m),fd);forecast+=1
                    for t,x in enumerate(z):
                        y=local(x,fd);o=obs(x,m)
                        assert abs(local(o,fd)-y)<=sum(fd[:2])*avg([abs(a-b) for a,b in zip(x,o)])+1e-9;checks+=1
                        for name,v in [('local',local(o,fd)),('mean',hom(o,fd)),('hist',hist(o,fd)),('forecast',local(p[t],fd))]:add(d,ch+'/'+name,v-y)
    assert (truth,forecast,alternate,checks)==(512,9216,512,82944)
    return dict(truth=truth,forecasts=forecast,alternate=alternate,bounds=checks,stats=report(d))
def masks(rep,common,persistent):
    j=rep%4; sign=1 if rep<4 else -1
    if common: initial=[1]*4
    else:
        a,b=(1 if j&1 else -1),(1 if j&2 else -1)
        initial=[-1,a,b,-a*b]
    x=((j+1)*2654435761)&0xffffffff; seq=[initial]
    for t in range(1,9):
        m=[]
        for _ in range(1 if common else 4):
            x=(1664525*x+1013904223)&0xffffffff;m.append(1 if x>>31 else -1)
        seq.append(m*4 if common else m)
    seq=[[sign*v for v in m] for m in seq]
    return [seq[0]]*9 if persistent else seq

def b1():
    for common,persistent in product((False,True),repeat=2):
        allm=[masks(r,common,persistent) for r in range(8)]
        assert all(sum(m[t][i] for m in allm)==0 for t in range(9) for i in range(4))
    d=defaultdict(lambda:[0,0.,0.,0.,0.]); mass=defaultdict(lambda:[0,0.,0.,0.,0.]);truth=replicates=0
    for k in product((1,3,5),repeat=4):
        for fd in ((.75,.5,1.8),(.5,.75,1.8)):
            z=traj(k,fd);truth+=1
            for common,persistent in product((False,True),repeat=2):
                ch=('common' if common else 'independent')+'/'+('persistent' if persistent else 'varying')
                for rep in range(8):
                    m=masks(rep,common,persistent);o=[obs(x,s) for x,s in zip(z,m)];replicates+=1
                    for label,model in [('correct',fd),('alternate',FDS[0])]:
                        f=traj(o[0],model);b=o[0]
                        for t,x in enumerate(z):
                            if t: b=[.5*(a+c) for a,c in zip(step(b,model),o[t])]
                            assert all(0<=a<=6 for a in b)
                            for name,khat in [('measured',o[t]),('forecast',f[t]),('blend',b)]:
                                for chan in (ch,'pooled'):
                                    for epoch in ('all',*(['early'] if t<=2 else ['late'] if t>=6 else [])):
                                        key='/'.join((chan,label,name,epoch));add(d,key,local(khat,model)-local(x,fd));add(mass,key,avg(khat)-avg(x))
    assert truth==162 and replicates==5184
    return dict(truth=truth,replicates=replicates,snapshots=replicates*9,flux=report(d),meanDensity=report(mass))
if __name__=='__main__': print(json.dumps(dict(b0=b0(),b1=b1()),indent=2))
