"""Paired downstream closure experiment in SUMO and T2."""
import json
from itertools import product
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import xml.etree.ElementTree as ET

from p39_engine_bridge import t2_case
from sumo_phase_pair import DEMAND, HORIZON, outcome, prepare, write


def sumo_run(folder, order, capacity, closed, *, step_size=.25, action_step=None):
    prepare(folder, order, yellow=False)
    nodes = ET.parse(folder / "nodes.nod.xml").getroot()
    nodes.remove(nodes.find("node[@id='left']"))
    boundary = nodes.find("node[@id='straight']")
    boundary.attrib.update(x=str(5 * capacity), type="traffic_light")
    ET.SubElement(nodes, "node", id="out", x="100", y="0")
    edges = ET.parse(folder / "edges.edg.xml").getroot()
    edges.remove(edges.find("edge[@id='L']"))
    edges.find("edge[@id='T']").set("length", str(5 * capacity))
    ET.SubElement(edges, "edge", id="X", numLanes="1", speed="10",
                  **{"from": "straight", "to": "out"})
    links = ET.parse(folder / "links.con.xml").getroot()
    links.find("connection[@to='L']").set("to", "T")
    ET.SubElement(links, "connection", fromLane="0", toLane="0", tl="straight",
                  linkIndex="0", **{"from": "T", "to": "X"})
    signals = ET.parse(folder / "signal.tll.xml").getroot()
    program = ET.SubElement(signals, "tlLogic", id="straight", type="static",
                            programID="0", offset="0")
    for duration, state in ((30, "G"), (30, "r")):
        ET.SubElement(program, "phase", duration=str(duration), state=state)
    demand = ET.parse(folder / "demand.rou.xml").getroot()
    demand.find("vType").attrib.update(length="4.5", minGap=".5")
    if action_step is not None:
        demand.find("vType").set("actionStepLength", str(action_step))
    for v in demand.findall("vehicle"):
        v.find("route").set("edges", "A T X")
    for name, tree in (("nodes.nod.xml", nodes), ("edges.edg.xml", edges),
                       ("links.con.xml", links), ("signal.tll.xml", signals),
                       ("demand.rou.xml", demand)):
        write(folder, name, tree)
    subprocess.run(["netconvert", "-n", "nodes.nod.xml", "-e", "edges.edg.xml",
                    "-x", "links.con.xml", "-i", "signal.tll.xml", "--no-internal-links",
                    "true", "-o", "net.xml"], cwd=folder, check=True, capture_output=True)
    root = ET.Element("additional")
    ET.SubElement(root, "timedEvent", type="SaveTLSStates", source="straight", dest="tls.xml")
    if closed:
        # Override startup only. The next scheduled green starts at second 60.
        startup = ET.SubElement(root, "tlLogic", id="straight", type="static",
                                programID="startup", offset="0")
        ET.SubElement(startup, "phase", duration="60", state="r", next="1")
        ET.SubElement(startup, "phase", duration="30", state="G", next="2")
        ET.SubElement(startup, "phase", duration="30", state="r", next="1")
    write(folder, "startup.add.xml", root)
    argv = ["sumo", "-n", "net.xml", "-r", "demand.rou.xml",
            "--end", str(HORIZON), "--step-length", str(step_size), "--time-to-teleport", "-1",
            "--tripinfo-output", "trips.xml", "--tripinfo-output.write-unfinished", "true",
            "--tripinfo-output.write-undeparted", "true", "--fcd-output", "fcd.xml", "--collision-output", "collisions.xml", "--no-step-log", "true", "--seed", "17"]
    argv += ["-a", "startup.add.xml"]
    subprocess.run(argv, cwd=folder, check=True, text=True, capture_output=True)
    if ET.parse(folder / "collisions.xml").getroot().find("collision") is not None:
        raise ValueError("SUMO reported a collision")
    states = ET.parse(folder / "tls.xml").getroot().findall("tlsState")
    if len(states) != round(HORIZON / step_size) or any(
            float(state.get("time")) != i * step_size
            or state.get("state") != ("G" if (i * step_size) % 60 < 30
                                      and (not closed or i * step_size >= 50) else "r")
            for i, state in enumerate(states)):
        raise ValueError("Compiled receiver signal does not match T2 discharge calendar")
    ids = [e.get("id") for e in ET.parse(folder / "trips.xml").getroot().findall("tripinfo")]
    if sorted(ids) != sorted(v.ident for v in DEMAND):
        raise ValueError("SUMO vehicle accounting mismatch")
    crossings = {}
    last_upstream = {}
    for _, step in ET.iterparse(folder / "fcd.xml", events=("end",)):
        if step.tag != "timestep":
            continue
        for v in step.findall("vehicle"):
            ident, lane = v.get("id"), v.get("lane")
            stamp = float(step.get("time"))
            if lane in ("A_0", "A_1"):
                last_upstream[ident] = stamp
            elif lane == "T_0" and ident not in crossings:
                if stamp - last_upstream.get(ident, float("-inf")) != step_size:
                    raise ValueError("Receiver entry lacks an adjacent upstream observation")
                crossings[ident] = stamp
        step.clear()
    return outcome(crossings)


def experiment():
    rows = []
    with TemporaryDirectory() as path:
        for capacity, closed in product((2, 4), (False, True)):
            row = {"capacity": capacity, "closed": closed}
            row["sumo"] = [sumo_run(Path(path) / f"{capacity}-{closed}-{order}", order,
                                   capacity, closed) for order in (False, True)]
            row["t2"] = [t2_case(order, 10, capacity, receiver_mode="cells",
                                receiver_closures=((0, 50),) if closed else ())
                         for order in (False, True)]
            for name in ("sumo", "t2"):
                lag, lead = row[name]
                row[name + "_contrast"] = (lead["approach_vehicle_seconds"]
                                           - lag["approach_vehicle_seconds"])
            rows.append(row)
    return rows


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
