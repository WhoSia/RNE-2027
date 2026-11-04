"""Read-only external SUMO signal/connection crosswalk. Source files are never edited."""
from dataclasses import dataclass
from xml.etree import ElementTree as ET

@dataclass(frozen=True)
class SignalPlan:
    controller: str
    program: str
    cycle_s: float
    signal_slots: int
    phases: tuple

def parse_plans(xml_file):
    root = ET.parse(xml_file).getroot()
    plans = {}
    for logic in root.iter("tlLogic"):
        controller, program = logic.attrib["id"], logic.get("programID", "0")
        states = []
        for phase in logic.findall("phase"):
            duration = float(phase.attrib["duration"])
            if duration <= 0:
                raise ValueError("nonpositive signal phase")
            states.append((duration, phase.attrib["state"]))
        if not states or len({len(s) for _, s in states}) != 1:
            raise ValueError("inconsistent signal state slots")
        key = (controller, program)
        if key in plans:
            raise ValueError("duplicate signal program")
        plans[key] = SignalPlan(controller, program,
                                sum(d for d, _ in states), len(states[0][1]), tuple(states))
    return plans

def parse_controlled_connections(network_file):
    connections = {}
    for e in ET.parse(network_file).getroot().iter("connection"):
        controller = e.get("tl")
        if controller:
            connections.setdefault(controller, []).append(int(e.attrib["linkIndex"]))
    return connections

def validate_crosswalk(plans, connections):
    errors = []
    for (_, _), plan in plans.items():
        actual = sorted(connections.get(plan.controller, []))
        expected = list(range(plan.signal_slots))
        if actual != expected:
            errors.append((plan.controller, expected, actual))
    if errors:
        raise ValueError(f"SUMO network-to-signal linkIndex mismatch: {errors}")
    return {x.controller: {"cycle_s": x.cycle_s, "slots": x.signal_slots}
            for x in plans.values()}
