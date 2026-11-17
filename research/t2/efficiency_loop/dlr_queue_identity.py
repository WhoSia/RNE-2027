"""Follow camera track identities around the known DLR signal transition."""
import argparse
import csv
from hashlib import file_digest
import json
from math import ceil, floor
from pathlib import Path

import pandas as pd

from dlr_green_audit import audit
from dlr_residual_queue import screen
from field_replay import EVAL, TRAIN

STOP_M = 155.566906348012
THROUGH_LANES = (-3, -4)


def queue_ids(samples, speed, gap):
    detected = {}
    stopped = samples[samples.velocity_magnitude <= speed]
    for (tick,lane), group in stopped.groupby(["tick","lane"]):
        rear = STOP_M
        members = []
        for v in group.sort_values("s",ascending=False,kind="stable").itertuples():
            front = v.s + v.dimension_length/2
            if rear - front > gap:
                break
            members.append(int(v.id))
            rear = v.s - v.dimension_length/2
        if members:
            detected[int(tick),int(lane)] = tuple(members)
    return detected


def compare_counts(ids, path):
    with path.open(newline="") as stream:
        reference = {(int(r["tick"]),int(r["lane"])):int(r["count"])
                     for r in csv.DictReader(stream) if int(r["lane"]) in THROUGH_LANES}
    actual = {key:len(v) for key,v in ids.items()}
    if actual != reference:
        raise ValueError("baseline queue reconstruction differs from saved counts")
    return len(reference)


def window_ids(ids, ticks):
    return set().union(*(ids.get((t,lane),()) for t in ticks for lane in THROUGH_LANES))


def presence_label(first, b0, b1):
    if first <= b0:
        return "observed_by_last_green"
    if first >= b1:
        return "first_observed_after_green"
    return "first_observed_in_transition_bracket"


def analyze(root, block):
    offset = (int(block[:2])-12)*3600 + int(block[2:])*60
    path = root/"week1"/"wide"/block
    cache = path/"east_tracks_working.pkl"
    # This is the project-generated cache from the previous DLR preprocessing.
    data = pd.read_pickle(cache)
    data = data[~data.interpolated].copy()
    spans = data.groupby("id").time.agg(["min","max"])
    data["tick"] = (data.time*2).round().astype(int)
    data["error"] = (data.time-data.tick/2).abs()
    samples = data[data.error <= .026]
    samples = samples.loc[samples.groupby(["id","tick"]).error.idxmin()]
    samples = samples[samples.lane.isin(THROUGH_LANES)]
    movement = data.dropna(subset=["movement"]).groupby("id").movement.first().to_dict()
    baseline = queue_ids(samples,1,8)
    with (path/"daylight_crossings.csv").open(newline="") as stream:
        crossings = {int(r["id"]):float(r["stop"]) for r in csv.DictReader(stream)}
    variants = {(speed,gap):queue_ids(samples,speed,gap)
                for speed,gap in ((.5,8),(2,8),(1,6),(1,10),(2,10))}
    matched = compare_counts(baseline,path/"daylight_queues_1ms.csv")
    screening = screen(root,block)
    greens = {g["interval"]:g for g in audit(root,block)["cycles"]}
    cases = []
    for row in screening["rows"]:
        g = greens[row["interval"]]
        b0,b1 = (v+offset for v in g["off_bracket_s"])
        a1 = g["on_bracket_s"][1]+offset
        green = range(max(ceil(2*a1),floor(2*b0)-9),floor(2*b0)+1)
        red0 = ceil(2*(row["red_first_s"]+offset))
        red = range(red0,red0+10)
        before,after = window_ids(baseline,green),window_ids(baseline,red)
        assert bool(before)==bool(row["green_tail_detected"])
        assert bool(after)==bool(row["early_red_detected"])
        if before or not after:
            continue
        people = []
        for ident in sorted(after):
            first = spans.loc[ident,"min"]
            track = data[(data.id==ident)&data.time.between(b0-5,b1)]
            pre = track[track.time <= b0]
            closest = pre.sort_values("time").tail(1)
            stop = crossings.get(ident)
            red_ticks = [t for t in red if any(ident in baseline.get((t,lane),()) for lane in THROUGH_LANES)]
            people.append({
                           "first_queue_after_first_red_s":round(red_ticks[0]/2-(row["red_first_s"]+offset),3),
                           "last_green_front_distance_m":round(STOP_M-float(
                               (closest.s+closest.dimension_length/2).iloc[0]),2) if len(closest) else None,
                           "last_green_sample_age_s":round(b0-float(closest.time.iloc[0]),3) if len(closest) else None,
                           "stop_crossing_after_last_green_s":round(stop-b0,3) if stop is not None else None,"first_observation_relative_last_green_s":round(first-b0,3),
                           "presence":presence_label(first,b0,b1),
                           "movement":movement.get(ident,"unclassified"),
                           "previous_visible_samples":len(track),
                           "previous_through_lane_samples":int(track.lane.isin(THROUGH_LANES).sum()),
                           "previous_min_speed_m_s":round(track.velocity_magnitude.min(),3) if len(track) else None})
        cases.append({"interval":row["interval"],"vehicles":people,
                      "sensitivity":[{"speed_m_s":v,"gap_m":gap,
                                      "same_track_both_windows":len(window_ids(ids,green) & after & window_ids(ids,red)),
                                      "original_tracks_retained_in_red":len(after & window_ids(ids,red))}
                                     for (v,gap),ids in variants.items()]})
    with cache.open("rb") as f:
        cache_sha = file_digest(f,"sha256").hexdigest()
    return {"block":block,"matched_baseline_lane_slots":matched,"cache_sha256":cache_sha,
            "inputs_sha256":screening["input_sha256"],"cases":cases}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("root",type=Path)
    p.add_argument("output",type=Path)
    args=p.parse_args()
    args.output.write_text(json.dumps([analyze(args.root,b) for b in TRAIN+EVAL],indent=2)+"\n")
