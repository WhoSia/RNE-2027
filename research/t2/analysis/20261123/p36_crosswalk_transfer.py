"""Audit transfer of the documented east-approach crosswalk to P34/P35."""
import argparse
from collections import Counter
import json
from pathlib import Path

from p35_observation_timing import load_p34, verify_bytes

P35_SHA = "2a6dbc99b6643879b88dd3c9a18f756acd31bf6a95a358c5c11a0f9bf659d58f"
EAST_GROUP_BY_LANE = {-4: 3, -3: 3, -2: 4}


def key(record, fields):
    return tuple(record[field] for field in fields)


def audit(crossings, timing):
    geometry_fields = (
        "id", "source_arm", "crossing_time_utc", "bracket_start_utc", "bracket_end_utc",
    )
    timing_fields = (
        "object_id", "source_arm", "crossing_estimate", "bracket_start", "bracket_end",
    )
    by_event = {key(event, timing_fields): event for event in timing}
    geometry_keys = {key(event, geometry_fields) for event in crossings}
    if (len(geometry_keys) != len(crossings) or len(by_event) != len(timing)
            or geometry_keys != by_event.keys()):
        raise ValueError("P34 geometry and P35 timing must match one to one")

    counts = Counter()
    for crossing in crossings:
        event = by_event[key(crossing, geometry_fields)]
        group = None
        if crossing["road_id"] == "100000" and crossing["source_arm"] == "East":
            group = EAST_GROUP_BY_LANE.get(crossing["map_lane_id"])
        if group is None:
            counts["unmapped"] += 1
            continue

        counts[f"group_{group}_candidates"] += 1
        counts["prior_sample_age_le_1s"] += (
            event["causal_sample_age_at_bracket_end_s"] <= 1.0
        )
        counts["candidate_group_discordant"] += (
            group in event["sampled_state_discordant_head_ids"]
        )
        counts["any_group_discordant"] += bool(event["sampled_state_discordant_head_ids"])

    return dict(counts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("p34_zip", type=Path)
    parser.add_argument("p35_json", type=Path)
    args = parser.parse_args()
    geometry = load_p34(args.p34_zip)["crossings"]
    timing = json.loads(verify_bytes(args.p35_json, P35_SHA))["event_records"]
    print(json.dumps(audit(geometry, timing), indent=2, sort_keys=True))
