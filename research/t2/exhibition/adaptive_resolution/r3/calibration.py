"""Prospective paired token-observation ledger validator; no empirical evidence supplied."""
import csv,json,math,re,sys
from collections import defaultdict,Counter
from fractions import Fraction as F
FIELDS=('block_id','stage','split','source_kind','truth_s','truth_l','status','obs_s','obs_l')

def occupancy(v):
    if v not in ('0','1','2'):raise ValueError('occupancy outside capacity')
    return int(v)

def wilson(k,n):
    if not n:return None
    z=1.959963984540054;p=k/n;den=1+z*z/n
    mid=(p+z*z/(2*n))/den;rad=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [max(0,mid-rad),min(1,mid+rad)]

def audit(rows):
    keys=set();blocks={};sources=set();counts=defaultdict(Counter);tables=defaultdict(Counter);nblock=defaultdict(set)
    for r in rows:
        if set(r)!=set(FIELDS) or any(v is None for v in r.values()):raise ValueError('unexpected columns or missing cells')
        b,t,split,src=r['block_id'],r['stage'],r['split'],r['source_kind']
        if not re.fullmatch(r'B[0-9]{1,6}',b) or t not in ('1','2','3','4','5','6'):raise ValueError('anonymous block/stage required')
        if split not in ('calibration','validation') or src not in ('synthetic','teacher_approved_tabletop'):raise ValueError('split/source')
        if (b,t) in keys or (b in blocks and blocks[b]!=split):raise ValueError('duplicate or split leakage')
        keys.add((b,t));blocks[b]=split;sources.add(src);nblock[split].add(b)
        truth=tuple(occupancy(r[k]) for k in ('truth_s','truth_l'));status=r['status'];c=counts[split];c['total']+=1
        if status in ('missing','invalid'):
            if r['obs_s'] or r['obs_l']:raise ValueError('missing/invalid outcome must be blank')
            c[status]+=1;tables[split][f'{truth}->{status}']+=1;continue
        if status!='observed':raise ValueError('status')
        o=tuple(occupancy(r[k]) for k in ('obs_s','obs_l'));tables[split][f'{truth}->{o}']+=1
        if truth[0]==truth[1]:c['symmetric']+=1;c['nonswap']+=int(o!=truth)
        elif o==truth:c['correct_unequal']+=1
        elif o==truth[::-1]:c['swap_unequal']+=1
        else:c['nonswap']+=1
    if len(sources)!=1 or set(counts)!={'calibration','validation'}:raise ValueError('one source kind and both disjoint splits required')
    result={}
    for s,c in counts.items():
        n=c['correct_unequal']+c['swap_unequal'];k=c['swap_unequal'];fit=n>0 and not any(c[x] for x in ('missing','invalid','nonswap')) and 2*k<=n
        result[s]={'counts':dict(c),'blocks':len(nblock[s]),'informative_valid_unequal':n,'conditional_swap_fraction':str(F(k,n)) if n else None,'wilson_95_descriptive':wilson(k,n),'swap_only_fit_candidate':str(F(k,n)) if fit and s=='calibration' else None,'swap_only_compatible_observed':bool(fit),'confusion':dict(tables[s])}
    return {'source_kind':sources.pop(),'source_is_declared_not_independently_verified':True,'splits':result,'warning':'Wilson intervals assume independent Bernoulli trials; repeated stages within blocks can be dependent. Conditional swap fractions exclude missing/invalid/non-swap outcomes. No sensor calibration or validation claim from synthetic fixture; validation split never fits.'}

def read(path):
    with open(path,newline='',encoding='utf-8-sig') as f:
        d=csv.DictReader(f)
        if tuple(d.fieldnames or ())!=FIELDS:raise ValueError('exact schema required')
        return audit(d)
if __name__=='__main__':print(json.dumps(read(sys.argv[1]),indent=2))
