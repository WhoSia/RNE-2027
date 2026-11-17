"""Evaluate fixed startup baselines with interval-valued crossing times."""
import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import median

from field_replay import EVAL, TRAIN

TARGETS = {("1100",9),("1215",4),("1230",9),("1445",2)}


def through_rows(blocks):
    return [r|{"block":b["block"]} for b in blocks for r in b["rows"]
            if r["movement"]=="through" and r["crossing_s_bounds"] is not None]


def loss(prediction,bounds):
    lower,upper = bounds
    return max(0,lower-prediction,prediction-upper),max(abs(prediction-lower),abs(prediction-upper))


def paired_difference(a,b,bounds):
    lo,hi = bounds
    points = [lo,hi] + [p for p in (a,b) if lo <= p <= hi]
    values = [abs(a-t)-abs(b-t) for t in points]
    return min(values),max(values)


def evaluate(data):
    rows = through_rows(data)
    training = [r for r in rows if r["block"] in TRAIN]
    evaluation = [r for r in rows if r["block"] in EVAL]
    by_rank = defaultdict(list)
    by_lane_rank = defaultdict(list)
    for r in training:
        middle = sum(r["crossing_s_bounds"])/2
        by_rank[r["rank"]].append(middle)
        by_lane_rank[r["lane"],r["rank"]].append(middle)
    overall = median(sum(r["crossing_s_bounds"])/2 for r in training)
    results = []
    for row in evaluation:
        rank = median(by_rank.get(row["rank"],[overall]))
        local = by_lane_rank.get((row["lane"],row["rank"]),())
        predictions = {"constant":overall,"rank":rank,
                       "lane_rank":median(local) if len(local)>=3 else rank}
        results.append(row|{"loss_bounds_s":{k:loss(v,row["crossing_s_bounds"])
                                               for k,v in predictions.items()},
                            "paired_rank_minus_constant_s":paired_difference(
                                rank,overall,row["crossing_s_bounds"]),
                            "paired_lane_rank_minus_rank_s":paired_difference(
                                predictions["lane_rank"],rank,row["crossing_s_bounds"])})
    targets = []
    for r in rows:
        if (r["block"],r["interval"]) not in TARGETS:
            continue
        references = [q for q in rows if q["block"]==r["block"] and q["interval"]!=r["interval"]
                      and (q["lane"],q["rank"])==(r["lane"],r["rank"])]
        lo,hi = r["crossing_s_bounds"]
        # Compare entire intervals, allowing either green onset within its bracket.
        targets.append(r|{"reference_n":len(references),
                          "definitely_later_than_n":sum(q["crossing_s_bounds"][1]<lo for q in references),
                          "definitely_earlier_than_n":sum(q["crossing_s_bounds"][0]>hi for q in references)})
    return {"training_n":len(training),"evaluation_n":len(evaluation),"targets":targets,"evaluation":results}


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("cohort",type=Path)
    p.add_argument("output",type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(evaluate(json.loads(a.cohort.read_text())),indent=2)+"\n")
