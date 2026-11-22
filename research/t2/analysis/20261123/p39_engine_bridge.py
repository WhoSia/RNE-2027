"""Nominal-schedule bridge and separate within-engine sensitivity contrasts."""
from itertools import product
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from dual_lane_v11 import DualConfig, run
from spatial_v10 import Config
from sumo_phase_pair import DEMAND, HORIZON, execute, outcome, prepare


def t2_case(left_first, pocket, receiver, *, receiver_closures=(), receiver_mode="fifo", receiver_headway=2, movement_details=False, through_share=1, receiver_offset=0):
    base = Config(duration_s=HORIZON, cycle_s=60, left_green_s=12, through_green_s=24,
                  clearance_s=5, phase_order="leading" if left_first else "lagging",
                  approach_length_m=100, pocket_length_m=pocket, cell_m=5)
    cfg = DualConfig(base=base, through_B_share=through_share, receiver_slots=receiver,
                     receiver_closures=receiver_closures, receiver_mode=receiver_mode,
                     receiver_headway_s=receiver_headway, downstream_offset_s=receiver_offset)
    result = run(cfg, tuple((v.time, "S" if v.movement == "T" else "L") for v in DEMAND),
                 trace=True)
    crossings = {}
    for event in result["service_events"]:
        if event["reason"] == "stopline_cross":
            ident = DEMAND[event["vehicle_id"]].ident
            if ident in crossings:
                raise ValueError("duplicate T2 crossing")
            crossings[ident] = event["t"]
    details = {"crossing_times": crossings} if movement_details else {}
    if movement_details:
        admitted = {}
        released = {}
        previous = set()
        for frame in result["frames"]:
            for lane in ("A", "B", "pocket"):
                for _, vehicle, *_ in frame[lane]:
                    admitted.setdefault(DEMAND[vehicle].ident, frame["t"])
            if receiver_mode == "cells":
                current = {vehicle for _, vehicle, _ in frame["receiver"]}
                for vehicle in previous - current:
                    released[DEMAND[vehicle].ident] = frame["t"]
                previous = current
        details.update(admitted=admitted, released=released, service_events=result["service_events"])
    return outcome(crossings) | details | {
        "receiver_denials": sum(e["reason"] in ("receiver_entry_cell_busy", "receiver_capacity_full")
                                for e in result["service_events"]),
        "pocket_access_denials": sum(e["event"] == "pocket_entry_denied"
                                    for e in result["access_events"]),
    }


def experiment():
    engines = {"SUMO": [], "T2": []}
    with TemporaryDirectory() as directory:
        for i, (yellow, tau) in enumerate(product((False, True), (1, 1.5))):
            pair = []
            for left_first in (False, True):
                folder = Path(directory) / f"{i}-{left_first}"
                prepare(folder, left_first, yellow=yellow, tau=tau)
                report = execute(folder, left_first, yellow=yellow)
                if report["sumo_status"] != "EXECUTED":
                    raise RuntimeError(report)
                pair.append(report["sumo"])
            engines["SUMO"].append({"yellow": yellow, "tau": tau, "pair": pair})
    for pocket, receiver in product((10, 30), (0, 2, 4)):
        engines["T2"].append({"pocket_m": pocket, "receiver_slots": receiver,
                              "pair": [t2_case(order, pocket, receiver) for order in (False, True)]})
    engines["T2_receiver_stress"] = [
        {"pocket_m": 10, "receiver_slots": cap, "receiver_closures": closures,
         "pair": [t2_case(order, 10, cap, receiver_closures=closures, receiver_mode="cells")
                  for order in (False, True)]}
        for cap, closures in product((2, 4), ((), ((0, 50),)))
    ]
    for rows in engines.values():
        for row in rows:
            lag, lead = row["pair"]
            row["lead_minus_lag_vehicle_s"] = (
                lead["approach_vehicle_seconds"] - lag["approach_vehicle_seconds"]
            )
    return engines


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
