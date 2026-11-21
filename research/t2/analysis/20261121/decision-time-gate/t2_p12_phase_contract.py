"""P12: illustrative stage-contract checker, NOT a controller or legal safety verifier.

The integer 'ticks' are arbitrary model units. No deployment/interface code exists.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


def nonnegative_int(value: object, name: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer, not bool")
    return value


@dataclass(frozen=True)
class Stage:
    movement: str
    green: int
    yellow: int
    all_red: int
    pedestrian_clearance: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.movement, str) or not self.movement.strip():
            raise ValueError("movement must be a nonempty string")
        for attr in ("green", "yellow", "all_red", "pedestrian_clearance"):
            nonnegative_int(getattr(self, attr), attr)


@dataclass(frozen=True)
class Contract:
    min_green: dict[str, int]
    min_yellow: int
    min_all_red: int
    permitted_movements: frozenset[str]
    cyclic: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.cyclic, bool):
            raise ValueError("cyclic must be bool")
        if not isinstance(self.min_green, dict) or not isinstance(self.permitted_movements, frozenset):
            raise ValueError("incorrect contract structures")
        if not self.permitted_movements or any(
            not isinstance(m, str) or not m.strip() for m in self.permitted_movements
        ):
            raise ValueError("permitted movement names invalid")
        if set(self.min_green) != set(self.permitted_movements):
            raise ValueError("minimum green must be specified for each permitted movement")
        for movement, minimum in self.min_green.items():
            nonnegative_int(minimum, f"min_green[{movement}]")
        nonnegative_int(self.min_yellow, "min_yellow")
        nonnegative_int(self.min_all_red, "min_all_red")


def check_plan(stages: Iterable[Stage], contract: Contract) -> tuple[str, ...]:
    """Return *model-contract* reasons, never a road-safety certification.

    Yellow and all-red are explicit fields, not a generic '-' placeholder.
    A stage's clearance must be sufficient when it is followed by a
    DIFFERENT movement; when cyclic, the last-to-first edge is checked.
    """
    stages = tuple(stages)
    if not stages:
        return ("empty_plan",)
    if any(not isinstance(s, Stage) for s in stages):
        raise TypeError("all elements must be Stage instances")
    violations: list[str] = []
    for i, stage in enumerate(stages):
        if stage.movement not in contract.permitted_movements:
            violations.append(f"stage_{i}:unknown_movement")
            continue
        if stage.green < contract.min_green[stage.movement]:
            violations.append(f"stage_{i}:green_below_contract_minimum")
        if stage.pedestrian_clearance > stage.green + stage.yellow:
            violations.append(f"stage_{i}:pedestrian_clearance_exceeds_green_plus_yellow")
        if stage.green == 0 and stage.pedestrian_clearance:
            violations.append(f"stage_{i}:pedestrian_clearance_without_green")
        next_index = (i + 1) % len(stages)
        has_successor = i + 1 < len(stages) or contract.cyclic
        if has_successor and stage.movement != stages[next_index].movement:
            if stage.yellow < contract.min_yellow:
                violations.append(f"stage_{i}:missing_yellow_change")
            if stage.all_red < contract.min_all_red:
                violations.append(f"stage_{i}:missing_red_clearance")
    return tuple(violations)


def duration_ticks(stages: Iterable[Stage]) -> int:
    """Sequential illustrative duration, not runtime engine phase scheduling."""
    stages = tuple(stages)
    if any(not isinstance(s, Stage) for s in stages):
        raise TypeError("all elements must be Stage instances")
    return sum(s.green + s.yellow + s.all_red for s in stages)


def illustrative_four_tick_case() -> dict:
    """Construct an intentionally incomplete virtual plan to expose the gate."""
    contract = Contract(
        min_green={"through": 6, "left": 6},
        min_yellow=2,
        min_all_red=1,
        permitted_movements=frozenset({"through", "left"}),
        cyclic=False,
    )
    stages = (
        Stage("through", 8, 0, 0),
        Stage("left", 4, 0, 0),
    )
    return {
        "contract": contract,
        "stages": stages,
        "duration_ticks": duration_ticks(stages),
        "violations": check_plan(stages, contract),
        "status": "ILLUSTRATIVE_SIMULATION_CONTRACT_NOT_REGULATORY",
    }


if __name__ == "__main__":
    print(illustrative_four_tick_case())
