"""Run provenance-gated physical two-lane scenarios with matched arrival stream."""
from dataclasses import replace
from pathlib import Path
import json
from site_v11 import read_site
from spatial_v10 import arrivals
from dual_lane_v11 import run

def execute(path):
    site=read_site(path)
    dual=site["config"]
    stream=arrivals(dual.base)
    scenarios=[]
    for length in (14.,28.,42.,70.):
        cfg=replace(dual,base=replace(dual.base,pocket_length_m=length))
        out=run(cfg,stream)
        scenarios.append({"pocket_m":length,"through_exits":out["exit_S"],
            "left_exits":out["exit_L"],"outside":out["outside"],
            "lane_changes":out["changes_A_to_B"],
            "pocket_block_seconds":out["pocket_block_seconds"],
            "network_through":out["network_out_S"],"network_left":out["network_out_L"],
            "receiver_final":out["receiver_final"],
            "receiver_full_denied_s":out["receiver_full_denied_s"]})
    return {"site_label":site["label"],"downstream_mode":site["downstream_mode"],
        "input_status":site["input_status"],
        "calibration_status":site["calibration_status"],
        "provenance":site["provenance"],
        "interventions":scenarios,
        "caution":"Source-asserted values are not automatically field calibrated."}

if __name__=="__main__":
    import sys
    result=execute(sys.argv[1])
    p=Path(sys.argv[2]);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print("rows",len(result["interventions"]))
