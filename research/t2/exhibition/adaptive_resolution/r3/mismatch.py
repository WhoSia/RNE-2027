"""Exact replay of a nominal policy under a different synthetic channel law."""
from receiving_channel import *
from collections import defaultdict
import json

def true_obs(m,x,mode):
    if not mode:return ((None,F(1)),)
    o=m.observe(x,mode)
    if mode!=3:return ((o,F(1)),)
    d=defaultdict(F);d[o]+=1-m.error;d[o[::-1]]+=m.error
    return tuple((k,v) for k,v in d.items() if v)

def replay(p,actual,b,k):
    m=p.m;completed=F(0);abort=F(0);total=ZERO;paid=F(0);worst=0;abort_stages=defaultdict(F);leaves=0
    def stop(prob,spent,h):
        nonlocal abort,paid,worst,leaves
        abort+=prob;paid+=prob*spent;worst=max(worst,spent);abort_stages[m.H-h+1]+=prob;leaves+=1
    def walk(x,b,h,remaining,prob,acc):
        nonlocal completed,total,paid,worst,leaves
        mode=p.sense(b,h,remaining)[1];c=COST[mode];spent=acc[5]+c
        assert c<=remaining and spent<=k
        parts={o:bb for o,_,bb in m.partition(b,mode)} if mode else {None:b}
        for o,po in true_obs(actual,x,mode):
            pr=prob*po
            if o not in parts:stop(pr,spent,h);continue
            bb=parts[o];a=p.control(bb,h,remaining-c)[1]
            nextparts={m.observe(cc[0][0],0):cc for _,cc in m.predict(bb,a)[1]} if h>1 else {}
            for y,v in actual.step(x,a):
                q=pr/8;aa=add(acc,add(v,(0,0,0,0,0,c,int(bool(mode)))))
                if h==1:
                    completed+=q;total=add(total,tuple(q*z for z in aa));paid+=q*aa[5];worst=max(worst,aa[5]);leaves+=1
                else:
                    oo=m.observe(y,0)
                    if oo not in nextparts:stop(q,aa[5],h-1)
                    else:walk(y,nextparts[oo],h-1,remaining-c,q,aa)
    for x,w in b:walk(x,b,m.H,k,F(w,mass(b)),ZERO)
    assert completed+abort==1 and worst<=k
    return {'complete_mass':str(completed),'abort_mass':str(abort),'abort_stage':{str(t):str(v) for t,v in sorted(abort_stages.items())},'completed_vector':[str(v/completed) for v in total] if completed else None,'completed_cost':str(p.cost(total)/completed) if completed else None,'unconditional_credits_spent':str(paid),'worst':int(worst),'leaves':leaves}

def run():
    b=initial((2,2),'0001');out=[];k=2;errors=(F(0),F(1,4),F(1,2))
    for obj,cls in [('upstream',Planner),('system',SystemPlanner)]:
        models={e:ChannelModel(e) for e in errors};ps={e:cls(m) for e,m in models.items()};opt={e:F(p.report(b,k)['cost']) for e,p in ps.items()}
        for e in errors:
            for t in errors:
                r=replay(ps[e],models[t],b,k)
                excess=F(r['completed_cost'])-opt[t] if r['abort_mass']=='0' else None
                if excess is not None:assert excess>=0
                if e==t:
                    assert excess==0 and r['completed_vector']==ps[e].report(b,k)['vector']
                out.append({'objective':obj,'nominal':str(e),'actual':str(t),'true_optimum':str(opt[t]),'excess_if_no_abort':str(excess) if excess is not None else None,**r})
    return out
if __name__=='__main__':print(json.dumps(run(),indent=2))
