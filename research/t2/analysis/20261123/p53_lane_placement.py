"""Perturb the T2 through-vehicle lane allocation for the closed receiver."""
import json

from p39_engine_bridge import t2_case
from p52_stage_deltas import stages


def experiment():
    rows = []
    for share in (0., .5, 1.):
        lag, lead = (stages(t2_case(order, 10, 2, receiver_mode="cells",
                                    receiver_closures=((0, 50),), movement_details=True,
                                    through_share=share)) for order in (False, True))
        rows.append({"through_B_share": share, "contrast": {
            move: [b - a for a, b in zip(lag[move], lead[move], strict=True)] for move in lag
        }})
    return rows


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
