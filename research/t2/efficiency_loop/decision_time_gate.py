"""Causal availability and minimax-regret bounds for two-arm signal sensing.

The numerical witnesses are archived *synthetic* cost differences (left-first
minus through-first), not estimates of field effects. A future schedule is
never treated as a live observation unless its timestamp passes the gate.
"""
from dataclasses import dataclass
from fractions import Fraction
import argparse
import json
from pathlib import Path

DECISION_TICK = 84


@dataclass(frozen=True)
class Evidence:
    name: str
    observed_tick: int
    processing_ticks: int = 0
    predictive: bool = False

    def admissible(self, decision_tick=DECISION_TICK):
        if self.processing_ticks < 0:
            raise ValueError("processing delay cannot be negative")
        # A prediction is admissible only if the *forecast* was issued before
        # commitment. It must not be constructed using a realized future event.
        return self.observed_tick + self.processing_ticks <= decision_tick


def fixed_regret(deltas):
    """Worst regret by deterministic order for nonempty compatible worlds."""
    values = tuple(deltas)
    if not values:
        raise ValueError("at least one compatible world required")
    left = max(0, max(values))
    through = max(0, -min(values))
    return {"left_first": left, "through_first": through,
            "minimax": min(left, through),
            "choice": "left_first" if left < through else
                      "through_first" if through < left else "either"}


def conditional_regret(worlds, observed):
    """Each entry is (world_key, delta). `observed` is a non-leaky key map."""
    groups = {}
    for key, delta in worlds:
        if key not in observed:
            raise ValueError(f"missing observation for world {key}")
        groups.setdefault(observed[key], []).append(delta)
    if not groups:
        raise ValueError("empty world set")
    base = fixed_regret(delta for _, delta in worlds)
    branches = {str(k): fixed_regret(v) for k, v in groups.items()}
    after = max(r["minimax"] for r in branches.values())
    if after > base["minimax"]:
        raise AssertionError("A valid partition cannot increase minimax regret")
    return {"before": base, "after": after,
            "guaranteed_reduction": base["minimax"]-after, "branches": branches}


def binary_certificate(early, late, *, decision=DECISION_TICK):
    """Analytical perfect/oracle and bounded-error results for two worlds."""
    if not early < 0 < late:
        raise ValueError("witness must strictly reverse phase preference")
    worlds = (("early", early), ("late", late))
    no_sensor = conditional_regret(worlds, {"early": "same", "late": "same"})
    oracle = conditional_regret(worlds, {"early": "early", "late": "late"})
    # If a binary channel reports the correct label with probability at least
    # 1-epsilon *for each true world*, following it has worst expected regret
    # max(-early,late)*epsilon. A fixed action remains available.
    large = max(-early, late)
    best_mixed = Fraction((-early)*late, late-early)
    fixed = no_sensor["before"]["minimax"]
    limit_fixed = Fraction(fixed, large)
    limit_mixed = best_mixed / large
    return {
        "deltas": [early, late], "fixed": fixed,
        "perfect_oracle": oracle["after"],
        "mixed_action_baseline": str(best_mixed),
        "error_bound_for_strict_gain_vs_fixed": str(limit_fixed),
        "error_bound_for_strict_gain_vs_mixed": str(limit_mixed),
        "max_regret_with_error_one_tenth": str(min(Fraction(fixed), Fraction(large, 10))),
        "gap_event_tick": decision,
        "zero_latency_current_gap_admissible": Evidence("gap_now", decision).admissible(decision),
        "one_tick_latency_current_gap_admissible": Evidence("gap_now", decision, 1).admissible(decision),
        "predecision_identical_worlds_regret": no_sensor["after"],
    }


def report():
    return {
        "note": "Two preselected synthetic matched witnesses; does not estimate a population frequency.",
        "decision_tick": DECISION_TICK,
        "legacy_terminal_sensitive": binary_certificate(-3, 35),
        "new_terminal_robust": binary_certificate(-113, 31),
        "interpretation": {
            "prefix_or_counts": "same in paired worlds; cannot separate their future gaps",
            "live_gap_tick_84": "optimistic zero-latency case only; not a feasible delayed camera decision",
            "future_schedule_label": "oracle, forbidden as an observed live feature",
            "forecast": "allowed only if generated before commitment; conditional error must be assessed",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(report(), indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
