"""Check whether the through-stage reversal survives downstream signal offsets."""
from itertools import product
import json

from p39_engine_bridge import t2_case
from p52_stage_deltas import stages


def experiment():
    rows = []
    for offset, share in product((0, 10, 20, 30, 40, 50), (0., 1.)):
        lag, lead = (
            stages(t2_case(order, 10, 2, receiver_mode="cells",
                           receiver_closures=((0, 50),), movement_details=True,
                           through_share=share, receiver_offset=offset))
            for order in (False, True)
        )
        rows.append({"offset_s": offset, "through_B_share": share,
                     "lead_minus_lag": {name: [b - a for a, b in zip(lag[name], lead[name], strict=True)]
                                        for name in lag}})
    return rows


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
