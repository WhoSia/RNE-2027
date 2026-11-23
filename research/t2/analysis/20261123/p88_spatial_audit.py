"""P88: exact spatial conservation audit of P87, same post-tick occupancy convention.

Run from research/t2/analysis/20261123:
  python p88_spatial_audit.py > P88_RESULT.json
No stochastic resampling: the 96 fixed P87 demand tapes are replayed.
"""
from collections import Counter
from dataclasses import replace
from itertools import product
import json
from pathlib import Path
from unittest.mock import patch

from receiving_cells_v15 import ReceivingCells
from p85_signal_coordination import build_config, p31, phases, run, score

HERE = Path(__file__).resolve().parent
ZONES = ("outside", "approach_A", "approach_B", "pocket", "receiver")


def aggregate(result):
    """Frame emitted AFTER entry and movements, exactly as scalar score accumulates."""
    total = Counter()
    vehicles = {}
    for f in result["frames"]:
        if f["t"] < 84:
            continue
        values = {"outside": f["outside"], "approach_A": len(f["A"]),
                  "approach_B": len(f["B"]), "pocket": len(f["pocket"]),
                  "receiver": len(f["receiver"])}
        total.update(values)
        for zone in ("approach_A", "approach_B", "pocket"):
            entries = f["pocket"] if zone == "pocket" else f[zone]
            for item in entries:
                vehicles.setdefault(item[1], Counter())[zone] += 1
    return dict(total), vehicles


def replay(cfg, tape, cp, period, onset):
    start_green = onset == "green"
    def green(link, tick):
        assert tick >= 84 and not link.config.closure_windows
        return ((tick - 84) % period < period // 2) == start_green

    with patch.object(ReceivingCells, "green", green):
        result = run(cfg, tape, resume_from=cp, phase_overrides=phases(6, "left_first"), trace=True)
    assert result["remaining"] == 0 and result["generated"] == len(tape)
    zone, vehicle = aggregate(result)
    scalar = {k: result[k] for k in
              ("outside_vehicle_seconds", "upstream_vehicle_seconds", "receiver_vehicle_seconds")}
    # The checkpoint has common pre-84 scalar counters; compare two arms via deltas, not absolutes.
    red_full = sum(len(f["receiver"]) == 4 and
                   (((f["t"] - 84) % period < period // 2) != start_green)
                   for f in result["frames"] if f["t"] >= 84)
    exits = sorted(({"t": e["t"], "id": e["vehicle_id"], "movement": e["movement"],
                     "lane": e["lane"]} for e in result["service_events"]
                    if e["reason"] == "stopline_cross" and e["t"] >= 84),
                   key=lambda e: (e["t"], str(e["id"]), e["lane"]))
    # Infer actual downstream network departures from consecutive post-tick receiver
    # snapshots; first comparison uses the frozen receiver before tick 84.
    previous = {item[1]: item[2] for item in cp["state"]["receiver"].snapshot()}
    downstream_departures = []
    for f in result["frames"]:
        if f["t"] < 84:
            continue
        current = {item[1]: item[2] for item in f["receiver"]}
        leaving = set(previous) - set(current)
        assert len(leaving) <= 1, ("multiple downstream departures", f["t"])
        for vehicle_id in leaving:
            downstream_departures.append({"t": f["t"], "id": vehicle_id,
                                          "movement": previous[vehicle_id]})
        previous = current
    old_count = cp["state"]["count"]
    expected_departures = sum(result["network_out_" + m] - old_count["network_out_" + m]
                              for m in ("S", "L"))
    assert len(downstream_departures) == expected_departures, (
        "downstream departure conservation", len(downstream_departures), expected_departures)
    return {"cost": score(result, 0), "denied": result["receiver_denied_seconds"],
            "full_red": red_full, "zones": zone, "vehicle_zones": vehicle,
            "scalar": scalar, "crossings": exits,
            "downstream_departures": downstream_departures}


def experiment():
    ref = json.loads((HERE / "P87_RESULT.json").read_text())
    reference = {(r["seed"], r["share"], r["clock"], r["onset"]): r
                 for r in ref["rows"]}
    assert len(reference) == 192
    rows, examples = [], []
    groups = Counter()
    for seed, share, clock in product(range(85001, 85017), (.25, .5, .75), p31.FAMILIES):
        cfg = build_config(seed, 900, share, 7, 4, .5)
        tape = p31.clock(cfg.base, clock)
        cfg = replace(cfg, base=replace(cfg.base, duration_s=1440), downstream_offset_s=0)
        cp = run(cfg, tape, checkpoint_at=84, trace=True)
        for onset in ("green", "red"):
            arms = [replay(cfg, tape, cp, p, onset) for p in (30, 60)]
            short, long = arms
            delta = {k: short[k] - long[k] for k in ("cost", "denied", "full_red")}
            key = (seed, share, clock, onset)
            assert delta == reference[key]["delta"], ("P87 replay mismatch", key, delta)
            zone_delta = {k: short["zones"][k] - long["zones"][k] for k in ZONES}
            assert sum(zone_delta.values()) == delta["cost"], ("spatial conservation", key)
            assert zone_delta["outside"] == (short["scalar"]["outside_vehicle_seconds"] -
                                             long["scalar"]["outside_vehicle_seconds"])
            assert sum(zone_delta[z] for z in ("approach_A", "approach_B", "pocket")) == (
                short["scalar"]["upstream_vehicle_seconds"] -
                long["scalar"]["upstream_vehicle_seconds"])
            assert zone_delta["receiver"] == (short["scalar"]["receiver_vehicle_seconds"] -
                                              long["scalar"]["receiver_vehicle_seconds"])
            category = ("blockage_down_cost_up" if delta["denied"] < 0 < delta["cost"]
                        else "both_down" if delta["denied"] < 0 and delta["cost"] < 0
                        else "other")
            groups[(onset, category)] += 1
            rows.append(dict(seed=seed, share=share, clock=clock, onset=onset,
                             category=category, delta=delta, zone_delta=zone_delta))
            if category in ("blockage_down_cost_up", "both_down") and not any(
                    e["onset"] == onset and e["category"] == category for e in examples):
                examples.append(dict(seed=seed, share=share, clock=clock, onset=onset,
                                     category=category, delta=delta, zone_delta=zone_delta,
                                     # Crossing order is a case study, not a universal mechanism.
                                     short_first_crossings=short["crossings"][:30],
                                     long_first_crossings=long["crossings"][:30],
                                     short_first_downstream_departures=short["downstream_departures"][:30],
                                     long_first_downstream_departures=long["downstream_departures"][:30]))
    assert len(rows) == 192
    assert groups[("green", "blockage_down_cost_up")] == 12
    assert groups[("red", "blockage_down_cost_up")] == 43
    return {"method": "post-tick zone occupancy, t>=84, 30s minus 60s",
            "score_definition": "outside+A+B+pocket+receiver; terminal penalty zero",
            "groups": {f"{a}/{b}": n for (a, b), n in sorted(groups.items())},
            "rows": rows, "examples": examples}


if __name__ == "__main__":
    print(json.dumps(experiment(), ensure_ascii=False, indent=2))
