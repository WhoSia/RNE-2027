"""T2 pre-registered synthetic arrival-clock diversity, without altering the canonical generator.

This module returns request arrivals, not traffic-model service admissions. Temporal
PRNG and turning-label PRNG streams are independent, both deterministically seeded.
"""
import hashlib
import json
import math
import random
from spatial_v10 import validate, arrivals

FAMILIES = ('legacy_deterministic', 'fixed_count_uniform', 'poisson_exponential')


def generate(base, family):
    validate(base)
    if family not in FAMILIES:
        raise ValueError('unknown arrival-clock family')
    if family == 'legacy_deterministic':
        return arrivals(base)
    times_rng = random.Random(811000 + base.seed)
    route_rng = random.Random(913000 + base.seed)
    if family == 'fixed_count_uniform':
        n = base.duration_s * base.demand_vph // 3600
        seconds = sorted(times_rng.randrange(base.duration_s) for _ in range(n))
    else:
        seconds = []
        if base.demand_vph:
            current = 0.0
            intensity = base.demand_vph / 3600.
            while True:
                current += times_rng.expovariate(intensity)
                if current >= base.duration_s:
                    break
                seconds.append(math.floor(current))
    return tuple((s, 'L' if route_rng.random() < base.left_fraction else 'S')
                 for s in seconds)


def tape_hash(tape):
    raw = json.dumps(tape, separators=(',', ':'), ensure_ascii=True).encode('ascii')
    return hashlib.sha256(raw).hexdigest()


def time_hash(tape):
    raw = json.dumps([t for t,_ in tape], separators=(',', ':')).encode('ascii')
    return hashlib.sha256(raw).hexdigest()
