import numpy as np
from itertools import product
import json

def run():
    eps=1e-8
    X=np.array(list(product((0,2,4,6),repeat=4)),float)
    Y=np.array(list(product((1,3,5),repeat=4)),float)
    masks=np.array(list(product((-1,1),repeat=4)),float)
    result=[]; stats={}
    for v,w in ((.75,.5),(1.,.25)):
        C=6*v*w/(v+w)
        def flux(x):return np.minimum(np.minimum(v*x[...,:-1],C),w*(6-x[...,1:]))
        def step(x,u,d):
            a=np.minimum(u,np.minimum(C,w*(6-x[...,0])))
            b=np.minimum(d,np.minimum(C,v*x[...,-1]))
            F=np.concatenate((a[...,None],flux(x),b[...,None]),axis=-1)
            z=x+F[...,:-1]-F[...,1:]
            assert np.all(z>=-eps) and np.all(z<=6+eps) and np.max(abs(z.sum(-1)-x.sum(-1)-a+b))<eps
            return z,a,b
        def mf(x):return flux(x).mean(-1)
        bc=np.array(list(product((0,C/2,C),repeat=2)))
        O=np.array([step(X,u,d)[0] for u,d in bc])
        D=abs(X[:,None]-X[None,:]).sum(-1)
        DD=abs(O[:,:,None,:]-O[:,None,:,:]).sum(-1)
        comp=np.all(X[:,None]<=X[None,:]+eps,axis=-1)
        bad=np.any(O[:,:,None,:]>O[:,None,:,:]+eps,axis=-1)&comp
        bd=abs(bc[:,None]-bc[None,:]).sum(-1)
        bdiff=abs(O[:,None]-O[None,:]).sum(-1)
        assert not np.any(DD>D+eps) and not np.any(bad) and not np.any(bdiff>bd[...,None]+eps)
        result.append(dict(v=v,w=w,strict=int(np.sum(DD<D-eps)),tie=int(np.sum(abs(DD-D)<=eps)),comparable=int(comp.sum()*9)))
        for h in range(3):
            x=Y.copy(); M=x.sum(-1)
            for t in range(13):
                assert np.max(abs(x.sum(-1)-M))<eps
                for name,ms in [('cellwise',masks),('common',masks[[0,-1]])]:
                    y=np.clip(x[:,None,:]+ms[None,:,:],0,6); xx=x[:,None,:]
                    D=((y-xx)**2).mean(-1); F=(mf(y)-mf(xx))**2
                    for label,bias in [('raw',None),('negative',-1),('exact',0),('positive',1)]:
                        if bias is None:z=y
                        else:
                            target=np.clip(M+bias*.125*t,0,24)[:,None]
                            lo=np.full(y.shape[:-1],-6.); hi=-lo
                            for _ in range(48):
                                mid=(lo+hi)/2; small=np.clip(y+mid[...,None],0,6).sum(-1)<target
                                lo=np.where(small,mid,lo); hi=np.where(small,hi,mid)
                            z=np.clip(y+((lo+hi)/2)[...,None],0,6)
                            assert np.max(abs(z.sum(-1)-target))<eps
                        d=((z-xx)**2).mean(-1); f=(mf(z)-mf(xx))**2
                        if label=='exact':assert np.all(d<=D+eps)
                        s=stats.setdefault(name+'/'+label,[0,0.,0.,0,0,0,0,0,0])
                        values=[d.size,d.sum(),f.sum(),np.sum(d<D-eps),np.sum(abs(d-D)<=eps),np.sum(d>D+eps),np.sum(f<F-eps),np.sum(abs(f-F)<=eps),np.sum(f>F+eps)]
                        for i,a in enumerate(values):s[i]+=float(a)
                if t<12:
                    u=0 if h==2 and t>=6 else C
                    d=0 if h==1 and t<4 else C/2 if h==2 and t<6 else C
                    x,a,b=step(x,u,d); M+=a-b
    return dict(b2=result,columns=['n','densitySE','fluxSE','densityBetter','densityTie','densityWorse','fluxBetter','fluxTie','fluxWorse'],stats=stats)
if __name__=='__main__':print(json.dumps(run(),indent=2))
