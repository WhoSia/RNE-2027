"""Independent finite P158 tuple/count replay; nominal resource caps unchanged."""
from itertools import product
import json


def cost(tape,P,shared,partition,reuse):
    q=();ns=nl=p=a=z=j=stranded=0;r=()
    for t in range(160):
        gate=('S' if t%4<2 else 'L') if t<8 else 'BBSSBBLL'[(t+2)%8]
        x=int(bool(r) and t%4<2);depart=r[0] if x else None
        now=int(t>=8 and reuse)
        total=2-len(r)+now*x
        supply={m:(1-r.count(m)+now*int(depart==m)) if partition else total for m in 'SL'}
        hs=bool(q and q[0]=='S') if shared else ns>0
        hl=bool(q and q[0]=='L') if shared else nl>0
        e=int(hl and p<P)
        wants={'S':hs and gate in 'BS','L':p>0 and gate in 'BL'}
        move=next((m for m in 'SL' if wants[m] and supply[m]>0),None)
        stranded+=int(partition and not move and any(wants.values()) and total>0)
        ms=int(move=='S');ml=int(move=='L');assert not(shared and ms and e)
        if shared:q=q[ms+e:]
        else:ns-=ms;nl-=e
        p+=e-ml;r=r[x:]+((move,) if move else ());z+=x
        if t in tape:
            a+=1;v=tape[t]
            if shared:q+=(v,)
            elif v=='S':ns+=1
            else:nl+=1
        n=len(q)+ns+nl+p+len(r);j+=n
        assert a-z==n and 0<=p<=P and len(r)<=2 and min(ns,nl)>=0
        assert not partition or all(r.count(m)<=1 for m in 'SL')
    assert z==a==len(tape)
    return j,stranded


def run():
    def tape(m):return {2*i:'L' if m&(1<<i) else 'S' for i in range(7)}
    A=[(tape(m),P) for m,P in ((82,1),(82,2),(83,1),(83,2),(86,2),(87,2))]
    B=[({t:v for t,v in tape(82).items() if m&(1<<(t//2))},1) for m in range(128)]
    C=[(tape(m),1) for m in range(128)]
    def cohort(entries):
        tops=list(product((True,False),(False,True)))
        totals=[[0,0,0,0,0] for _ in tops];contrasts=[[[0,0,0],[0,0,0]] for _ in tops[1:]]
        for tape,P in entries:
            costs=[[cost(tape,P,*top,r) for r in (False,True)] for top in tops]
            for i,((old,so),(new,sn)) in enumerate(costs):
                totals[i][(new>old)-(new<old)+1]+=1;totals[i][3]+=so;totals[i][4]+=sn
                if i:
                    for k in (0,1):
                        a,b=costs[i][k][0],costs[0][k][0]
                        contrasts[i-1][k][(a>b)-(a<b)+1]+=1
        return dict(totals=totals,contrasts=contrasts)
    a,b,c=map(cohort,(A,B,C))
    assert a['totals']==[[0,0,6,0,0],[0,6,0,6,6],[0,6,0,0,0],[0,6,0,6,6]]
    assert b['totals']==[[0,126,2,0,0],[16,112,0,24,4],[0,128,0,0,0],[16,112,0,24,4]]
    assert c['totals']==[[0,126,2,0,0],[90,38,0,332,169],[0,128,0,0,0],[60,68,0,289,197]]
    assert c['contrasts']==[[[0,16,112],[0,63,65]],[[20,108,0],[22,106,0]],[[6,33,89],[8,58,62]]]
    return dict(status='INDEPENDENT_NATIVE_AGGREGATE_REPLAY_NOT_FIELD',arms=2096,A=a,B=b,C=c)

if __name__=='__main__':print(json.dumps(run(),indent=2))
