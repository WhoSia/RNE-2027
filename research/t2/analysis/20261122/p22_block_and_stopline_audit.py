"""P22 preregistered evidence audit, synthetic blocks + published stopline bins.

Not a real controller recommendation, a same-state causal effect, or SUMO.
"""
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

SOURCES = {
    '12:00-12:15': ('traffic-volume_230924-120000_230924-121500.csv', '98e4e0a593702188c2d134cef1346cbc7501067c9ad421ddb9e72a1e6d9d1d15'),
    '18:00-18:15': ('traffic-volume_230924-180000_230924-181500.csv', '62bc193f77d7e54e761855ea7c8a82229d4a8a924a4b622de228588eb3b4bcfe'),
    '23:30-23:45': ('traffic-volume_230924-233000_230924-234500.csv', '00f6f29b2be6c2fa517077de3b7accbbfc75edddc92332534f00ad6b62312798'),
}


def source_volume(path, sha):
    path = Path(path)
    if hashlib.sha256(path.read_bytes()).hexdigest() != sha:
        raise ValueError('STOP: wrong raw DLR volume file digest')
    with path.open(encoding='utf-8', newline='') as f:
        dr = csv.DictReader(f)
        columns = dr.fieldnames
        if not columns or columns[0] != 'timestamp' or len(columns) != len(set(columns)):
            raise ValueError('invalid timestamp/movement columns')
        movement = columns[1:]
        if not movement:
            raise ValueError('no movement channels')
        rows = list(dr)
    if not rows:
        raise ValueError('empty observed source')
    parsed = [datetime.fromisoformat(x['timestamp']) for x in rows]
    if any(x.tzinfo is None for x in parsed):
        raise ValueError('naive timestamp')
    if len(set(parsed)) != len(parsed) or parsed != sorted(parsed):
        raise ValueError('duplicate or unordered timestamps')
    gaps = [(y-x).total_seconds() for x,y in zip(parsed, parsed[1:])]
    if any(x != 1 for x in gaps):
        raise ValueError('unexpected time grid gap')
    totals = Counter()
    simultaneous = Counter()
    for row in rows:
        count = 0
        for channel in movement:
            value = row[channel]
            if value not in ('0','1'):
                raise ValueError('only observed binary movement bins are supported')
            inc = int(value)
            totals[channel] += inc
            count += inc
        simultaneous[count] += 1
    return {
        'sha256': sha,
        'first_timestamp': parsed[0].isoformat(),
        'last_timestamp': parsed[-1].isoformat(),
        'seconds_observed': len(rows),
        'movement_columns': len(movement),
        'movement_names': movement,
        'recorded_crossing_bins': sum(totals.values()),
        'seconds_with_a_crossing': len(rows)-simultaneous[0],
        'max_simultaneous_movement_crossing_bins': max(simultaneous),
        'per_movement_crossings': dict(sorted(totals.items())),
        'unit': 'one-second movement-specific center-crossing indicator (metadata, not unique-ID trajectory)',
    }


def audit_p19(rows):
    if len(rows)!=256:
        raise ValueError('wrong frozen P19 row count')
    by_block = defaultdict(list)
    matching = defaultdict(set)
    for r in rows:
        key=(r['tape_hash'], r['downstream_offset_s'])
        by_block[key].append(r['model_delta'])
        matching[(r['tape_hash'],r['receiver_capacity'],r['pocket_m'],r['b_share'])].add(r['downstream_offset_s'])
    tapes = {k[0] for k in by_block}
    if len(tapes) != 16 or len(by_block)!=32 or any(len(v)!=8 for v in by_block.values()):
        raise ValueError('incorrect independent block structure')
    if len(matching)!=128 or any(v!={0,15} for v in matching.values()):
        raise ValueError('not exact matched cross-offset geometry')
    results={}
    for off in (0,15):
        subset=[r for r in rows if r['downstream_offset_s']==off]
        sums_by_seed=Counter()
        for r in subset:
            sums_by_seed[r['seed']]+=r['model_delta']
        base=sum(sums_by_seed.values())
        results[str(off)]={
            'worlds':len(subset),
            'positive_cost_delta':sum(r['model_delta']>0 for r in subset),
            'negative_cost_delta':sum(r['model_delta']<0 for r in subset),
            'ties':sum(r['model_delta']==0 for r in subset),
            'positive_gt5':sum(r['model_delta']>5 for r in subset),
            'tape_blocks':len(tapes),
            'tape_blocks_with_any_positive':sum(any(x>0 for x in by_block[(t,off)]) for t in tapes),
            'tape_blocks_with_positive_gt5':sum(any(x>5 for x in by_block[(t,off)]) for t in tapes),
            'sum_model_delta_over_reused_worlds':base,
            'leave_one_seed_out_total_by_seed':{str(s):base-sums_by_seed[s] for s in sorted(sums_by_seed)},
        }
    # Probability statement valid only under IID/exchangeable random tape blocks.
    return {'worlds':len(rows),'unique_full_tape_hashes':len(tapes),
        'tape_offset_blocks':len(by_block),'matched_offset_geometry_pairs':len(matching),
        'effects':results,
        'iid_block_based_zero_of_16_one_sided_95pct_upper_probability':1-math.exp(math.log(.05)/16),
        'warning':'IID/exchangeability is not established; 16 tape hashes do not represent 128 field trials. Across offsets predecision checkpoint states differ.'}


def produce(p19_path, data_dir):
    raw=json.loads(Path(p19_path).read_text(encoding='utf-8'))
    volumes={k:source_volume(Path(data_dir)/filename,sha) for k,(filename,sha) in SOURCES.items()}
    return {'protocol':'P22_PRE_REGISTERED_ADVERSARIAL_BLOCK_AND_STOPLINE',
        'sources':'GitHub-main P19 sealed result + immutable Drive DLR 1s stopline volume CSVs',
        'frozen_preinspection_windows':list(SOURCES),
        'p19':audit_p19(raw['records']), 'observed_stopline':volumes,
        'data_limits':[
            'All observed DLR files refer to one Sunday 2023-09-24; periods are time blocks not independent dates.',
            'Movement columns vary by window (source schema drift); missing columns do not prove zero count.',
            'The observed volume columns cannot identify vehicle IDs, signal control heads, or sub-second headways.',
            'Crossing count and congestion/queue length are different physical variables.',
            'P19 model treatment sign is not a real-world traffic light safety or policy effect.',
        ]}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('p19_results',type=Path)
    p.add_argument('volume_dir',type=Path)
    p.add_argument('output',type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(produce(a.p19_results,a.volume_dir),sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
