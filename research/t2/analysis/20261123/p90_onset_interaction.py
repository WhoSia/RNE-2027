"""P90 matched-onset falsification audit of archived P87 pairs.

No simulator dependency; rerun: python p90_onset_interaction.py > P90_RESULT.json
This analyzes synthetic tapes only and makes no independent-observation claim.
"""
from collections import Counter, defaultdict
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent

def experiment():
    rows = json.loads((HERE / "P87_RESULT.json").read_text())["rows"]
    pairs = defaultdict(dict)
    for r in rows:
        key = (r["seed"], r["share"], r["clock"])
        assert r["onset"] not in pairs[key], key
        pairs[key][r["onset"]] = r["delta"]
    assert len(rows) == 192 and len(pairs) == 96
    table = Counter()
    signs = Counter()
    by_share = defaultdict(Counter)
    by_clock = defaultdict(Counter)
    records = []
    for (seed, share, clock), p in sorted(pairs.items()):
        assert set(p) == {"green", "red"}
        g, r = p["green"], p["red"]
        gp = g["denied"] < 0 and g["cost"] > 0
        rp = r["denied"] < 0 and r["cost"] > 0
        gup = g["cost"] > 0
        rup = r["cost"] > 0
        table[("Y" if gp else "N") + ("Y" if rp else "N")] += 1
        signs[("Y" if gup else "N") + ("Y" if rup else "N")] += 1
        for c in (by_share[share], by_clock[clock]):
            c["n"] += 1
            c["green_paradox"] += gp
            c["red_paradox"] += rp
        records.append(dict(seed=seed, share=share, clock=clock,
                            green=g, red=r, green_paradox=gp, red_paradox=rp,
                            interaction_cost=(r["cost"] - g["cost"]),
                            interaction_denied=(r["denied"] - g["denied"])))
    assert dict(table) == {"NN": 41, "NY": 43, "YN": 12}
    assert sum(x["interaction_cost"] for x in records) == 131518
    assert by_share[.25]["green_paradox"] == 11 and by_share[.25]["red_paradox"] == 0
    assert by_share[.5]["green_paradox"] == 1 and by_share[.5]["red_paradox"] == 11
    assert by_share[.75]["green_paradox"] == 0 and by_share[.75]["red_paradox"] == 32
    return dict(source="P87_RESULT.json",analysis="paired per (seed, share, clock)",
                evidence_grade="descriptive exact reaggregation, not population inference",
                table={k:table[k] for k in ("NN","NY","YN","YY")},
                cost_sign_table={k:signs[k] for k in ("NN","NY","YN","YY")},
                by_share={str(k):dict(v) for k,v in sorted(by_share.items())},
                by_clock={k:dict(v) for k,v in sorted(by_clock.items())},
                paired_cost_interaction_sum=sum(x["interaction_cost"] for x in records),
                paired_cost_interaction_mean=sum(x["interaction_cost"] for x in records)/96,
                records=records)

if __name__ == "__main__":
    print(json.dumps(experiment(), ensure_ascii=False, indent=2))
