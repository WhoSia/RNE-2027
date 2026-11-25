from itertools import product
import json

POL = list(product((3,4,5),(0,2,4,6)))

def labels(seed,left):
    a=list(range(24)); x=seed+1
    for i in range(23,0,-1):
        x=(1664525*x+1013904223)&0xffffffff
        j=x%(i+1); a[i],a[j]=a[j],a[i]
    return ''.join('L' if v<left else 'S' for v in a)

def step(s,t,g,o,P,R,v):
    q,p,r,A,Y,Z,J=s
    h=q[:1]; gs=t%8<g; ds=(t+o)%8<4
    x=int(gs and h=='S' and r<R); a=int(h=='L' and p<P)
    y=int(not gs and p>0); z=int(ds and r>0)
    q=q[x+a:]+v; p+=a-y; r+=x-z; A+=bool(v); Y+=y; Z+=z
    stock=len(q)+p+r
    assert stock+Y+Z==A and 0<=p<=P and 0<=r<=R
    return q,p,r,A,Y,Z,J+stock

def run():
    out=dict(arms=0,groups=0,ambiguous=0,maxGroup=0,oracle=0,meanJ=0,minimaxJ=0,meanRegret=0,minimaxRegret=0,maxMean=0,maxMinimax=0)
    for seed,left,P,R in product(range(440,460),(6,12,18),(1,3),(1,3)):
        lab=labels(seed,left); pre=('',0,0,0,0,0,0)
        for t in range(16):pre=step(pre,t,4,0,P,R,lab[t//4] if t%4==0 else '')
        costs=[]
        for start,stride in ((16,4),(16,1),(32,1)):
            ar={start+j*stride:v for j,v in enumerate(lab[4:])}
            row=[]
            for g,o in POL:
                s=pre
                for t in range(16,240):s=step(s,t,g,o,P,R,ar.get(t,''))
                assert s[3]==s[4]+s[5]==24
                row.append(s[-1]);out['arms']+=1
            costs.append(row)
        opt=list(map(min,costs)); total=list(map(sum,zip(*costs)))
        worst=[max(row[i]-v for row,v in zip(costs,opt)) for i in range(12)]
        a=min(range(12),key=lambda i:(total[i],i)); b=min(range(12),key=lambda i:(worst[i],total[i],i))
        m=sum(opt); gap=total[a]-m
        assert (gap==0)==any(all(row[i]==v for row,v in zip(costs,opt)) for i in range(12))
        out['groups']+=1; out['ambiguous']+=gap>0;out['maxGroup']=max(out['maxGroup'],gap)
        out['oracle']+=m;out['meanJ']+=total[a];out['minimaxJ']+=total[b]
        out['meanRegret']+=gap;out['minimaxRegret']+=total[b]-m
        out['maxMean']=max(out['maxMean'],worst[a]);out['maxMinimax']=max(out['maxMinimax'],worst[b])
    assert out['arms']==8640 and out['groups']==240
    return out

if __name__=='__main__': print(json.dumps(run(),indent=2))
