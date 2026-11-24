"""Native independent P156 replay; fixed synthetic head-observation stress."""
from collections import defaultdict
from itertools import product
import json


def step(state,t,g,reuse,priority,P,D,sink,arrival):
    q,p,d,a,z,j=state
    release=int(d>0 and (t+sink)%4<2)
    space=D-d+release*reuse
    enter=int(bool(q) and q[0]=='L' and p<P)
    eligible=[]
    if q and q[0]=='S' and g in 'BS':eligible.append('S')
    if p and g in 'BL':eligible.append('L')
    move=(priority if priority in eligible else eligible[0]) if eligible and space>0 else None
    assert not(enter and move=='S')
    q=q[enter+int(move=='S'):]+((arrival,) if arrival else ())
    p+=enter-int(move=='L');d+=int(move is not None)-release
    a+=int(arrival is not None);z+=release
    n=len(q)+p+d;assert a-z==n and 0<=p<=P and 0<=d<=D
    return q,p,d,a,z,j+n


def worlds():
    clocks=((0,1,3,5,8,9,12,15),(0,2,4,7,9,11,13,16))
    gates={4:'BSBL',8:'BBSSBBLL'}
    for mask,clock,P,D,sink in product(range(256),range(2),(1,2),(1,2),(0,2)):
        tape={t:'L' if mask&(1<<i) else 'S' for i,t in enumerate(clocks[clock])}
        pre=((),0,0,0,0,0)
        for t in range(8):pre=step(pre,t,'S' if t%4<2 else 'L',0,'S',P,D,sink,tape.get(t))
        q,p,d,*_=pre
        fs=((),(len(q)+p+d,),(len(q),p,d),(len(q),p,d,q[0] if q else '-'),(''.join(q),p,d))
        for pair,reuse,priority in product(range(4),(0,1),('S','L')):
            costs=[]
            for period in (4,8):
                s=pre;offset=pair if period==4 else 2*pair
                for t in range(8,160):
                    s=step(s,t,gates[period][(t+offset)%period],reuse,priority,P,D,sink,tape.get(t))
                    if s[4]==8:break
                assert s[3]==s[4]==8
                costs.append(s[5])
            yield mask,clock,(P,D,sink,pair),fs,costs[0]-costs[1]


def run():
    maps=[defaultdict(lambda:[set(),0,0,0,0]) for _ in range(5)];test=[];train=0
    def loss(action,d):return max(0,d if action==4 else -d)
    for mask,clock,ctx,fs,d in worlds():
        if mask%5==0:test.append((mask,clock,ctx,fs,d));continue
        train+=1
        for m,f in zip(maps,fs):
            a=m[ctx+f];a[0].add(mask);a[1]+=int(d<0);a[2]+=int(d>0);a[3]+=loss(4,d);a[4]+=loss(8,d)
    def action(m,key):
        s=m.get(key)
        return (4 if s[1] else 8) if s and len(s[0])>=4 and bool(s[1])!=bool(s[2]) else None
    def stats():return dict(n=0,covered=0,strictHarm=0,coveredRegret=0,coveredWorst=0,allRegret=0,allWorst=0,changed=0)
    names=('context','total','counts','head','ordered','flip','missing','mixed10')
    res={k:stats() for k in names};baseline=0
    for mask,clock,ctx,fs,d in test:
        b=maps[0][ctx];fallback=4 if b[3]<=b[4] else 8;baseline+=loss(fallback,d)
        head=fs[3];h=head[-1];P,D,sink,pair=ctx
        flip=head[:-1]+({'S':'L','L':'S'}.get(h,h),)
        mixed=flip if (mask+3*P+5*D+7*sink+11*pair+13*clock)%10==0 else head
        acts=[(action(m,ctx+f),False) for m,f in zip(maps,fs)]+[(action(maps[3],ctx+flip),flip!=head),(None if h!='-' else action(maps[3],ctx+head),h!='-'),(action(maps[3],ctx+mixed),mixed!=head)]
        for name,(a,changed) in zip(names,acts):
            x=res[name];l=loss(a if a is not None else fallback,d);x['n']+=1;x['changed']+=changed;x['allRegret']+=l;x['allWorst']=max(x['allWorst'],l)
            if a is not None:x['covered']+=1;x['strictHarm']+=int(l>0);x['coveredRegret']+=l;x['coveredWorst']=max(x['coveredWorst'],l)
    expected=[(5824,4928),(6740,4928),(7472,4868),(8060,4664),(8240,4664)]
    assert train==52224 and len(test)==13312 and baseline==4928
    for name,(c,r) in zip(names,expected):assert (res[name]['covered'],res[name]['allRegret'],res[name]['strictHarm'],res[name]['allWorst'])==(c,r,0,15)
    return dict(status='NATIVE_P156_AGGREGATE_REPLAY_AND_SYNTHETIC_STRESS',trainWorlds=train,testWorlds=len(test),arms=2*(train+len(test)),baseline=baseline,results=res)

if __name__=='__main__':print(json.dumps(run(),indent=2))
