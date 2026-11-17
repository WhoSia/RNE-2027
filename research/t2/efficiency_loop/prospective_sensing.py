"""Compare observations when future arrival counts are forecast envelopes."""
import argparse
from itertools import product
from functools import lru_cache
import json
from pathlib import Path

from d51_phase_order import Params
from sensing import MOVEMENT, PRESENCE, compare
from timing_bounds import exact

WIDTH = 3
PROFILE = ((1,1),(2,0),(0,2),(1,0),(0,1))
QUEUE_STARTS = (("",0,0),("",0,1))


def information_at_decision(realized, width, decision, cap):
    """Expose only closed bins; apply a joint count ceiling to all other bins."""
    if width < 1 or not 0 <= decision <= width*len(realized) or not 0 <= cap <= width:
        raise ValueError("invalid decision, bin width, or future cap")
    closed = decision // width
    lower = tuple(realized[:closed]) + ((0,0),)*(len(realized)-closed)
    upper = tuple(realized[:closed]) + ((cap,cap),)*(len(realized)-closed)
    ceilings = tuple(map(sum,realized[:closed])) + (cap,)*(len(realized)-closed)
    return lower, upper, ceilings


def decision_record(bound):
    lead, lag = max(0,bound.high),max(0,-bound.low)
    return {"delta":[bound.low,bound.high],"possible_paths":bound.paths,
            "worst_regret":bound.regret,
            "minimax_choice":"either" if lead == lag else "lead" if lead < lag else "lag",
            "low_witness":{"arrivals":bound.low_path,"initial":bound.low_start},
            "high_witness":{"arrivals":bound.high_path,"initial":bound.high_start}}


def pocket_partition(width, lower, config, options, base, groups):
    arms = {}
    for label, states in groups:
        b = exact(width,lower,config,**options,decision_left=states)
        if b is not None:
            arms[label] = decision_record(b)
    if sum(row["possible_paths"] for row in arms.values()) != base.paths:
        raise RuntimeError("Pocket occupancy observations did not partition the same worlds")
    return {"worst_regret":max(row["worst_regret"] for row in arms.values()),"branches":arms}


def live_evaluation(lower, upper, ceilings, config, decision, width, initial):
    forecasts = {"bin_upper":upper,"bin_total_upper":ceilings}
    options = forecasts | {"initial":initial,"decision_tick":decision}
    base = exact(width,lower,config,**options)
    instruments = {}
    for name,sensor in (("presence",PRESENCE),("movement",MOVEMENT)):
        result = compare(width,lower,config,decision,sensor,1,initial,**forecasts)
        regret, (tick,) = result["fixed"]
        branches = {}
        for labels in sensor:
            b = exact(width,lower,config,observed={tick:labels},**options)
            if b is not None:
                branches["/".join(label or "empty" for label in labels)] = decision_record(b)
        if sum(r["possible_paths"] for r in branches.values()) != base.paths:
            raise RuntimeError("Past observation did not partition the same worlds")
        instruments[name] = {"worst_regret":regret,"observation_tick":tick,"branches":branches}
    instruments["pocket_fullness"] = pocket_partition(width,lower,config,options,base,(
        ("not_full",range(config.left_capacity)),("full",(config.left_capacity,))))
    instruments["pocket_count"] = pocket_partition(width,lower,config,options,base,(
        (str(count),(count,)) for count in range(config.left_capacity+1)))
    return {"forecast":decision_record(base),"sensors":instruments}


def evaluate(realized, config, decision, cap, *, width=WIDTH, initial=QUEUE_STARTS, live=live_evaluation):
    lower,upper,ceilings = information_at_decision(realized,width,decision,cap)
    # This uses realized future counts and is retained as an oracle diagnostic.
    oracle = exact(width,realized,config,initial=initial,decision_tick=decision)
    return {"realized_oracle_counts":realized,"decision_tick":decision,"forecast_cap":cap,
            "left_capacity":config.left_capacity,"visible_bins":list(lower[:decision//width]),
            "oracle":decision_record(oracle)} | live(lower,upper,ceilings,config,decision,width,tuple(initial))


def switches(sensor):
    return {"lead","lag"} <= {b["minimax_choice"] for b in sensor["branches"].values()}


def summarize(cases):
    names = ("presence","movement","pocket_fullness","pocket_count")
    return {
        "cases":len(cases),
        "forecast_ambiguous_n":sum(c["forecast"]["worst_regret"]>0 for c in cases),
        "oracle_zero_but_forecast_ambiguous_n":sum(c["oracle"]["worst_regret"]==0 and
                                                 c["forecast"]["worst_regret"]>0 for c in cases),
        "count_strictly_better_than_fullness_n":sum(
            c["sensors"]["pocket_count"]["worst_regret"] < c["sensors"]["pocket_fullness"]["worst_regret"]
            for c in cases),
        "instruments":{name:{
            "pairs_reduced":sum(c["sensors"][name]["worst_regret"]<c["forecast"]["worst_regret"]
                                for c in cases),
            "pairs_resolved":sum(c["sensors"][name]["worst_regret"]==0<c["forecast"]["worst_regret"]
                                 for c in cases),
            "branches_change_minimax_choice_n":sum(switches(c["sensors"][name]) for c in cases),
            "max_reduction_vehicle_seconds":max(c["forecast"]["worst_regret"]-
                                                c["sensors"][name]["worst_regret"] for c in cases),
        } for name in names},
    }


def grid():
    cases = []
    live = lru_cache(maxsize=None)(live_evaluation)
    for capacity,decision,cap,realized in product((1,2),(6,8),(2,3),product(PROFILE,repeat=3)):
        params = Params(left_capacity=capacity,horizon_s=180)
        cases.append(evaluate(realized,params,decision,cap,live=live))
    for case in cases:
        oracle,base = case["oracle"],case["forecast"]
        assert base["delta"][0] <= oracle["delta"][0] <= oracle["delta"][1] <= base["delta"][1]
        assert 0 <= case["sensors"]["movement"]["worst_regret"] <= case["sensors"]["presence"]["worst_regret"]
        assert case["sensors"]["pocket_count"]["worst_regret"] <= case["sensors"]["pocket_fullness"]["worst_regret"]
        assert all(0 <= branch["worst_regret"] <= base["worst_regret"]
                   for branch in case["sensors"].values())
    # Future oracle counts can vary without changing the live information at decision.
    unique = {}
    oracle_success = set()
    for c in cases:
        key = (c["decision_tick"],c["forecast_cap"],c["left_capacity"],tuple(c["visible_bins"]))
        if c["oracle"]["worst_regret"] == 0 and c["forecast"]["worst_regret"] > 0:
            oracle_success.add(key)
        previous = unique.setdefault(key,c)
        assert previous["forecast"] == c["forecast"] and previous["sensors"] == c["sensors"]
    def reduction(c, name):
        return c["forecast"]["worst_regret"]-c["sensors"][name]["worst_regret"]
    strongest = {}
    for name in ("presence","movement","pocket_fullness","pocket_count"):
        best = max(unique.values(),key=lambda c:reduction(c,name))
        if reduction(best,name) > 0:
            strongest[name] = best
    live_cases = list(unique.values())
    live_summary = summarize(live_cases)
    del live_summary["oracle_zero_but_forecast_ambiguous_n"]
    live_summary["forecast_ambiguous_with_at_least_one_zero_regret_oracle_n"] = len(oracle_success)
    panels = {f"decision_{decision}_cap_{cap}":summarize(
        [c for c in live_cases if c["decision_tick"] == decision and c["forecast_cap"] == cap])
        for decision,cap in product((6,8),(2,3))}
    for panel in panels.values():
        del panel["oracle_zero_but_forecast_ambiguous_n"]
    return {"all_oracle_scenarios":summarize(cases),"distinct_live_contexts":live_summary,
            "live_contexts_by_decision_and_cap":panels,
            "live_calculations":live.cache_info().misses,
            "examples":strongest,
            "comparison_scope":"Synthetic D51 queue model. Future count oracle cases repeat the same live context."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(grid(),indent=2)+"\n")
