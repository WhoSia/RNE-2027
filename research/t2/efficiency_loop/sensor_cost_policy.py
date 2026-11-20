"""Decision-time and cost gate for synthetic T2 sensor/forecast candidates.

A forecast issued before the decision may concern a future event; its
*realized* future value can never be used as a current observation. No
camera, detector or real signal is claimed to exist. Policy selection uses
sample-independent worst-case regret from synthetic worlds plus fixed costs.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from sensor_fusion_decision import Channel, optimize


@dataclass(frozen=True)
class Source:
    key: str
    is_forecast: bool
    issued_at: int
    reported_at: int
    target_at: int
    error_bound: F
    fixed_cost: F
    provenance_ok: bool = True
    def __post_init__(self):
        if self.key not in ('structure','arrival'):
            raise ValueError('unexpected source kind')
        if any(type(t) is not int for t in (self.issued_at,self.reported_at,self.target_at)):
            raise TypeError('time must be integer ticks')
        if not (F(0)<=self.error_bound<=F(1)) or self.fixed_cost<0:
            raise ValueError('invalid error/cost')
        if self.reported_at<self.issued_at:
            raise ValueError('report before issuance')


def available(source:Source, commitment:int)->bool:
    if type(commitment) is not int:
        raise TypeError('commitment tick must be integer')
    if not source.provenance_ok or source.reported_at>commitment:
        return False
    if not source.is_forecast and source.target_at>commitment:
        return False
    if source.is_forecast and source.issued_at>commitment:
        return False
    return True


def pick(sources, commitment:int, budget):
    budget=F(budget)
    if budget<0:raise ValueError('negative cost budget')
    items={x.key:x for x in sources if available(x,commitment)}
    candidates=[]
    for mode in (False,True):
        for arrival in (False,True):
            if mode and 'structure' not in items:continue
            if arrival and 'arrival' not in items:continue
            cost=sum((items[k].fixed_cost for k,on in
                      (('structure',mode),('arrival',arrival)) if on),F(0))
            if cost>budget:continue
            em=items['structure'].error_bound if mode else F(0)
            ea=items['arrival'].error_bound if arrival else F(0)
            d=optimize(Channel(mode,arrival),em,ea,cost=cost)
            candidates.append({'sources':tuple(k for k,on in
                (('structure',mode),('arrival',arrival)) if on),
                'gross_regret':d.worst_regret-float(cost),'cost':float(cost),
                'total':d.worst_regret})
    if not candidates:raise AssertionError('no null-sensing candidate')
    return min(candidates,key=lambda x:(round(x['total'],8),len(x['sources']),x['cost']))
