"""Compare independent review exports without reading the automatic labels."""
import argparse
import csv
import json
from pathlib import Path

from dlr_path_screen import sha

FIELDS = {
    "leader_movement": {"left","through","other","unknown"},
    "follower_movement": {"left","through","other","unknown"},
    "cannot_advance": {"yes","no","unknown"},
    "lead_or_lane_change": {"yes","no","unknown"},
    "downstream_space": {"available","blocked","unknown"},
    "signal_for_follower": {"green","non_green","unknown"},
    "tracking_gap": {"yes","no","unknown"},
    "judgment": {"possible_left_block","other_observed","unknown"},
}


def validate(review, scope):
    if not isinstance(review["reviewer"],str) or not review["reviewer"].strip() or not review["cases"]:
        raise ValueError("A reviewer code and at least one case are required")
    for case,row in review["cases"].items():
        if case not in scope or set(row) != FIELDS.keys() | {"evidence"}:
            raise ValueError(f"Unrecognized review case or fields: {case}")
        if any(row[key] not in allowed for key,allowed in FIELDS.items()):
            raise ValueError(f"Unexpected response in {case}")
        if not isinstance(row["evidence"],str) or not row["evidence"].strip():
            raise ValueError(f"{case} lacks evidence notes")


def compare(a, b, expected):
    validate(a,expected)
    validate(b,expected)
    if a["reviewer"].strip() == b["reviewer"].strip():
        raise ValueError("Review exports must have different reviewer codes")
    aa,bb = a["cases"],b["cases"]
    common = sorted(aa.keys() & bb.keys())
    disputes = {case: {key:[aa[case][key],bb[case][key]] for key in FIELDS
                       if aa[case][key] != bb[case][key]} for case in common}
    fields = {}
    for key in FIELDS:
        determinate = [case for case in common if "unknown" not in (aa[case][key],bb[case][key])]
        fields[key] = {"joint_cases":len(common),
                       "agree_including_unknown":sum(key not in disputes[c] for c in common),
                       "joint_determinate":len(determinate),
                       "agree_given_joint_determinate":sum(key not in disputes[c] for c in determinate)}
    return {"expected_cases":len(expected),"joint_cases":common,
            "missing_by_reviewer":{a["reviewer"]:sorted(expected-aa.keys()),b["reviewer"]:sorted(expected-bb.keys())},
            "fields":fields,"disputes":{c:{"fields":diff,"evidence":[aa[c]["evidence"],bb[c]["evidence"]]}
                                         for c,diff in disputes.items() if diff}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name in ("sheet","review_a","review_b","output"):
        parser.add_argument(name,type=Path)
    args = parser.parse_args()
    with args.sheet.open(newline="",encoding="utf-8") as stream:
        scope = {row["case"] for row in csv.DictReader(stream)}
    a,b = (json.loads(path.read_text()) for path in (args.review_a,args.review_b))
    digest = sha(args.sheet)
    if any(r.get("review_sheet_sha256") != digest for r in (a,b)):
        raise ValueError("Both reviews must refer to the supplied review sheet")
    args.output.write_text(json.dumps(compare(a,b,scope),indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
