from itertools import product
import json

POL=list(product((3,4,5),(0,2,4,6)))
PRIORS=[(i,j,6-i-j) for i in range(7) for j in range(7-i)]

def labels(seed,left):
    a=list(range(24)); x=seed+1
    for i in range(23,0,-1):
        x=(1664525*x+1013904223)&0xffffffff; j=x%(i+1)
        a[i],a[j]=a[j],a[i]
    return ''.join('L' if v<left else 'S' for v in a)

def step(s,t,g,o,P,R,v):
    q,p,r,A,Y,Z,J=s; h=q[:1]
    x=int(t%8<g and h=='S' and r<R); a=int(h=='L' and p<P)
    y=int(t%8>=g and p>0); z=int((t+o)%8<4 and r>0)
    q=q[x+a:]+v; p+=a-y; r+=x-z; A+=bool(v);Y+=y;Z+=z
    stock=len(q)+p+r
    assert stock+Y+Z==A and 0<=p<=P and 0<=r<=R
    return q,p,r,A,Y,Z,J+stock

def run():
    grid={w:[0,0,0] for w in PRIORS}; groups=arms=ambiguous=oracle=0
    for seed,left,P,R in product(range(460,480),(6,12,18),(1,3),(1,3)):
        lab=labels(seed,left); pre=('',0,0,0,0,0,0)
        for t in range(16):pre=step(pre,t,4,0,P,R,lab[t//4] if t%4==0 else '')
        cost=[]
        for start,stride in ((16,4),(16,1),(32,1)):
            ar={start+j*stride:v for j,v in enumerate(lab[4:])}; row=[]
            for g,o in POL:
                s=pre
                for t in range(16,240):s=step(s,t,g,o,P,R,ar.get(t,''))
                assert s[3]==s[4]+s[5]==24
                row.append(s[-1]); arms+=1
            cost.append(row)
        mins=list(map(min,cost)); oracle+=sum(mins); groups+=1
        r=[[v-m for v in row] for row,m in zip(cost,mins)]
        ambiguous+=min(map(sum,zip(*r)))>0
        for w in PRIORS:
            # Separate minimum for each signal output, no pair enumeration.
            no=min(sum(4*w[u]*r[u][a] for u in range(3)) for a in range(12))
            def conditional(q):
                return sum(min(sum(w[u]*(q[u] if h==0 else 4-q[u])*r[u][a] for u in range(3)) for a in range(12)) for h in range(2))
            perfect=conditional((4,0,0)); noisy=conditional((3,1,1))
            assert 0<=perfect<=noisy<=no
            for i,v in enumerate((no,perfect,noisy)):grid[w][i]+=v
    assert groups==240 and arms==8640
    return dict(arms=arms,groups=groups,ambiguous=ambiguous,groupOracle=oracle,denominator=24,grid=[dict(w=w,none=v[0],binary=v[1],noisy=v[2],perfect=0) for w,v in grid.items()])

if __name__=='__main__':print(json.dumps(run(),indent=2))
