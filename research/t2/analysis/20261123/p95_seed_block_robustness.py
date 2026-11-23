"""P95: seed-block robustness of P87 onset-by-left-share interaction.
Read P87_RESULT.json; never treat two onsets or two clock families as
independent random samples. Run: python p95_seed_block_robustness.py.
"""
import json
from collections import defaultdict, Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

def experiment():
    data = json.loads((HERE / "P87_RESULT.json").read_text())["rows"]
    panel = defaultdict(dict)
    for r in data:
        key = (r["seed"], r["share"], r["clock"])
        assert r["onset"] not in panel[key], key
        panel[key][r["onset"]] = r["delta"]
    assert len(data) == 192 and len(panel) == 96
    by_share = {}
    records = []
    for (seed, share, clock), p in sorted(panel.items()):
        assert set(p) == {"green", "red"}
        diff = p["red"]["cost"] - p["green"]["cost"]
        records.append(dict(seed=seed, share=share, clock=clock,
                            cost_interaction=diff,
                            green_cost=p["green"]["cost"], red_cost=p["red"]["cost"],
                            green_denied=p["green"]["denied"], red_denied=p["red"]["denied"]))
    for share in (.25, .5, .75):
        cohort = [r for r in records if r["share"] == share]
        seeds = sorted({r["seed"] for r in cohort})
        assert len(cohort) == 32 and len(seeds) == 16
        total = sum(r["cost_interaction"] for r in cohort)
        loo = []
        for seed in seeds:
            kept = [r for r in cohort if r["seed"] != seed]
            assert len(kept) == 30
            loo.append(dict(held_out_seed=seed,
                            interaction_mean=sum(r["cost_interaction"] for r in kept)/30,
                            positives=sum(r["cost_interaction"] > 0 for r in kept)))
        by_share[str(share)] = {
            "n": len(cohort), "seed_blocks": len(seeds),
            "interaction_sum": total, "interaction_mean": total / len(cohort),
            "positive": sum(r["cost_interaction"] > 0 for r in cohort),
            "negative": sum(r["cost_interaction"] < 0 for r in cohort),
            "zero": sum(r["cost_interaction"] == 0 for r in cohort),
            "min": min(r["cost_interaction"] for r in cohort),
            "max": max(r["cost_interaction"] for r in cohort),
            "leave_one_seed_out_min_mean": min(r["interaction_mean"] for r in loo),
            "leave_one_seed_out_max_mean": max(r["interaction_mean"] for r in loo),
            "leave_one_seed_out_same_mean_sign": len(set((v["interaction_mean"]>0)-(v["interaction_mean"]<0) for v in loo)) == 1,
            "leave_one_seed_out": loo,
        }
    assert by_share["0.25"]["negative"] == 29
    assert by_share["0.5"]["positive"] == 29
    assert by_share["0.75"]["positive"] == 32
    assert sum(by_share[k]["interaction_sum"] for k in by_share) == 131518
    return {"source":"P87_RESULT.json","evidence_grade":"source-cohort descriptive sensitivity, not out-of-sample inference",
            "design":"paired onset within 96 tapes, leave one of 16 seed blocks out of each left-turn share",
            "by_share":by_share,"records":records}

if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
