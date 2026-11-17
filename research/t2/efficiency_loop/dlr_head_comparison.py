"""Join candidate signal heads and stopped queues around paired starts."""
import argparse
import csv
from datetime import datetime
import json
from pathlib import Path

from dlr_green_audit import audit
from dlr_green_service import digest
from field_replay import ORIGIN

HEADS = (3,4,8,9)


def timeline(root, pairs):
    block = "1230"
    offset = 1800
    raw = root/"day"/f"day{block}_signals.csv"
    queue = root/"week1"/"wide"/block/"daylight_queues_1ms.csv"
    with raw.open(newline="") as stream:
        samples = [(int(r["id"]), (datetime.fromisoformat(r["timestamp"])-ORIGIN).total_seconds(),
                    int(r["state"])) for r in csv.DictReader(stream) if int(r["id"]) in HEADS]
    with queue.open(newline="") as stream:
        queues = [(int(r["tick"])/2,int(r["lane"]),int(r["count"])) for r in csv.DictReader(stream)]
    green = {c["interval"]:c for c in audit(root,block)["cycles"]}
    out = []
    for r in pairs:
        if r["block"]!=block:
            continue
        t = offset+green[r["interval"]]["on_bracket_s"][1]
        states = {str(h):[[round(s-t,3),state] for head,s,state in samples
                          if head==h and t-2<=s<=t+6] for h in HEADS}
        waiting = [[round(s-t,3),lane,count] for s,lane,count in queues if t-2<=s<=t+6]
        out.append(r|{"candidate_head_states":states,"detected_queues":waiting})
    return {"input_sha256":{str(p.relative_to(root)):digest(p) for p in (raw,queue)},"cases":out}


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("root",type=Path)
    p.add_argument("pairs",type=Path)
    p.add_argument("output",type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(timeline(a.root,json.loads(a.pairs.read_text())["pairs"]),indent=2)+"\n")
