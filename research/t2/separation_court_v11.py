"""Conditional noninterference theorem for fully separated two-lane scenario.

If all straight cars use lane B and all left cars use lane A, lane changes
are forbidden and downstream storage is independent, the transition of B
does not depend on the pocket geometry. An induction over time steps
therefore proves the full B path and straight departures are invariant
under pocket length. NOT a theorem about real connected road networks.
"""
from dataclasses import replace
from dual_lane_v11 import DualConfig,run
from spatial_v10 import Config,arrivals

def court():
    records=[]
    for seed in range(10):
        for ratio in (.15,.30,.45):
            base=Config(seed=seed,left_fraction=ratio,duration_s=1800)
            stream=arrivals(base)
            cases=[]
            for length in (0.,14.,28.,42.,70.):
                cfg=DualConfig(base=replace(base,pocket_length_m=length),
                     through_B_share=1.0,allow_lane_changes=False)
                y=run(cfg,stream)
                cases.append((length,y["exit_S"],
                              tuple(x["exit_S"] for x in y["cycles"])))
            if any(x[1:]!=cases[0][1:] for x in cases):
                raise AssertionError(("independent lane violated",seed,ratio,cases))
            records.append({"seed":seed,"turn_ratio":ratio,
                            "through_exits":cases[0][1]})
    return {"status":"PASS_SYNTHETIC_CONDITIONAL",
      "independent_cases":len(records),"pocket_lengths_m":[0.,14.,28.,42.,70.],
      "records":records}

if __name__=="__main__":
    import json
    print(json.dumps(court(),indent=2))
