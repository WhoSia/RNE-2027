"""Repeat the P66 block with the SUMO approach length set to T2's 140 m."""
import json
from pathlib import Path
from unittest.mock import patch

import sumo_phase_pair as network
from p66_transfer import experiment


def evaluate():
    baseline = json.loads(Path(__file__).with_name("P66_RESULT.json").read_text())
    with patch.object(network, "APPROACH_M", 140):
        updated = experiment()
    for old, new in zip(baseline["rows"], updated["rows"], strict=True):
        if (old["tape"], old["delta60"]) != (new["tape"], new["delta60"]):
            raise ValueError("Mismatched paired condition")
        new["sumo_delta_100m"] = old["sumo_delta"]
    return updated


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
