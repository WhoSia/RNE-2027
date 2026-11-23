"""Locate hidden vehicle differences in P74's equal-cost two-slot cases."""
import json
from dataclasses import replace
from pathlib import Path
from p69_fixed_budget import build_config, p31, run, schedule, score, tape_hash


def signature(result):
    crossings = [(e["t"], e["vehicle_id"], e["movement"]) for e in result["service_events"]
                 if e["reason"] == "stopline_cross"]
    departures = []
    previous = set()
    for frame in result["frames"]:
        current = {item[1] for item in frame["receiver"]}
        departures.extend((frame["t"], ident) for ident in sorted(previous - current))
        previous = current
    assert len(departures) == result["network_out_S"] + result["network_out_L"]
    return dict(crossing=crossings, departure=departures, remaining=result["remaining"],
                denials=result["receiver_denied_attempts"])


def experiment():
    rows = []
    cells = json.loads(Path(__file__).with_name("P74_RESULT.json").read_text())
    for cell in cells:
        if cell["capacity"] != 2:
            continue
        for ref in cell["rows"]:
            cfg = replace(build_config(ref["seed"], 900, cell["share"], 7, 2, .5),
                          downstream_offset_s=15)
            tape = p31.clock(cfg.base, cell["clock"])
            assert tape_hash(tape) == ref["tape"]
            cp = run(cfg, tape, checkpoint_at=84, trace=True)
            arms = [run(cfg, tape, resume_from=cp, phase_overrides=schedule(d), trace=True) for d in (6, 10)]
            assert score(arms[1], 60) - score(arms[0], 60) == ref["delta"] == 0
            a, b = map(signature, arms)
            rows.append(dict(seed=ref["seed"], share=cell["share"], clock=cell["clock"],
                             counts=[len(a["departure"]), len(a["crossing"]), a["remaining"]],
                             differs={key: a[key] != b[key] for key in a}))
    return rows


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
