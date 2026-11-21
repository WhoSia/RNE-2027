"""RF06-B exact synthetic two-blockage observation equivalence / value of information.

Uses toy functions and algebra inspired at the concept level by Hu & Fan
(2024), DOI 10.1016/j.trb.2024.103057, and Zhang et al. (2026),
arXiv:2609.13212v2. DOES NOT reproduce either traffic network study.
No measured Wi-Fi, magnetometer, LiDAR, camera, signal timing or CIM dataset.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import isfinite, log2
import json

STATES = ((0, 0), (0, 1), (1, 0), (1, 1))  # pocket, downstream
SENSORS = ("aggregate_count", "any_rf_change", "pocket_probe",
           "downstream_probe", "motion_event")


def normalized_prior(weights=(1, 1, 1, 1)):
    """Return rational masses; weights are nonnegative finite rational inputs."""
    if len(weights) != len(STATES):
        raise ValueError("one weight per state required")
    amounts = []
    for x in weights:
        if isinstance(x, bool) or not isinstance(x, (int, float, Fraction)):
            raise ValueError("weights must be rational numeric")
        if isinstance(x, float) and not isfinite(x):
            raise ValueError("weights must be finite")
        weight = Fraction(str(x)) if isinstance(x, float) else Fraction(x)
        if weight < 0:
            raise ValueError("negative state probability weight")
        amounts.append(weight)
    z = sum(amounts, Fraction(0))
    if z == 0:
        raise ValueError("zero total state probability")
    return tuple(x / z for x in amounts)


def observation(state: tuple[int, int], channel: str) -> int:
    if state not in STATES:
        raise ValueError("unknown toy two-zone state")
    p, d = state
    if channel == "aggregate_count":
        return p + d
    if channel == "any_rf_change":
        return int(bool(p or d))
    if channel == "pocket_probe":
        return p
    if channel == "downstream_probe":
        return d
    if channel == "motion_event":
        return 0  # snapshots are explicitly stationary
    raise ValueError("unknown idealized channel")


def partition(channels: tuple[str, ...]) -> dict[tuple[int, ...], tuple[tuple[int,int], ...]]:
    if not isinstance(channels, tuple) or not channels:
        raise ValueError("nonempty tuple of channels required")
    if len(set(channels)) != len(channels):
        raise ValueError("duplicate channels")
    if any(c not in SENSORS for c in channels):
        raise ValueError("unknown observation channel")
    groups = defaultdict(list)
    for state in STATES:
        key = tuple(observation(state, c) for c in channels)
        groups[key].append(state)
    return {key: tuple(values) for key, values in groups.items()}


def _target_label(state, target: str):
    if target == "full_state":
        return state
    if target == "pocket":
        return state[0]
    if target == "downstream":
        return state[1]
    raise ValueError("target must be full_state, pocket or downstream")


def study(channels: tuple[str, ...], *, weights=(1, 1, 1, 1),
          target="full_state") -> dict:
    """Exact Bayes 0/1 loss, Shannon observation entropy, no fit/test leakage.

    Deterministic observation implies I(State; Observation)=H(Observation).
    Output Bayes error is target-specific; higher overall information need
    not minimize decision risk. No measurement process is modeled.
    """
    prior = normalized_prior(weights)
    groups = partition(channels)
    index = {state: i for i, state in enumerate(STATES)}
    masses = []
    accuracy = Fraction(0)
    for signature, group in groups.items():
        class_mass = defaultdict(Fraction)
        for state in group:
            class_mass[_target_label(state, target)] += prior[index[state]]
        masses.append(sum(class_mass.values(), Fraction(0)))
        accuracy += max(class_mass.values())
    entropy = -sum(float(x) * log2(float(x)) for x in masses if x > 0)
    risk = Fraction(1) - accuracy
    return {
        "channels": channels,
        "target": target,
        "observation_entropy_bits": entropy,
        "deterministic_mutual_information_bits": entropy,
        "bayes_error_fraction": risk,
        "bayes_error": float(risk),
        "partition": groups,
        "status": "ANALYTIC_IDEAL_SENSOR_NOT_MEASURED_CSI"
    }


def minimum_full_state_sensor_sets() -> tuple[tuple[str, ...], ...]:
    for size in range(1, len(SENSORS) + 1):
        winners = tuple(candidate
                        for candidate in combinations(SENSORS, size)
                        if study(candidate)["bayes_error_fraction"] == 0)
        if winners:
            return winners
    raise AssertionError("ideal sensors unexpectedly nonidentifying")


def _rational(x):
    if isinstance(x, bool) or not isinstance(x, (Fraction, int, float)):
        raise ValueError("dynamics coefficient must be finite rational")
    if isinstance(x, float) and not isfinite(x):
        raise ValueError("nonfinite coefficient")
    return Fraction(str(x)) if isinstance(x, float) else Fraction(x)


def linear_two_state_observability(a, b) -> dict:
    """For A=diag(a,b), C=(1,1), O=[C;C*A]; exact determinant b-a."""
    aa, bb = _rational(a), _rational(b)
    return {
        "determinant": bb-aa,
        "observable_rank_2": aa != bb,
        "two_states_first_aggregate": Fraction(1),
        "pocket_only_next_reading": aa,
        "downstream_only_next_reading": bb,
        "two_states_next_reading_gap": abs(bb-aa),
        "two_immediate_sensor_matrix_determinant": Fraction(-1),
        "status": "IDEAL_KNOWN_DYNAMICS_NO_UNKNOWN_INFLOW"
    }


def frozen_examples_json() -> str:
    cases = {
        "aggregate": study(("aggregate_count",)),
        "rf_or": study(("any_rf_change",)),
        "pocket": study(("pocket_probe",)),
        "motion_static": study(("motion_event",)),
        "aggregate_plus_pocket": study(("aggregate_count", "pocket_probe")),
        "rf_or_plus_pocket": study(("any_rf_change", "pocket_probe")),
        "pocket_target_aggregate": study(("aggregate_count",), target="pocket"),
        "pocket_target_local": study(("pocket_probe",), target="pocket"),
    }
    def compact(d):
        return {
            "entropy_bits": d["observation_entropy_bits"],
            "bayes_error": str(d["bayes_error_fraction"]),
            "separated_classes": len(d["partition"])
        }
    o = {
        "evidence_status": "MATHEMATICAL_TOY_NOT_MEASURED_SENSOR",
        "cases": {key: compact(val) for key, val in cases.items()},
        "minimal_full_state_sensor_sets": [list(c) for c in minimum_full_state_sensor_sets()],
        "stationary_equal_dynamics": {
            "determinant": str(linear_two_state_observability(1,1)["determinant"])
        },
        "near_equal_dynamics": {
            "determinant": str(linear_two_state_observability(Fraction(4,5), Fraction(81,100))["determinant"])
        },
    }
    return json.dumps(o, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


if __name__ == "__main__":
    print(frozen_examples_json(), end="")
