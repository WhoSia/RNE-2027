"""Exact logical observation benchmark; not an RF or road model."""
from itertools import combinations, product
import json

FIELDS = ('discharge', 'demand', 'pocket_block', 'downstream_block')

def worlds():
    for demand, pocket, downstream in product((0, 1), repeat=3):
        label = 'no_demand' if not demand else {
            (0, 0): 'free', (1, 0): 'pocket',
            (0, 1): 'downstream', (1, 1): 'both'
        }[pocket, downstream]
        yield dict(demand=demand, pocket_block=pocket,
                   downstream_block=downstream,
                   discharge=int(demand and not pocket and not downstream),
                   label=label)

def partition(fields):
    cells = {}
    for w in worlds():
        key = tuple(w[f] for f in fields)
        cells.setdefault(key, set()).add(w['label'])
    return {'fields': list(fields), 'cells': len(cells),
            'ambiguous_cells': sum(len(v) > 1 for v in cells.values()),
            'max_candidate_labels': max(map(len, cells.values())),
            'identifies_label': all(len(v) == 1 for v in cells.values()),
            'groups': [{'observation': list(k), 'labels': sorted(v)}
                       for k, v in sorted(cells.items())]}

def audit():
    rows = [partition(f) for n in range(len(FIELDS)+1)
            for f in combinations(FIELDS, n)]
    minimal = [r['fields'] for r in rows if r['identifies_label'] and
               not any(s['identifies_label'] and set(s['fields']) < set(r['fields'])
                       for s in rows)]
    return {'status': 'EXACT_LOGICAL_BENCHMARK_NOT_MEASUREMENT',
            'latent_worlds': 8, 'subsets': rows, 'minimal_identifying_sets': minimal}

if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
