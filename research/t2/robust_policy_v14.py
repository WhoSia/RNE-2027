"""Robust policy screen across eight synthetic rate/share/platoon contexts.

A policy is (pocket length, signal offset). The minimum context
throughput is a finite deterministic stress metric, NOT an empirical
confidence bound or justification to operate real signals.
"""
from collections import defaultdict
from statistics import mean
from pathlib import Path
import json

def evaluate(rows):
    groups=defaultdict(list)
    for r in rows:
        groups[(r['pocket_m'],r['signal_offset'])].append(r)
    output=[]
    for (pocket,offset),items in sorted(groups.items()):
        if len(items)!=8:
            raise ValueError('eight context scenarios required')
        output.append({'pocket_m':pocket,'signal_offset':offset,
            'mean_total_across_contexts':mean(r['mean_total'] for r in items),
            'min_total_across_contexts':min(r['mean_total'] for r in items),
            'mean_S_across_contexts':mean(r['mean_network_S'] for r in items),
            'mean_L_across_contexts':mean(r['mean_network_L'] for r in items),
            'min_S_across_contexts':min(r['mean_network_S'] for r in items)})
    return output

if __name__=='__main__':
    root=Path(__file__).resolve().parent/'results'
    rows=json.loads((root/'temporal_summary_v14.json').read_text())
    out=evaluate(rows)
    (root/'robust_policy_v14.json').write_text(json.dumps(out,indent=2)+'\n')
    print('policies',len(out))
