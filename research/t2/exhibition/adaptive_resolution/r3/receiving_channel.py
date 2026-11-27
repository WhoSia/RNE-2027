"""Known synthetic measurement likelihood; not a calibrated detector."""
from receiving import *

class ChannelModel(Model):
    def __init__(self,error=F(0)):
        if not 0<=error<=F(1,2):raise ValueError('error')
        self.error=F(error)
        super().__init__(True)
    def _partition(self,b,m):
        if m!=3:return super()._partition(b,m)
        groups=defaultdict(Counter);e=self.error
        for x,w in b:
            rs,rl=self.observe(x,3)
            for o,mult in (((rs,rl),e.denominator-e.numerator),((rl,rs),e.numerator)):
                if mult:groups[o][x]+=w*mult
        den=mass(b)*e.denominator
        assert sum(sum(g.values()) for g in groups.values())==den
        return tuple((o,F(sum(g.values()),den),norm(g.items())) for o,g in sorted(groups.items()))

class SystemPlanner(Planner):
    def cost(self,v):return v[3]

def run():
    out=[]
    for e in (F(0),F(1,4),F(1,2)):
        m=ChannelModel(e)
        specs=[('free',(0,)),('word',(0,1,2)),('receiving',(0,3)),('joint',(0,1,2,3))]
        planners={obj:{n:cls(m,modes=a) for n,a in specs} for obj,cls in [('upstream',Planner),('system',SystemPlanner)]}
        cals={obj:{c:cls(m,calendar=c) for c in calendars(3,4)} for obj,cls in [('upstream',Planner),('system',SystemPlanner)]}
        for q,w in [((2,2),'0001'),((2,0),'0011')]:
            b=initial(q,w)
            if e==F(1,2):assert all(bb==b for _,_,bb in m.partition(b,3))
            rows=[]
            for k in (0,1,2,4):
                policies={o:{p:s.report(b,k) for p,s in ps.items()} for o,ps in planners.items()}
                best={}
                for obj,cs in cals.items():
                    cr=[{'calendar':c,'report':s.report(b,k)} for c,s in cs.items() if sum(COST[x] for x in c)<=k]
                    best[obj]=min(cr,key=lambda r:(F(r['report']['cost']),r['calendar']))
                    opt=F(policies[obj]['joint']['cost']);assert all(F(v['cost'])>=opt for v in policies[obj].values()) and all(F(v['report']['cost'])>=opt for v in cr)
                    if rows:assert opt<=F(rows[-1]['policy'][obj]['joint']['cost'])
                u=policies['upstream']['joint'];s=policies['system']['joint'];regret=F(u['vector'][3])-F(s['cost']);assert regret>=0
                rows.append({'budget':k,'policy':policies,'best_calendar':best,'system_regret_of_upstream_optimum':str(regret),'system_optimal_upstream_cost':str(F(s['vector'][0])+F(s['vector'][1]))})
            out.append({'error':str(e),'q':q,'word':w,'rows':rows})
            print('complete',e,q,file=__import__('sys').stderr,flush=True)
    return out
if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2))
