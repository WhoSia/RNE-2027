"""Reproducible, paired 2x2 design and finite order counterexample search."""
from __future__ import annotations
import csv, hashlib, itertools, json, statistics
from dataclasses import asdict, replace
from pathlib import Path
from spatial_v05 import Config, simulate, build_arrivals

FORKS=(-21,-13)
CAPS=(2,4)
MODES=('leading','lagging')
SEEDS=tuple(range(10))


def run_matrix():
    rows=[]
    for mode in MODES:
        for seed in SEEDS:
            common=build_arrivals(Config(seed=seed))
            stream_hash=hashlib.sha256(json.dumps(common,separators=(',',':')).encode()).hexdigest()
            for fork in FORKS:
                for cap in CAPS:
                    c=Config(signal_mode=mode,seed=seed,fork_cells=fork,bay_limit=cap)
                    result=simulate(c,common)
                    stat=result['stats']
                    rows.append({'mode':mode,'seed':seed,'fork_cells':fork,'bay_limit':cap,
                                 'arrival_sha256':stream_hash,
                                 'exits':stat['exits'],'exit_left':result['route_exits'].get('L',0),
                                 'exit_through':result['route_exits'].get('S',0),
                                 'remaining':stat['remaining'],
                                 'cap_block_s':stat.get('fork_block_cap_s',0),
                                 'bay_gap_block_s':stat.get('fork_block_gap_bay_s',0),
                                 'down_gap_block_s':stat.get('fork_block_gap_downstream_s',0),
                                 'physical_slots':stat['bay_physical_slots'],
                                 'cycle_exits':result['cycle_exits']})
    return rows


def summarize(rows):
    groups={}
    interactions=[]
    for mode in MODES:
        for fork in FORKS:
            for cap in CAPS:
                group=[r for r in rows if r['mode']==mode and r['fork_cells']==fork and r['bay_limit']==cap]
                groups[f'{mode}|f{fork}|K{cap}']={
                    'mean_exits':statistics.mean(r['exits'] for r in group),
                    'min_exits':min(r['exits'] for r in group),
                    'max_exits':max(r['exits'] for r in group),
                    'mean_left':statistics.mean(r['exit_left'] for r in group),
                    'mean_through':statistics.mean(r['exit_through'] for r in group),
                    'mean_cap_block_s':statistics.mean(r['cap_block_s'] for r in group)}
        for seed in SEEDS:
            y={(r['fork_cells'],r['bay_limit']):r['exits'] for r in rows if r['mode']==mode and r['seed']==seed}
            # Interactions as (K4-K2) at f=-13 minus (K4-K2) at f=-21
            I=(y[(-13,4)]-y[(-13,2)])-(y[(-21,4)]-y[(-21,2)])
            interactions.append({'mode':mode,'seed':seed,'interaction':I,
                'cap_effect_f_minus21':y[(-21,4)]-y[(-21,2)],
                'cap_effect_f_minus13':y[(-13,4)]-y[(-13,2)]})
    return {'cells_ft':25,'time_step_s':1,'seeds':list(SEEDS),
            'modes':list(MODES),'forks':list(FORKS),'caps':list(CAPS),
            'groups':groups,'interactions':interactions,
            'mode_mean_interaction':{m:statistics.mean(x['interaction'] for x in interactions if x['mode']==m) for m in MODES},
            'mode_mean_paired_cap_effect':{m:{str(f):statistics.mean(x['cap_effect_f_minus21' if f==-21 else 'cap_effect_f_minus13'] for x in interactions if x['mode']==m) for f in FORKS} for m in MODES},
            'calibrated':False,'claim':'virtual gate K, not physical independent bay length'}


def order_witness():
    # Identical arrival timestamps and counts, but one sorted by route and one interleaved.
    # This is a constructive witness rather than an exhaustive proof.
    n=60
    seq1=('L',)*n+('S',)*n
    seq2=tuple(x for _ in range(n) for x in ('L','S'))
    common=tuple(range(n*2))
    a=tuple((t,route,'upstream') for t,route in zip(common,seq1))
    b=tuple((t,route,'upstream') for t,route in zip(common,seq2))
    c=Config(duration=150,signal_mode='leading',fork_cells=-13,bay_limit=4,demand_vph=0)
    ra=simulate(c,a,keep_events=True)
    rb=simulate(c,b,keep_events=True)
    return {'duration':c.duration,'config':asdict(c),
        'same_arrival_times':tuple(t for t,_,_ in a)==tuple(t for t,_,_ in b),
        'same_route_counts':sum(x[1]=='L' for x in a)==sum(x[1]=='L' for x in b),
        'sequence_A':'L*60 + S*60','sequence_B':'(L,S)*60',
        'exits_A':ra['stats']['exits'],'exits_B':rb['stats']['exits'],
        'left_A':ra['route_exits'].get('L',0),'left_B':rb['route_exits'].get('L',0),
        'through_A':ra['route_exits'].get('S',0),'through_B':rb['route_exits'].get('S',0),
        'bay_cap_block_A':ra['stats'].get('fork_block_cap_s',0),
        'bay_cap_block_B':rb['stats'].get('fork_block_cap_s',0),
        'events_A':ra['events'][:28], 'events_B':rb['events'][:28],
        'interpretation':'finite-horizon throughput under paired timestamps and route counts; not an invariant against alternate demand schedules'}


def main():
    rows=run_matrix()
    output=Path(__file__).resolve().parent/'results'
    output.mkdir(exist_ok=True)
    fieldnames=[x for x in rows[0] if x!='cycle_exits']
    with (output/'paired_runs.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows({k:v for k,v in row.items() if k!='cycle_exits'} for row in rows)
    s=summarize(rows)
    s['order_witness']=order_witness()
    (output/'summary.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('mean interactions',s['mode_mean_interaction'])
    print('mean cap effects',s['mode_mean_paired_cap_effect'])
    print('order witness',s['order_witness']['exits_A'],s['order_witness']['exits_B'])
    print('rows',len(rows))


if __name__=='__main__':
    main()
