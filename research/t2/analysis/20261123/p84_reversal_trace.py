"""Locate cumulative cost reversals in P83's strict rank-switch case."""
from dataclasses import replace
import json
from p75_trace_pairs import build_config, p31, run, schedule, score


def experiment():
    cfg = replace(build_config(748, 900, .25, 7, 4, .5), downstream_offset_s=15)
    tape = p31.clock(cfg.base, "platoon4")
    original = cfg.base.duration_s
    cfg = replace(cfg, base=replace(cfg.base, duration_s=original + 1200))
    cp = run(cfg, tape, checkpoint_at=84, trace=True)
    arms = [run(cfg, tape, resume_from=cp, phase_overrides=schedule(d), trace=True)
            for d in (6, 10)]
    cumulative = 0
    switches = []
    previous = 0
    cutoff = None
    last_occupied = 0
    for a, b in zip(*(r["frames"] for r in arms), strict=True):
        assert a["t"] == b["t"]
        counts = [f["outside"] + sum(len(f[k]) for k in ("A", "B", "pocket", "receiver"))
                  for f in (a, b)]
        if any(counts):
            last_occupied = a["t"]
        gap = counts[1] - counts[0]
        cumulative += gap
        sign = (cumulative > 0) - (cumulative < 0)
        if sign != previous:
            switches.append(dict(t=a["t"], delta=cumulative))
            previous = sign
        if a["t"] + 1 == original:
            cutoff = dict(t=a["t"], occupancy=counts, cumulative=cumulative,
                          penalized=cumulative + 60 * gap)
    assert cutoff["penalized"] == -172
    assert cumulative == score(arms[1], 0) - score(arms[0], 0) == 346
    return dict(cutoff=cutoff, sign_changes=switches, final=cumulative,
                first_empty_after_last_occupancy=last_occupied+1)


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
