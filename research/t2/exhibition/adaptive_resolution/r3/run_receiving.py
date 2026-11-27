import json,sys
from fractions import Fraction as F
from receiving import *

def run(finite):
    m=Model(finite);out=[]
    for peak in (0,4):
        p={name:Planner(m,peak,allowed) for name,allowed in [('free',(0,)),('word',(0,1,2)),('receiving',(0,3)),('joint',(0,1,2,3))]}
        cals={c:Planner(m,peak,calendar=c) for c in calendars(3,4)}
        for q,w in [((2,2),'0001'),((2,0),'0011')]:
            b=initial(q,w);rows=[]
            for k in (0,1,2,4):
                reps={n:s.report(b,k) for n,s in p.items()}
                cr=[{'calendar':c,'report':s.report(b,k)} for c,s in cals.items() if sum(COST[x] for x in c)<=k]
                best=min(cr,key=lambda x:(F(x['report']['cost']),x['calendar']));opt=F(reps['joint']['cost'])
                assert all(F(r['cost'])>=opt for r in reps.values()) and all(F(x['report']['cost'])>=opt for x in cr)
                if rows:assert opt<=F(rows[-1]['policies']['joint']['cost'])
                # known initial receiving state, then no paid acquisition; future receiving can remain hidden
                known=sum(pr*F(p['free'].report(bb,k)['cost']) for _,pr,bb in m.partition(b,3))
                rows.append({'budget':k,'policies':reps,'calendar_count':len(cr),'best_calendar':best,'calendar_gain':str(F(best['report']['cost'])-opt),'known_initial_receiving_free':str(known),'calendars':cr})
            out.append({'finite':finite,'peak':peak,'q':q,'word':w,'rows':rows});print(finite,peak,q,'done',file=sys.stderr,flush=True)
    return out
if __name__=='__main__':print(json.dumps(run(sys.argv[1]=='finite'),indent=2))
