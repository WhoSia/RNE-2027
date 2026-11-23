"""P91: falsify a single 'receiver-full' explanation using independent P87 metrics.

Run: python p91_multi_metric_falsification.py > P91_RESULT.json
Consumes archived P87 only; it does not reconstruct individual vehicle histories.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent

def summarize(rows):
    assert len(rows) == 192
    by_onset = {}
    for onset in ("green", "red"):
        subset = [r for r in rows if r["onset"] == onset]
        assert len(subset) == 96
        cohorts = {}
        for name, chosen in (
            ("paradox", [r for r in subset if r["delta"]["denied"] < 0 < r["delta"]["cost"]]),
            ("both_down", [r for r in subset if r["delta"]["denied"] < 0 and r["delta"]["cost"] < 0]),
        ):
            d = [r["delta"] for r in chosen]
            signs = Counter(("lower" if x["full_red"] < 0 else
                             "higher" if x["full_red"] > 0 else "equal") for x in d)
            cohorts[name] = dict(n=len(chosen),
                cost_sum=sum(x["cost"] for x in d),
                denied_sum=sum(x["denied"] for x in d),
                full_red_sum=sum(x["full_red"] for x in d),
                full_red_signs={k: signs[k] for k in ("lower", "equal", "higher")},
                clock_counts={family:sum(r["clock"] == family for r in chosen)
                              for family in ("uniform", "platoon4")})
        by_onset[onset] = cohorts
    assert by_onset["green"]["paradox"]["n"] == 12
    assert by_onset["red"]["paradox"]["n"] == 43
    assert sum(by_onset[o]["paradox"]["full_red_signs"]["lower"]
               for o in ("green","red")) == 51
    return dict(evidence_grade="independent archived JSON reaggregation; no new simulation",
                interpretation="51/55 paradox pairs have both denial and full-red seconds lower, yet total vehicle-seconds higher; locate added occupancy via P88",
                by_onset=by_onset)

if __name__ == "__main__":
    print(json.dumps(summarize(json.loads((HERE/"P87_RESULT.json").read_text())["rows"]), indent=2))
