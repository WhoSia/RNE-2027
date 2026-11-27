"""Exact optimal control under class-informed predetermined measurement calendars."""
from itertools import product
from fractions import Fraction as F
import json
from model import Config,Model,witness_belief,CREDITS
from objective import Objective,VectorDynamics,VectorPlanner
from run_objective import CLASSES

class CalendarPlanner(VectorPlanner):
    def __init__(self,dynamics,objective,calendar):
        self.calendar=calendar
        if len(calendar)!=dynamics.model.c.horizon or any(m not in range(3) for m in calendar) or sum(CREDITS[m] for m in calendar)>dynamics.model.c.budget:raise ValueError('calendar')
        super().__init__(dynamics,objective)
    def modes(self,b,h,k):
        m=self.calendar[self.model.c.horizon-h]
        return (m,) if m and CREDITS[m]<=k and len(self.model.partition(b,m))>1 else (0,)

def run():
    refs=json.load(open('budget_frontier_results.json'));out=[]
    calendars=[m for m in product(range(3),repeat=4) if sum(CREDITS[x] for x in m)<=4];assert len(calendars)==20
    for law,erasure,service in [('ideal',F(0),'fixed'),('broad',F(1,4),'random')]:
        for weights in [(1,1,0,0,0),(1,1,4,0,0)]:
            o=Objective(weights);d=VectorDynamics(Model(Config(schedule=(1,2,3,4),erasure=erasure,service=service,budget=4)))
            ps=[CalendarPlanner(d,o,m) for m in calendars]
            for q,w in CLASSES:
                b=witness_belief(q,w);ref=next(x for x in refs if x['law']==law and x['q']==list(q) and x['weights']==list(weights));cap=next(x for x in ref['rows'] if x['budget']==4);exact=F(cap['policy']['adaptive']['objective']);old=min(F(cap['policy'][p]['objective']) for p in ('free','head','full'));rows=[]
                for p in ps:
                    r=p.report(b);assert F(r['objective'])>=exact and r['gap']=='0' and r['worst_credits']<=4
                    rows.append({'calendar':p.calendar,'report':r})
                best=min(rows,key=lambda r:(F(r['report']['objective']),r['calendar']));v=F(best['report']['objective']);combined=min(old,v)
                out.append({'law':law,'q':q,'word':w,'weights':weights,'exact':str(exact),'previous_fixed':str(old),'best_calendar':best,'combined_baseline':str(combined),'residual_gain':str(combined-exact),'rows':rows})
                print(law,q,weights,'complete',file=__import__('sys').stderr,flush=True)
    return out
if __name__=='__main__':print(json.dumps(run(),indent=2))
