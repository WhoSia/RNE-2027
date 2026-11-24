"""Independent native tuple/count verification of P155 factorial totals."""
import itertools
import json


def cost(tape,P,D,shared,staged,common,reuse):
    q=(); nS=nL=p=u=v=out=arrived=J=0
    for t in range(160):
        g=('S' if t%4<2 else 'L') if t<8 else 'BBSSBBLL'[(t+2)%8]
        x=int(u>0 and t%4<2); y=int(v>0 and t%4<2)
        supply=D-u+int(t>=8 and reuse)*x
        left_supply=supply if common else D-v+int(t>=8 and reuse)*y
        hs=bool(q and q[0]=='S') if shared else nS>0
        hl=bool(q and q[0]=='L') if shared else nL>0
        enter=int(staged and hl and p<P)
        ms=int(hs and g in 'BS' and supply>0)
        ml=int((p>0 if staged else hl) and g in 'BL' and left_supply>0 and not(common and ms))
        from_left=enter+int(not staged)*ml
        assert not(shared and ms and from_left)
        if shared:q=q[ms+from_left:]
        else:nS-=ms;nL-=from_left
        p+=enter-int(staged)*ml
        u+=ms+int(common)*ml-x;v+=int(not common)*ml-y;out+=x+y
        if t in tape:
            a=tape[t];arrived+=1
            if shared:q+=(a,)
            elif a=='S':nS+=1
            else:nL+=1
        n=len(q)+nS+nL+p+u+v;J+=n
        assert arrived-out==n and min(nS,nL,p,u,v)>=0 and p<=P and u<=D and v<=D
    assert out==arrived==len(tape)
    return J


def run():
    def tape(n,m):return {2*i:'L' if m&(1<<i) else 'S' for i in range(n)}
    A=[(tape(7,m),P,2) for m,P in ((82,1),(82,2),(83,1),(83,2),(86,2),(87,2))]
    B=[({t:a for t,a in tape(7,82).items() if m&(1<<(t//2))},1,2) for m in range(128)]
    C=[(tape(n,m),1,2) for n in range(1,8) for m in range(1<<n)]
    tops=list(itertools.product((True,False),repeat=3))
    def summarize(cohort,top):
        totals=[0,0,0];minimum=None
        for t,P,D in cohort:
            a=cost(t,P,D,*top,False);b=cost(t,P,D,*top,True)
            totals[(b>a)-(b<a)+1]+=1
            if b>a:minimum=len(t) if minimum is None else min(minimum,len(t))
        return [*totals,minimum]
    a=[summarize(A,t) for t in tops];b=[summarize(B,t) for t in tops];c=summarize(C,tops[0])
    assert a==[[0,0,6,7]]+[[0,6,0,None]]*7
    assert b==[[0,126,2,6]]+[[0,128,0,None]]*7
    assert c[2:]==[2,7]
    return dict(status='INDEPENDENT_NATIVE_AGGREGATE_REPLAY_NOT_FIELD',arms=2652,A=a,B=b,C=c)

if __name__=='__main__':print(json.dumps(run(),indent=2))
