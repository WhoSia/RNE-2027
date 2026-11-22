"""Compare the movement contrast with and without the SUMO amber treatment."""
import json

from p50_movement_bridge import experiment


if __name__ == "__main__":
    print(json.dumps(experiment(yellow=False), indent=2, sort_keys=True))
