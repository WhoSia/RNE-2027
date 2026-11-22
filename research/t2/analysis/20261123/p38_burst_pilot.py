"""Exploratory P31 repeat under fresh seeds and compressed platoons."""
from unittest.mock import patch
import json

import p31_two_arrival_families as p31

SEEDS = ((128, 1650, .50), (129, 1650, .50), (130, 1800, .45), (131, 1800, .45))
PLATOON_SPAN = 5


if __name__ == "__main__":
    with patch.multiple(p31, SEED_DEMAND=SEEDS, PLATOON_SPAN=PLATOON_SPAN):
        run = p31.experiment()
    print(json.dumps({
        "status": "exploratory synthetic",
        "platoon_span_s": PLATOON_SPAN,
        **{key: run[key] for key in ("seeds", "worlds", "unique_arrival_tapes", "by_family")},
    }, indent=2, sort_keys=True))
