"""T2 decision-focused fusion of a *synthetic* structure sensor and arrival forecast.

Compatible with the eight published exhibit-arrival worlds and two structural
bypass rules. A mode report is not a proven camera measurement, and the
arrival reporter is a hypothetical predictive distribution. Errors in each
channel are independently distributed conditional on the true world; each
per-world conditional error may vary anywhere from zero to its bound.
No field signal controller is defined or recommended here.

Reuse deliberately follows Long et al. (2026) chronological information
and action-value diagnostics, Huang et al. (2025) separation of lane
allocation from signal decisions, and Shafik & Rakha (2025)'s general
principle of integrating distinct measurement channels. We do not reproduce
or claim to implement their original optimization or Kalman estimator.
"""
from fractions import Fraction as F
from itertools import product
from dataclasses import dataclass
from scipy.optimize import linprog
from finite_sensor_information import ARRIVALS, DELTA, worlds


@dataclass(frozen=True)
class Channel:
    mode: bool = False
    arrival: bool = False
    def __post_init__(self):
        if type(self.mode) is not bool or type(self.arrival) is not bool:
            raise TypeError('Channel flags must be bool')


@dataclass(frozen=True)
class Decision:
    worst_regret: float
    p_left_by_report: tuple
    reports: tuple
    n_worlds: int
    n_inequalities: int


def report_support(ch: Channel):
    m=(0,1) if ch.mode else (None,)
    a=ARRIVALS if ch.arrival else (None,)
    return tuple(product(m,a))


def distribution(world, ch: Channel, em: F, ea: F):
    """For one true world, return P(report) for each report in support order.

    The arrival channel emits the correct 3-bit label with probability 1-ea;
    when wrong, its other SEVEN possible labels are equiprobable. A confusion
    pattern other than this is a separate model, not validated by this one.
    """
    mode,bits,delta=world
    if not (0 <= em <= 1 and 0 <= ea <= 1):
        raise ValueError('error probability must lie in [0,1]')
    probs=[]
    for rm,ra in report_support(ch):
        pm = (1-em if rm==mode else em) if ch.mode else F(1)
        pa = (1-ea if ra==bits else ea/7) if ch.arrival else F(1)
        probs.append(pm*pa)
    if sum(probs)!=1:
        raise AssertionError('report probabilities must sum to one')
    return tuple(probs)


def extremes(ch: Channel, em_max: F, ea_max: F):
    if not (0 <= em_max <= 1 and 0 <= ea_max <= 1):
        raise ValueError('error bounds must lie in [0,1]')
    mode_grid=(F(0),em_max) if ch.mode else (F(0),)
    arrival_grid=(F(0),ea_max) if ch.arrival else (F(0),)
    return tuple(dict.fromkeys(product(mode_grid,arrival_grid)))


def optimize(channel: Channel, mode_error=F(0), arrival_error=F(0), *, cost=0):
    """Solve the minimax policy with independent channel errors up to bounds.

    All per-world upper-bound error choices are protected, not just one
    global common error rate. Multilinearity in (em,ea) makes their corners
    sufficient for this *specified* conditional-independent channel family.
    """
    em_max,ea_max,cost=F(mode_error),F(arrival_error),F(cost)
    if cost < 0:
        raise ValueError('sensor cost must be nonnegative')
    support=report_support(channel)
    n=len(support)
    A=[]; B=[]
    for w in worlds():
        delta=F(w[2])
        for em,ea in extremes(channel,em_max,ea_max):
            probs=distribution(w,channel,em,ea)
            # regret = max(-delta,0) + delta * P(left-first)
            A.append([float(delta*x) for x in probs]+[-1.0])
            B.append(-float(max(-delta,F(0))))
    sol=linprog([0.0]*n+[1.0],A_ub=A,b_ub=B,
                bounds=[(0,1)]*n+[(0,None)],method='highs')
    if not sol.success:
        raise RuntimeError('regret LP failure: '+sol.message)
    probs=tuple(float(p) for p in sol.x[:n])
    # Audit solution directly, including ALL world-specific noise corners.
    check=max(float(max(-F(w[2]),F(0)) + F(w[2])*sum(
        r*p for r,p in zip(distribution(w,channel,em,ea),probs)))
              for w in worlds() for em,ea in extremes(channel,em_max,ea_max))
    if abs(check-float(sol.x[-1])) > 1e-6:
        raise AssertionError('LP primal value audit failed')
    return Decision(worst_regret=check+float(cost),p_left_by_report=probs,
                    reports=support,n_worlds=len(worlds()),n_inequalities=len(A))


def full_report():
    channels={
        'none':Channel(),
        'structure':Channel(mode=True),
        'arrival':Channel(arrival=True),
        'fusion':Channel(mode=True,arrival=True),
    }
    grid=(F(0),F(1,10),F(1,5),F(3,10),F(1,2))
    return {
        'scope':'16 synthetic paired exhibit worlds; no field sensor or measured driver gaps',
        'model':'independent conditional channel-error bounds; uniform wrong arrival label over other 7 patterns',
        'rates':{str(e):{name:round(optimize(ch,e,e).worst_regret,9)
                         for name,ch in channels.items()} for e in grid},
        'cost_boundary':{
            'structure_at_20pct':round(optimize(Channel(mode=True),F(1,5)).worst_regret,9),
            'fusion_at_20pct':round(optimize(Channel(mode=True,arrival=True),F(1,5),F(1,5)).worst_regret,9),
        },
        'oracle_regret':0,
        'predecision_contract':'reports must be emitted before the action commitment; arrival data here are hypothetical forecasts, not observed future events',
    }


if __name__=='__main__':
    import argparse,json
    from pathlib import Path
    parser=argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    args.output.write_text(json.dumps(full_report(),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
