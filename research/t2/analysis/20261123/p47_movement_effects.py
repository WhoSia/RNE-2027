"""Describe per-movement changes inside equal-cost policy pairs."""
from collections import Counter
from dataclasses import replace
from itertools import product
import json
from unittest.mock import patch

from p41_tail_audit import metrics, REGIMES, action, build_config, p31, run, score


def experiment():
    totals = Counter()
    by_family = {}
    with patch.object(p31, "PLATOON_SPAN", 5):
        for family in p31.FAMILIES:
            counts = Counter(dict.fromkeys(("ties", "offsetting_movements",
                                            "mixed_vehicle_effects", "benefit_over_10s",
                                            "harm_over_10s"), 0))
            for (seed, demand, turn), cap, offset, pocket, share in product(
                    REGIMES, (2, 4), (0, 15), (14., 28.), (0., .5)):
                cfg = replace(build_config(seed, demand, turn, pocket, cap, share),
                              downstream_offset_s=offset)
                tape = p31.clock(cfg.base, family)
                cp = run(cfg, tape, checkpoint_at=84, trace=True)
                a, b = [run(cfg, tape, resume_from=cp, phase_overrides=action(d), trace=True)
                        for d in (6, 10)]
                if score(a, 60) != score(b, 60):
                    continue
                counts["ties"] += 1
                first, second = (metrics(r, tape, cfg.base.duration_s)[1] for r in (a, b))
                deltas = [end[0] - start[0] for start, end in zip(first, second, strict=True)]
                movement_delta = Counter()
                for (_, movement), delta in zip(tape, deltas, strict=True):
                    movement_delta[movement] += delta
                counts["offsetting_movements"] += movement_delta["L"] * movement_delta["S"] < 0
                counts["mixed_vehicle_effects"] += min(deltas) < 0 < max(deltas)
                counts["benefit_over_10s"] += min(deltas) < -10
                counts["harm_over_10s"] += max(deltas) > 10
                totals.update(deltas)
            by_family[family] = dict(counts)
    return {"families": by_family, "vehicle_delta_histogram": dict(totals)}


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
