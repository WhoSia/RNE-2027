"""Paired synthetic protected-left benchmark with dedicated approach lanes."""
import argparse
from itertools import groupby
from collections import deque
from math import isfinite
from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class Arrival:
    ident: str
    time: int
    movement: str


APPROACH_M = 100
SPEED_M_S = 10
HORIZON = 180
DEMAND = tuple(Arrival(f"v{i:02}", 2*i, "L" if i % 3 == 1 else "T")
               for i in range(24))


def phases(left_first, *, yellow=True):
    through = ((24, "Gr"), (3, "yr"), (2, "rr"))
    left = ((12, "rG"), (3, "ry"), (2, "rr"))
    order = left + through if left_first else through + left
    cycle = order + ((14, "rr"),)
    if yellow:
        return cycle
    return tuple((length, state.replace("y", "r")) for length, state in cycle)


def write(folder, name, element):
    ET.indent(element)
    ET.ElementTree(element).write(folder / name, encoding="utf-8", xml_declaration=True)


def prepare(folder, left_first, *, yellow=True, tau=1):
    if not isfinite(tau) or tau <= 0:
        raise ValueError("Krauss tau must be finite and positive")
    folder.mkdir(parents=True, exist_ok=True)
    nodes = ET.Element("nodes")
    for name, x, y in (("in", -100, 0), ("j", 0, 0), ("straight", 40, 0), ("left", 0, 40)):
        ET.SubElement(nodes, "node", id=name, x=str(x), y=str(y),
                      type="traffic_light" if name == "j" else "dead_end")
    edges = ET.Element("edges")
    for name, start, end, lanes, length in (("A", "in", "j", 2, APPROACH_M),
                                           ("T", "j", "straight", 1, 40),
                                           ("L", "j", "left", 1, 40)):
        ET.SubElement(edges, "edge", {"id": name, "from": start, "to": end,
                                      "numLanes": str(lanes), "speed": str(SPEED_M_S),
                                      "length": str(length)})
    connections = ET.Element("connections")
    for index, movement in enumerate(("T", "L")):
        ET.SubElement(connections, "connection", {"from": "A", "to": movement,
                                                   "fromLane": str(index), "toLane": "0",
                                                   "tl": "j", "linkIndex": str(index)})
    signals = ET.Element("tlLogics")
    program = ET.SubElement(signals, "tlLogic", id="j", type="static", programID="0", offset="0")
    for duration, state in phases(left_first, yellow=yellow):
        ET.SubElement(program, "phase", duration=str(duration), state=state)
    routes = ET.Element("routes")
    ET.SubElement(routes, "vType", id="car", carFollowModel="Krauss", sigma="0",
                  accel="2", decel="4.5", tau=format(tau, "g"), minGap="2", length="4.5", maxSpeed="10")
    for trip in DEMAND:
        vehicle = ET.SubElement(routes, "vehicle", id=trip.ident, type="car", depart=str(trip.time),
                                departLane="1" if trip.movement == "L" else "0",
                                departSpeed=str(SPEED_M_S), departPos="0")
        ET.SubElement(vehicle, "route", edges="A " + trip.movement)
    for name, tree in (("nodes.nod.xml", nodes), ("edges.edg.xml", edges),
                       ("links.con.xml", connections), ("signal.tll.xml", signals), ("demand.rou.xml", routes)):
        write(folder, name, tree)


def point_service_windows(left_first, movement, amber_service_s=0):
    """Return half-open service windows within the nominal cycle."""
    if not 0 <= amber_service_s <= 3:
        raise ValueError("point service extension must fit the amber interval")
    index = ("T", "L").index(movement)
    start = 0
    for duration, state in phases(left_first):
        if state[index] == "G":
            yield start, start + duration + amber_service_s
        start += duration


def point_departures(left_first, *, start_loss=2, headway=2, travel_time=APPROACH_M / SPEED_M_S,
                     amber_service_s=0):
    """Dedicated point queues, with optional continuous service into amber."""
    if not all(isfinite(v) and v >= 0 for v in (start_loss, travel_time)) or not isfinite(headway) or headway <= 0:
        raise ValueError("invalid point discharge parameters")
    crossed = {}
    cycle_duration = sum(duration for duration, _ in phases(left_first))
    for movement in ("T", "L"):
        windows = tuple(point_service_windows(left_first, movement, amber_service_s))
        ready = deque(trip for trip in DEMAND if trip.movement == movement)
        for cycle_start in range(0, HORIZON, cycle_duration):
            for first, last in windows:
                previous = cycle_start + first + start_loss - headway
                while ready:
                    candidate = max(ready[0].time + travel_time, previous + headway)
                    if candidate >= min(cycle_start + last, HORIZON):
                        break
                    crossed[ready.popleft().ident] = candidate
                    previous = candidate
    return crossed


def outcome(crossings):
    known = {trip.ident for trip in DEMAND}
    if not crossings.keys() <= known:
        raise ValueError("Unknown vehicle in crossing output")
    if any(not isfinite(t) or not trip.time <= t <= HORIZON
           for trip in DEMAND if (t := crossings.get(trip.ident)) is not None):
        raise ValueError("Crossing violates the scheduled time or horizon")
    return {"scheduled": len(known), "crossed": len(crossings),
            "uncrossed": len(known - crossings.keys()),
            "approach_vehicle_seconds": sum(min(crossings.get(t.ident, HORIZON), HORIZON) - t.time
                                           for t in DEMAND)}


def validate_network(network, left_first, *, yellow=True):
    root = ET.parse(network).getroot()
    links = {(c.get("to"), c.get("fromLane"), c.get("linkIndex"))
             for c in root.findall("./connection") if c.get("from") == "A" and c.get("tl") == "j"}
    program = root.find("./tlLogic[@id='j'][@programID='0']")
    if program is None or links != {("T", "0", "0"), ("L", "1", "1")}:
        raise ValueError("Compiled TLS links differ from input")
    compiled = tuple((float(p.get("duration")), p.get("state")) for p in program.findall("phase"))

    def state_timeline(sequence):
        return tuple((sum(duration for duration, _ in run), state)
                     for state, run in groupby(sequence, key=lambda interval: interval[1]))

    # netconvert can coalesce adjacent phases with the same signal state.
    if (program.get("type") != "static" or float(program.get("offset", "nan")) != 0
            or state_timeline(compiled) != state_timeline(phases(left_first, yellow=yellow))):
        raise ValueError("Compiled TLS phase program differs from input")


def crossing_brackets(fcd, step):
    """Bracket the edge change using the last upstream and first downstream sample."""
    expected = {trip.ident: trip for trip in DEMAND}
    prior = {}
    crossed = {}
    for _, elem in ET.iterparse(fcd, events=("end",)):
        if elem.tag != "timestep":
            continue
        stamp = float(elem.attrib["time"])
        for vehicle in elem.findall("vehicle"):
            ident = vehicle.attrib["id"]
            lane = vehicle.attrib["lane"]
            if ident not in expected:
                raise ValueError("FCD contains an unknown vehicle")
            trip = expected[ident]
            last = prior.get(ident)
            if lane == trip.movement + "_0" and ident not in crossed:
                if last is None or last[1] != ("A_0" if trip.movement == "T" else "A_1") or abs(stamp - last[0] - step) > 1e-7:
                    raise ValueError("Crossing lacks adjacent input-edge observation")
                if stamp > HORIZON or last[0] < trip.time:
                    raise ValueError("Crossing is outside the vehicle observation window")
                crossed[ident] = last[0], stamp
            prior[ident] = stamp, lane
        elem.clear()
    if not prior:
        raise ValueError("FCD did not contain any vehicle observations")
    return crossed



def crossing_times(fcd, step):
    return {ident: upper for ident, (_, upper) in crossing_brackets(fcd, step).items()}


def execute(folder, left_first, *, yellow=True, step=.25):
    from hashlib import file_digest
    import shutil
    import subprocess

    sums = {}
    binaries = {name: shutil.which(name) for name in ("sumo", "netconvert")}
    inputs = ("nodes.nod.xml", "edges.edg.xml", "links.con.xml", "signal.tll.xml", "demand.rou.xml")
    for name in inputs:
        with (folder / name).open("rb") as file:
            sums[name] = file_digest(file, "sha256").hexdigest()
    report = {"input_sha256": sums, "point_queue": outcome(point_departures(left_first))}
    missing = [name for name, path in binaries.items() if not path]
    if missing:
        return report | {"sumo_status": "NOT_EXECUTED", "missing": missing}
    if step not in (.25, .5, 1):
        raise ValueError("unsupported simulation step")
    commands = ([binaries["netconvert"], "--node-files", inputs[0], "--edge-files", inputs[1],
                 "--connection-files", inputs[2], "--tllogic-files", inputs[3],
                 "--no-internal-links", "true", "--output-file", "model.net.xml"],
                [binaries["sumo"], "-n", "model.net.xml", "-r", inputs[4],
                 "--end", str(HORIZON), "--step-length", str(step), "--seed", "17",
                 "--time-to-teleport", "-1", "--collision.action", "warn", "--no-step-log", "true",
                 "--fcd-output", "fcd.xml", "--tripinfo-output", "tripinfo.xml",
                 "--tripinfo-output.write-unfinished", "true", "--tripinfo-output.write-undeparted", "true"])
    try:
        subprocess.run(commands[0], cwd=folder, check=True, capture_output=True, text=True, timeout=60)
        validate_network(folder / "model.net.xml", left_first, yellow=yellow)
        run = subprocess.run(commands[1], cwd=folder, check=True, capture_output=True, text=True, timeout=90)
        if "collision" in run.stderr.lower():
            raise ValueError("SUMO reported a collision")
        observed = crossing_times(folder / "fcd.xml", step)
        trip_rows = [entry for entry in ET.parse(folder / "tripinfo.xml").getroot()
                     if entry.tag == "tripinfo"]
        tripinfo_ids = {entry.attrib["id"] for entry in trip_rows}
        if len(trip_rows) != len(DEMAND) or tripinfo_ids != {trip.ident for trip in DEMAND}:
            raise ValueError("Tripinfo does not account for each scheduled ID exactly once")
        if any(entry.attrib["id"] in observed and float(entry.attrib["depart"]) < 0 for entry in trip_rows):
            raise ValueError("FCD reports a crossing before SUMO insertion")
        raw = {}
        for name in ("model.net.xml", "fcd.xml", "tripinfo.xml"):
            with (folder / name).open("rb") as file:
                raw[name] = file_digest(file, "sha256").hexdigest()
        version = subprocess.check_output([binaries["sumo"], "--version"], text=True, timeout=15)
        return report | {"sumo_status": "EXECUTED", "sumo": outcome(observed),
                         "step_s": step, "raw_sha256": raw, "version": version.splitlines()[0]}
    except (subprocess.SubprocessError, OSError, ET.ParseError, ValueError) as exc:
        return report | {"sumo_status": "FAILED", "error": str(exc),
                         "stderr": (getattr(exc, "stderr", "") or "")[-1500:]}


if __name__ == "__main__":
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("run_directory", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report = {}
    for label, left_first in (("lagging_left", False), ("leading_left", True)):
        folder = args.run_directory / label
        prepare(folder, left_first)
        report[label] = execute(folder, left_first)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
