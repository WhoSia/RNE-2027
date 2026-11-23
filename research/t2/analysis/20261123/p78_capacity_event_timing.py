"""Time the first capacity-dependent change in the paired policy contrast."""
import json
from collections import defaultdict
from dataclasses import replace
from pathlib import Path

from p75_trace_pairs import build_config, p31, run, schedule, score, signature, tape_hash


def replay(cell, ref, capacity):
    cfg = replace(build_config(ref["seed"], 900, cell["share"], 7, capacity, .5),
                  downstream_offset_s=15)
    tape = p31.clock(cfg.base, cell["clock"])
    assert tape_hash(tape) == ref["tape"]
    cp = run(cfg, tape, checkpoint_at=84, trace=True)
    arms = [run(cfg, tape, resume_from=cp, phase_overrides=schedule(d), trace=True)
            for d in (6, 10)]
    assert score(arms[1], 60) - score(arms[0], 60) == ref[f"delta_capacity_{capacity}"]
    return [signature(arm) for arm in arms], cfg.base.duration_s


def events_by_second(arms, kind):
    indexed = defaultdict(lambda: [[], [], [], []])
    for i, arm in enumerate(arms):
        for t, *vehicle in arm[kind]:
            indexed[t][i].append(vehicle)
    return indexed


def contrast(groups):
    short2, long2, short4, long4 = map(len, groups)
    return (long4 - short4) - (long2 - short2)


def experiment():
    rows = []
    for cell in json.loads(Path(__file__).with_name("P76_RESULT.json").read_text()):
        for ref in cell["rows"]:
            delta = ref["delta_capacity_4"] - ref["delta_capacity_2"]
            if delta == 0:
                continue
            arms2, horizon = replay(cell, ref, 2)
            arms4, _ = replay(cell, ref, 4)
            row = dict(seed=ref["seed"], share=cell["share"], clock=cell["clock"],
                       tape=ref["tape"], cost_contrast=delta)
            departures = events_by_second(arms2 + arms4, "departure")
            crossings = events_by_second(arms2 + arms4, "crossing")
            for kind, events in (("crossing", crossings), ("departure", departures)):
                first = next((t for t in sorted(events) if contrast(events[t])), None)
                row[kind] = None if first is None else dict(t=first, vehicles=events[first])
            # A departure at t removes one vehicle from every end-of-second census
            # from t through horizon-1, and from the terminal penalty.
            reconstructed = -sum(contrast(groups) * (horizon - t + 60)
                                 for t, groups in departures.items())
            assert reconstructed == delta
            rows.append(row)
    return rows


if __name__ == "__main__":
    for row in experiment():
        print(json.dumps(row, separators=(",", ":")))
