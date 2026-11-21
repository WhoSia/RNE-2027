"""P13: strict same-observation policy-sign audit, no traffic controller."""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
from collections import defaultdict


@dataclass(frozen=True)
class Record:
    world_id: str
    arrival_group: str
    observation: tuple[int, ...]
    delta_cost: float
    action_contract: str
    provenance: str

    def __post_init__(self):
        for value in (self.world_id, self.arrival_group, self.action_contract, self.provenance):
            if not isinstance(value, str) or not value.strip():
                raise ValueError("required nonempty string metadata")
        if not isinstance(self.observation, tuple) or len(self.observation) != 6:
            raise ValueError("six-count observation tuple required")
        if any(type(n) is not int or n < 0 for n in self.observation):
            raise ValueError("nonnegative integer counts required; bool forbidden")
        if type(self.delta_cost) not in (int, float) or not isfinite(self.delta_cost):
            raise ValueError("finite real difference required")


def audit(records: tuple[Record, ...], *, epsilon: float = 5.0) -> tuple[dict, ...]:
    """Group by exact six-count observation AND identical action definition.

    Numerical outcomes are assumed known per world. No assertion about field
    observations, operational legality, or independent random draws is made.
    """
    if type(epsilon) not in (int, float) or not isfinite(epsilon) or epsilon < 0:
        raise ValueError("invalid nonnegative epsilon")
    if any(not isinstance(record, Record) for record in records):
        raise TypeError("records must be Record")
    ids = [record.world_id for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError("world IDs must be unique")
    groups = defaultdict(list)
    for record in records:
        groups[(record.action_contract, record.observation)].append(record)
    answer = []
    for (action, observation), rows in sorted(groups.items()):
        values = [record.delta_cost for record in rows]
        low, high = min(values), max(values)
        strict = low < -epsilon and high > epsilon
        answer.append({
            "action_contract": action,
            "observation": observation,
            "world_rows": len(rows),
            "independent_arrival_groups": len({record.arrival_group for record in rows}),
            "minimum_delta": low,
            "maximum_delta": high,
            "epsilon": epsilon,
            "classification": (
                "STRICT_OPPOSITE_SIGNS_SAME_OBSERVATION" if strict else
                "NOT_STRICTLY_OPPOSITE_ON_THIS_OBSERVATION"
            ),
            "scope": "SYNTHETIC_DEVELOPMENT_SCREEN_NOT_FIELD_CAUSAL_EVIDENCE",
        })
    return tuple(answer)


def archive_correction_example():
    """The 2026-11-21 archive does not provide matching six-count vectors.

    Return only the logically supported weaker interpretation, not invented
    observation data to force a desired alias.
    """
    return {
        "archived_delta_pair": (34, -178),
        "six_counts_equal": False,
        "result": "DIFFERENT_OBSERVATIONS_NOT_A_STRICT_ALIAS",
        "source": "T2_ARRIVAL_CLOCK_AND_GREEN_ENVELOPE_FINDINGS.md",
    }
