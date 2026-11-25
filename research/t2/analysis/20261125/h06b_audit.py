import json
import numpy as np

def run():
    out=[]
    for N in (6,8,10):
        ids=np.arange(3**N,dtype=np.int64)
        X=(ids[:,None]//(3**np.arange(N)))%3
        targets=[]
        for V,W,C in ((15,10,36),(20,5,24)):
            x=3*X; D=1
            for t in range(3):
                F=np.minimum(np.minimum(V*x,C*D),W*(6*D-np.roll(x,-1,axis=1)))
                targets.append(F.sum(axis=1))
                y=20*x+np.roll(F,1,axis=1)-F
                assert np.all((y>=0)&(y<=120*D)) and np.array_equal(y.sum(axis=1),20*x.sum(axis=1))
                x=y; D*=20
        entries=[]; codes=np.zeros_like(X)
        for k in range(1,7):
            codes=3*codes+np.roll(X,-(k-1),axis=1)
            _,ix,n=np.unique(np.sort(codes,axis=1),axis=0,return_inverse=True,return_counts=True)
            ix=ix.ravel(); n=n.ravel()
            q=n/len(X)
            a=dict(k=k,groups=len(n),singletons=int(np.sum(n==1)),entropy=float(-np.sum(q*np.log2(q))),targets=[])
            for i,v in enumerate(targets):
                den=N*20**(1+i%3); lo=np.full(len(n),np.iinfo(np.int64).max,dtype=np.int64);hi=np.zeros(len(n),dtype=np.int64)
                np.minimum.at(lo,ix,v); np.maximum.at(hi,ix,v)
                mu=np.bincount(ix,weights=v)/n
                mse=float(np.mean(((v-mu[ix])/den)**2))
                bad=hi>lo
                assert k<2*(i%3)+2 or not bad.any()
                a['targets'].append(dict(fd=i//3,t=i%3,floor=mse,ambiguousGroups=int(bad.sum()),ambiguousStates=int(n[bad].sum()),maxRange=float(np.max(hi-lo)/den)))
            entries.append(a)
        out.append(dict(N=N,states=len(X),rawEntropy=float(N*np.log2(3)),entries=entries))
    return dict(status='NATIVE_NUMPY_EXECUTED',results=out,states=sum(x['states'] for x in out))
if __name__=='__main__': print(json.dumps(run(),indent=2))
