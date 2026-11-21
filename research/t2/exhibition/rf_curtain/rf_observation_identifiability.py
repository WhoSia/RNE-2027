"""Five-label ideal-observation identifiability gate for RF-CURTAIN.

This is an *analytical upper-bound / measurement-design aid*, NOT an RF
propagation model, CSI classifier, validation of traffic causality or a
replication of the ten-category Wu et al. (2024) spillback taxonomy.

Two static ideal occupancy flags, P (pocket) and D (downstream), are
insufficient to separate 'no demand' from 'free travel' at an instant.
An independent approach-demand flag A resolves that abstract alias.
Real CSI features may encode motion history; this result applies ONLY
to the fixed three-binary-observation model declared here.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import json

SENSORS = ("pocket", "downstream", "approach_demand")


@dataclass(frozen=True)
class ToyWorld:
    label: str
    pocket: bool
    downstream: bool
    approach_demand: bool


WORLDS = (
    ToyWorld("no_demand", False, False, False),
    ToyWorld("free", False, False, True),
    ToyWorld("pocket", True, False, True),
    ToyWorld("downstream", False, True, True),
    ToyWorld("both", True, True, True),
)
LABELS = tuple(w.label for w in WORLDS)


def _validate_sensors(sensors):
    if len(set(sensors)) != len(sensors):
        raise ValueError("duplicate sensor")
    if any(s not in SENSORS for s in sensors):
        raise ValueError("unknown ideal sensor")


def compatible_labels(observation: dict[str, bool | None]) -> tuple[str, ...]:
    """Exact, perfect-bit matching, allowing omitted / missing observations.

    Empty tuple means OUTSIDE DEFINED FIVE-WORLD MODEL, not 'no traffic'.
    It must not be turned into a plausible class by arbitrary tie-breaking.
    """
    _validate_sensors(tuple(observation))
    for value in observation.values():
        if value is not None and type(value) is not bool:
            raise ValueError("ideal observation values must be bool or None")
    return tuple(
        world.label for world in WORLDS
        if all(observation[s] is None or getattr(world, s) == observation[s]
               for s in observation)
    )


def partition(sensors: tuple[str, ...]) -> list[dict]:
    """Group five latent truth labels by indistinguishable sensor signatures."""
    _validate_sensors(sensors)
    groups = {}
    for world in WORLDS:
        signature = tuple(getattr(world, s) for s in sensors)
        groups.setdefault(signature, []).append(world.label)
    return [
        {"signature": list(sig), "labels": values, "size": len(values)}
        for sig, values in sorted(groups.items(), key=lambda item: repr(item[0]))
    ]


def audit() -> dict:
    results = []
    for count in range(len(SENSORS) + 1):
        for subset in combinations(SENSORS, count):
            groups = partition(subset)
            uniquely_identified = [
                label for group in groups if group["size"] == 1
                for label in group["labels"]
            ]
            results.append({
                "sensors": list(subset),
                "partition": groups,
                "distinct_observations": len(groups),
                "uniquely_identifiable_labels": uniquely_identified,
                "unique_label_count": len(uniquely_identified),
                "unresolved_label_count": len(LABELS) - len(uniquely_identified),
            })
    return {
        "status": "ANALYTIC_IDEAL_OCCUPANCY_ONLY_NOT_MEASURED_RF",
        "assumptions": [
            "Toy labels are user-defined, not Wu et al. 2024 ten traffic spillback categories",
            "P and D represent ideal static occupancy, not RF CSI or verified causal mechanism",
            "A is independently measured demand; NO invented sensor accuracy",
            "Instantaneous P and D cannot distinguish absent demand from free travel in this model",
            "CSI motion-history features might remove the alias; not ruled out by this analysis",
        ],
        "labels": list(LABELS),
        "sensor_combinations": results,
        "contradictory_example": {
            "observation": {"pocket": True, "approach_demand": False},
            "compatible": list(compatible_labels({"pocket": True, "approach_demand": False})),
            "decision": "OUTSIDE_DEFINED_MODEL_DO_NOT_GUESS",
        },
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, sort_keys=True, indent=2))
