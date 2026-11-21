"""RF06-D: exact, INVENTED action-cost toy demonstrating task-specific sensor value.

Invented dimensionless costs, no traffic delay, RF observations, calibrated
vehicle state, signal timing, real controller, or CIM data.
Preregistered at RF06_POLICY_INFORMATION_VALUE_PREREG_20261121.md.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
import json
from rf_cause_observability import STATES, SENSORS, normalized_prior, observation, study


def synthetic_delta_cost(state) -> Fraction:
    """Cost change of an imaginary action vs baseline. Entirely hypothetical."""
    if state not in STATES:
        raise ValueError("unknown toy state")
    return Fraction(-2 if state[0] == 1 else 3)


def evaluate_information_value(channels: tuple[str, ...], *,
                               weights=(1, 1, 1, 1)) -> dict:
    """Conditional Bayes action, perfect-oracle comparison, exact rational."""
    if not isinstance(channels, tuple):
        raise ValueError("channels must be a tuple")
    if len(set(channels)) != len(channels):
        raise ValueError("duplicate observation channels")
    if any(c not in SENSORS for c in channels):
        raise ValueError("unknown ideal sensor")
    prior = normalized_prior(weights)
    grouping = defaultdict(list)
    for idx, state in enumerate(STATES):
        key = tuple(observation(state, ch) for ch in channels)
        grouping[key].append(idx)

    policy = {}
    total_cost = Fraction(0)
    for sig in sorted(grouping):
        indices = grouping[sig]
        weighted_delta = sum((prior[i] * synthetic_delta_cost(STATES[i])
                              for i in indices), Fraction(0))
        treat = weighted_delta < 0  # on tie choose baseline
        total_cost += weighted_delta if treat else 0
        policy[str(sig)] = "hypothetical_treatment" if treat else "baseline"

    oracle_cost = sum((min(Fraction(0), prior[i]*synthetic_delta_cost(state))
                       for i, state in enumerate(STATES)), Fraction(0))
    regret = total_cost-oracle_cost
    if regret < 0:
        raise AssertionError("Bayesian conditional policy beats oracle")
    state_info = study(channels,weights=weights)["observation_entropy_bits"] if channels else 0.0
    return {
        "channels": channels,
        "prior": tuple(str(x) for x in prior),
        "expected_toy_cost": total_cost,
        "perfect_state_oracle_toy_cost": oracle_cost,
        "regret_relative_to_oracle": regret,
        "full_state_information_bits": state_info,
        "policy": policy,
        "evidence_status": "INVENTED_COST_TABLE_EXACT_MATH_NO_TRAFFIC_POLICY_EVIDENCE",
    }


def frozen_policy_summary() -> str:
    wanted={
        "none":(),
        "aggregate":("aggregate_count",),
        "pocket":("pocket_probe",),
        "rf_or":("any_rf_change",),
        "downstream":("downstream_probe",),
        "motion":("motion_event",),
        "rf_or_and_pocket":("any_rf_change","pocket_probe"),
        "aggregate_and_pocket":("aggregate_count","pocket_probe"),
    }
    results={}
    for name,channels in wanted.items():
        data=evaluate_information_value(channels)
        results[name]={"expected_cost":str(data["expected_toy_cost"]),
                       "oracle_cost":str(data["perfect_state_oracle_toy_cost"]),
                       "regret":str(data["regret_relative_to_oracle"]),
                       "full_state_information_bits":data["full_state_information_bits"]}
    special=evaluate_information_value((),weights=(7,1,1,1))
    return json.dumps({
        "status":"ARBITRARY_HYPOTHETICAL_COSTS_NOT_ACTUAL_T2_DELTAJ",
        "hypothetical_intervention_delta_if_P0":"+3",
        "hypothetical_intervention_delta_if_P1":"-2",
        "cases":results,
        "asymmetric_no_sensor_oracle_regret":str(special["regret_relative_to_oracle"])
    },sort_keys=True,indent=2)+"\n"


if __name__=="__main__":
    print(frozen_policy_summary(),end="")
