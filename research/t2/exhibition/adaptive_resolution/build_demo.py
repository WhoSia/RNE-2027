"""Build a standalone offline HTML replay from evaluated model results."""
import json
from fractions import Fraction as F
from pathlib import Path
from model import Config,Model,witness_belief
from planner import Planner
from trace import replay
ROOT=Path(__file__).parent
POL={'free':('free',4),'head':('head',4),'full':('full',4),'qmdp':('adaptive',1),'depth2':('adaptive',2),'exact':('adaptive',4)}

def build():
    data=json.loads((ROOT/'results.json').read_text());auto=json.loads((ROOT/'lazy_results.json').read_text())['rows'];b=witness_belief()
    for case in data:
        c=Config(erasure=F(case['erasure']),service=case['service'],schedule=tuple(case['schedule']),budget=case['budget']);case['traces']={};case['auto']={}
        for row in auto:
            if all(row[k]==case[k] for k in ('erasure','service','schedule','budget')):
                d=row['selected_depth']; assert d in (1,2,4)
                case['auto'][f"{row['cap']}|{row['epsilon']}"]={**row['policy'],'lower':row['lower'],'objective':row['upper'],'gap':row['gap'],'regret':str(F(row['upper'])-F(case['policies']['exact']['objective'])),'selected_depth':d,'explored_depth':row['explored_depth'],'certified':row['certified'],'exact':row['exact'],'evaluations':row['evaluations'],'epsilon':row['epsilon'],'trace_policy':{1:'qmdp',2:'depth2',4:'exact'}[d]}
        assert len(case['auto'])==4
        # Two declared example event streams, same per-policy, not random performance estimates.
        streams=[[(2,'0',False),(2,'1',False),(2,'0',False),(2,'1',False)],[(1 if c.service=='random' else 2,'1',bool(c.erasure)),(2,'0',False),(1 if c.service=='random' else 2,'1',bool(c.erasure)),(2,'0',False)]]
        for p,(mode,d) in POL.items():
            planner=Planner(Model(c),mode,d);case['traces'][p]=[[replay(planner,b,x,events) for x,_ in b] for events in streams]
    payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    template=(ROOT/'demo_template.html').read_text()
    (ROOT/'adaptive_resolution_demo.html').write_text(template.replace('__DATA__',payload))
if __name__=='__main__':build()
