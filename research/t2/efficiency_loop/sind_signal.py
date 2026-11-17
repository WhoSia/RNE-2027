"""Normalize the SinD public Tianjin and Changchun signal samples."""
import argparse
import csv
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from statistics import median

TIANJIN_SHA = "a28abf25725df5ca015840824db02efd03135e2fb5e0c153a6b6506b039d8c7a"
GREEN = 1
YELLOW = 3
DATASETS = {
    "tianjin": (TIANJIN_SHA, tuple(f"Traffic light {i}" for i in range(1,9))),
    "changchun": ("ebede8df767f5c0f77f33a2df14c880f6fa734925d56474dc3cc6375af401f49",
                 ("Vehicle Traffic light 1","Vehicle Traffic light 2")),
}


def audit(path, site):
    expected, heads = DATASETS[site]
    data = path.read_bytes()
    digest = sha256(data).hexdigest()
    if digest != expected:
        raise ValueError("source does not match the published Git LFS object")
    rows = list(csv.DictReader(data.decode("utf-8-sig").splitlines()))
    frames = [int(r["RawFrameID"]) for r in rows]
    times = [float(r["timestamp(ms)"]) / 1000 for r in rows]
    states = [tuple(int(r[h]) for h in heads) for r in rows]
    if (any(y <= x for x,y in zip(frames,frames[1:]))
            or any(y <= x for x,y in zip(times,times[1:]))
            or any(set(s) - {0,GREEN,YELLOW} for s in states)):
        raise ValueError("unknown state or unordered transitions")
    pattern = Counter(states)
    all_red = [b-a for a,b,s in zip(times,times[1:],states) if not any(s)]
    head_stats = {}
    for i,head in enumerate(heads):
        starts = [times[k] for k in range(1,len(states))
                  if states[k][i] == GREEN and states[k-1][i] != GREEN]
        cycles = [b-a for a,b in zip(starts,starts[1:])]
        ends = [times[k] for k in range(1,len(states))
                if states[k][i] != GREEN and states[k-1][i] == GREEN]
        green = [min(t for t in ends if t > start)-start for start in starts if any(t>start for t in ends)]
        head_stats[head] = {"complete_onset_pairs":len(cycles),"cycle_s_range":[min(cycles),max(cycles)],
                            "median_cycle_s":median(cycles),"median_complete_green_s":median(green)}
    return {"source_sha256":digest,"events":len(rows),"window_s":[times[0],times[-1]],
            "states":len(pattern),"all_red_s_range":[min(all_red),max(all_red)] if all_red else None,
            "head_statistics":head_stats}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input",type=Path)
    p.add_argument("--site",choices=DATASETS,default="tianjin")
    p.add_argument("output",type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(audit(a.input,a.site),indent=2)+"\n")
