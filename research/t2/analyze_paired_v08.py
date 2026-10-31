"""Deterministic paired comparisons from the sealed v0.8 CSV."""
import csv,statistics,json
from pathlib import Path

def analyze(source):
    raw=list(csv.DictReader(Path(source).open()))
    rows=[{k:(int(v) if k in ('seed','through_exits','left_exits','block_L_s','external_max','total_exits') else float(v) if k in ('left_share','length_m') else v=='True' if k=='leading' else v) for k,v in x.items()} for x in raw]
    index={(r['left_share'],r['seed'],r['leading'],r['length_m']):r for r in rows}
    if len(index)!=len(rows):raise ValueError('duplicate factorial cells')
    ratios=sorted({r['left_share'] for r in rows})
    seeds=sorted({r['seed'] for r in rows})
    phases=sorted({r['leading'] for r in rows})
    lengths=sorted({r['length_m'] for r in rows})
    if len(rows)!=len(ratios)*len(seeds)*len(phases)*len(lengths):
        raise ValueError('incomplete design')
    results=[]
    for p in ratios:
        for leading in phases:
            for a,b in zip(lengths,lengths[1:]):
                deltas=[index[p,seed,leading,b]['through_exits']-index[p,seed,leading,a]['through_exits'] for seed in seeds]
                results.append({'left_share':p,'leading':leading,'from_m':a,'to_m':b,
                    'n_seeds':len(deltas),'paired_through_gain_veh':statistics.mean(deltas),
                    'min_gain':min(deltas),'max_gain':max(deltas),
                    'nonnegative_seeds':sum(d>=0 for d in deltas),'each_seed_gain':deltas})
    return {'source_rows':len(rows),'design':{'ratios':ratios,'seeds':seeds,
        'phases':phases,'lengths_m':lengths},'paired_contrasts':results,
        'warning':'Simulator seed variability is not empirical uncertainty; no field calibration'}

if __name__=='__main__':
    import sys
    print(json.dumps(analyze(sys.argv[1]),indent=2,ensure_ascii=False))
