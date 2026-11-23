"""Count paired factor contrasts and preserve their denominators."""
import json
from collections import defaultdict
from pathlib import Path

rows = json.loads(Path(__file__).with_name("P68_RESULT.json").read_text())
factors = ("pocket", "share", "changes", "headway")
groups = defaultdict(list)
for row in rows:
    groups[row["tape"]].append(row["delta"])
if len(groups) != 32 or any(len(ds) != 36 for ds in groups.values()):
    raise ValueError("Incomplete cohort")
summary = dict(rows=len(rows), improved=sum(r["delta"] < 0 for r in rows),
               worse=sum(r["delta"] > 0 for r in rows),
               opposite_within_tape=sum(min(ds) < 0 < max(ds) for ds in groups.values()))
for factor in factors:
    paired = defaultdict(dict)
    for r in rows:
        key = (r["tape"], *(r[k] for k in factors if k != factor))
        paired[key][r[factor]] = r["delta"]
    contrasts = [(g[min(g)], g[max(g)]) for g in paired.values()]
    summary[factor] = dict(pairs=len(contrasts), changed=sum(a != b for a,b in contrasts),
                           opposite=sum(a*b < 0 for a,b in contrasts))
print(json.dumps(summary, indent=2))
