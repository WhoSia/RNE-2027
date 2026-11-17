"""Paired point-queue and SUMO sensitivity without retiming the green phases."""

import argparse
import json
from collections import Counter
from itertools import product
from pathlib import Path

from phase_pair_diagnostics import bracket_state, paired_departure_cost
from sumo_phase_pair import execute, crossing_brackets, phases, point_departures, prepare


def point_grid():
    rows = []
    for amber, headway, travel in product((0, .25, .5, 1, 3), (1.5, 1.75, 2, 2.25), (9.75, 10, 10.25)):
        contrast = paired_departure_cost(*(point_departures(
            lead, headway=headway, travel_time=travel, amber_service_s=amber) for lead in (False, True)))
        witness = contrast.pop("vehicles")["v01"]
        rows.append({"amber_service_s": amber, "headway_s": headway, "travel_s": travel,
                     **contrast, "first_left": witness})
    return rows

def sumo_grid(root):
    rows = []
    for yellow, tau, step in product((True, False), (.8, 1, 1.5), (.25, .5)):
        arms = []
        for lead in (False, True):
            folder = root / f"yellow-{yellow}_tau-{tau}_step-{step}_lead-{lead}"
            prepare(folder, lead, yellow=yellow, tau=tau)
            report = execute(folder, lead, yellow=yellow, step=step)
            if report["sumo_status"] != "EXECUTED":
                raise RuntimeError(f"SUMO failed in {folder.name}: {report}")
            brackets = crossing_brackets(folder / "fcd.xml", step)
            arms.append((report, brackets))
        (lag, lag_brackets), (lead, lead_brackets) = arms
        changed = {k for k, v in lag["input_sha256"].items() if lead["input_sha256"][k] != v}
        if changed != {"signal.tll.xml"} or lead["version"] != lag["version"]:
            raise RuntimeError("Paired SUMO inputs or simulator version differ")
        contrast = paired_departure_cost(*(
            {ident: upper for ident, (_, upper) in bracket.items()}
            for bracket in (lag_brackets, lead_brackets)
        ))
        vehicles = contrast.pop("vehicles")
        statuses = []
        for left_first, brackets in ((False, lag_brackets), (True, lead_brackets)):
            cycle = phases(left_first, yellow=yellow)
            statuses.append(dict(Counter(
                bracket_state(cycle, *window, vehicles[ident]["movement"])
                for ident, window in brackets.items()
            )))
        ranked = sorted(vehicles, key=lambda ident: (-abs(vehicles[ident]["delta"]), ident))
        rows.append({"yellow": yellow, "tau_s": tau, "step_s": step, **contrast, "version": lead["version"],
                     "signal_at_crossing": statuses, "leading_first_left_bracket": lead_brackets.get("v01"),
                     "largest_contributions": {ident: vehicles[ident] for ident in ranked[:3]}})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_directory", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report = {"point_model": point_grid(), "sumo": sumo_grid(args.run_directory)}
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
