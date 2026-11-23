import json
from collections import defaultdict
from pathlib import Path

rows = json.loads(Path(__file__).with_name("P69_RESULT.json").read_text())
by_tape = defaultdict(list)
for row in rows:
    by_tape[row["tape"]].append(row["delta"])
if len(by_tape) != 32 or any(len(ds) != 16 for ds in by_tape.values()):
    raise ValueError("Incomplete factorial block")
summary = {}
for label, subset in [("all", rows)] + [(f"{key}={value}", [r for r in rows if r[key] == value])
                                        for key in ("family","blocked","offset","headway","pocket")
                                        for value in sorted({r[key] for r in rows})]:
    ds = [r["delta"] for r in subset]
    summary[label] = dict(improved=sum(d < 0 for d in ds), worse=sum(d > 0 for d in ds),
                          tie=ds.count(0), mean=sum(ds)/len(ds))
summary["opposite_within_tape"] = sum(min(ds) < 0 < max(ds) for ds in by_tape.values())
print(json.dumps(summary, indent=2))
