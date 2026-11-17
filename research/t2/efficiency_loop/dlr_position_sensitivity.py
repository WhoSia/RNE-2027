"""Check lead-only performance and training-block dependence."""
import argparse
import json
from pathlib import Path

from dlr_startup_position import evaluate
from field_replay import TRAIN


def sensitivity(data):
    return {
        "lead_only": evaluate(data, rank_filter=1),
        "omit_training_block": {block: evaluate(data, omit_training_block=block)
                                for block in TRAIN},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cohort", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report = sensitivity(json.loads(args.cohort.read_text()))
    args.output.write_text(json.dumps(report, indent=2) + "\n")
