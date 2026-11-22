"""Audit 6/10-second aggregate cost ties for vehicle delay and backlog."""
from collections import Counter
from dataclasses import replace
from itertools import product
import json
from math import ceil
from unittest.mock import patch

from dual_lane_v11 import run
from p19_receiver_service_opportunity import build_config
from p25_p26_physical_followups import action
from p39_policy_holdout import REGIMES
from physical_transfer_screen import score
import p31_two_arrival_families as p31


def metrics(result, tape, horizon):
    crossed = {}
    for e in result["service_events"]:
        if e["reason"] == "stopline_cross":
            ident = e["vehicle_id"]
            if ident in crossed or not 0 <= ident < len(tape) or not tape[ident][0] <= e["t"] < horizon:
                raise ValueError("invalid crossing event")
            crossed[ident] = e["t"]
    times = sorted(crossed.get(i, horizon) - t for i, (t, _) in enumerate(tape))
    frames = result["frames"]
    if len(frames) != horizon:
        raise ValueError("incomplete backlog trace")
    return (times[ceil(.95 * len(times)) - 1],
            max(len(f["A"]) + len(f["B"]) + len(f["pocket"]) + f["outside"] for f in frames),
            len(tape) - len(crossed))


def experiment():
    bins = Counter()
    by_family = {}
    with patch.object(p31, "PLATOON_SPAN", 5):
        for family in p31.FAMILIES:
            counts = Counter()
            for (seed, demand, turn), cap, offset, pocket, share in product(
                    REGIMES, (2, 4), (0, 15), (14., 28.), (0., .5)):
                cfg = replace(build_config(seed, demand, turn, pocket, cap, share),
                              downstream_offset_s=offset)
                tape = p31.clock(cfg.base, family)
                cp = run(cfg, tape, checkpoint_at=84, trace=True)
                a, b = [run(cfg, tape, resume_from=cp, phase_overrides=action(d), trace=True)
                        for d in (6, 10)]
                counts["worlds"] += 1
                if score(a, 60) != score(b, 60):
                    continue
                counts["cost_ties"] += 1
                before, after = (metrics(r, tape, cfg.base.duration_s) for r in (a, b))
                for k, initial, final in zip(("p95", "peak_backlog", "uncrossed"), before, after):
                    counts[k + "_changed"] += initial != final
                    counts[k + "_worse"] += final > initial
                counts["any_changed"] += before != after
                bins[(after[0] - before[0], after[1] - before[1])] += 1
            by_family[family] = dict(counts)
    return {"families": by_family,
            "p95_peak_delta_histogram": [[a, b, n] for (a, b), n in sorted(bins.items())]}


if __name__ == "__main__":
    print(json.dumps(experiment(), sort_keys=True, indent=2))
