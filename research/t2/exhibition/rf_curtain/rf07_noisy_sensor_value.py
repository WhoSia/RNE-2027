"""RF07: exact Bayes value of artificial noisy sensors; NOT empirical CSI."""
from fractions import Fraction as F
from itertools import product
import json

STATES=tuple(product((0,1),repeat=2))
CHANNELS=('aggregate','noisy_pocket','noisy_downstream','noisy_or','motion_only')
ACTIONS=('hold','virtual_treat')

def cost(state,action):
    if state not in STATES or action not in ACTIONS: raise ValueError('bad state/action')
    return F(0) if action=='hold' else F(-2 if state[0] else 3)

def likelihood(channel,state):
    p,d=state
    if channel=='aggregate': return {p+d:F(1)}
    if channel=='motion_only': return {0:F(1)}
    if channel=='noisy_pocket': truth,accuracy=p,F(4,5)
    elif channel=='noisy_downstream': truth,accuracy=d,F(4,5)
    elif channel=='noisy_or': truth,accuracy=int(bool(p or d)),F(9,10)
    else: raise ValueError('bad sensor')
    return {truth:accuracy,1-truth:1-accuracy}

def evaluate(channels=(),*,prior=None,sensor_fee=F(0)):
    """Conditional independence of channels GIVEN state is assumed, not measured."""
    channels=tuple(channels)
    if len(set(channels))!=len(channels) or any(c not in CHANNELS for c in channels):
        raise ValueError('bad or duplicated channels')
    if sensor_fee<0: raise ValueError('negative sensor fee')
    weights={s:F(1,4) for s in STATES} if prior is None else prior
    if set(weights)!=set(STATES) or any(v<0 for v in weights.values()) or sum(weights.values())!=1:
        raise ValueError('invalid prior')
    obs={}
    for state in STATES:
        joint={():F(1)}
        for channel in channels:
            nxt={}
            for prefix,mass in joint.items():
                for signal,lik in likelihood(channel,state).items():
                    nxt[prefix+(signal,)]=mass*lik
            joint=nxt
        for signal,prob in joint.items():
            masses=obs.setdefault(signal,{s:F(0) for s in STATES})
            masses[state]+=weights[state]*prob
    assert sum(sum(v.values()) for v in obs.values())==1
    risk=F(0);policy={}
    for signal,masses in sorted(obs.items()):
        expected={a:sum((masses[s]*cost(s,a) for s in STATES),F(0)) for a in ACTIONS}
        chosen=min(ACTIONS,key=lambda a:(expected[a],ACTIONS.index(a)))
        risk+=expected[chosen]
        policy[str(signal)]=chosen
    oracle=sum((weights[s]*min(cost(s,a) for a in ACTIONS) for s in STATES),F(0))
    regret=risk-oracle
    assert regret>=0
    return {'channels':channels,'expected_cost':risk,'oracle_cost':oracle,
            'regret':regret,'net_cost':risk+sensor_fee*len(channels),
            'policy':policy,'status':'SYNTHETIC_EXACT_NOT_MEASURED'}

def summarize():
    cases=[(),('aggregate',),('noisy_pocket',),('noisy_downstream',),
           ('noisy_or',),('motion_only',),('aggregate','noisy_pocket'),
           ('noisy_pocket','noisy_downstream'),('noisy_or','noisy_pocket')]
    return {'assumption':'conditional independence given toy state',
            'fee_unit':'invented dimensionless cost per sensor',
            'cases':[{'channels':list(c),
                      'cost':str(evaluate(c)['expected_cost']),
                      'regret':str(evaluate(c)['regret']),
                      'net_cost_fee_1_5':str(evaluate(c,sensor_fee=F(1,5))['net_cost'])}
                     for c in cases],
            'status':'SYNTHETIC_EXACT_NOT_MEASURED'}

if __name__=='__main__':
    print(json.dumps(summarize(),indent=2,ensure_ascii=False))
