"""Matched synthetic T2 green-extension screen across demand and road conditions."""
import json
from dataclasses import replace
from itertools import product
from statistics import mean

from p39_policy_holdout import build_config, p31, run, score, action, tape_hash


def experiment(seeds=range(201, 207)):
    rows = []
    for seed, demand, turn, family, capacity, offset in product(
        seeds, (900, 1800), (.2, .5), p31.FAMILIES, (2, 4), (0, 15)
    ):
        cfg = replace(build_config(seed, demand, turn, 14., capacity, .5),
                      downstream_offset_s=offset)
        tape = p31.clock(cfg.base, family)
        state = run(cfg, tape, checkpoint_at=84)
        pair = [run(cfg, tape, resume_from=state, phase_overrides=action(duration))
                for duration in (6, 10)]
        delta = [score(pair[1], penalty) - score(pair[0], penalty) for penalty in (0, 60)]
        rows.append(dict(seed=seed, demand=demand, turn=turn, family=family,
                         capacity=capacity, offset=offset, tape=tape_hash(tape),
                         delta0=delta[0], delta60=delta[1]))
    groups = {}
    for key in ('family', 'demand', 'turn', 'capacity', 'offset'):
        for value in sorted({r[key] for r in rows}):
            ds = [r['delta60'] for r in rows if r[key] == value]
            groups[f'{key}={value}'] = dict(n=len(ds), better=mean(d < 0 for d in ds),
                                           worse=mean(d > 0 for d in ds), mean_delta=mean(ds))
    return dict(groups=groups, rows=rows, tapes=len({r['tape'] for r in rows}),
                changed_sign=sum((r['delta0'] > 0)-(r['delta0'] < 0) !=
                                 (r['delta60'] > 0)-(r['delta60'] < 0) for r in rows))


if __name__ == '__main__':
    print(json.dumps(experiment(), indent=2))
