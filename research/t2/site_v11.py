"""Provenance for the physical two-lane model; labels are not validation."""
from dataclasses import replace
from pathlib import Path
import json
from spatial_v10 import Config,validate
from dual_lane_v11 import DualConfig

BASE_FIELDS=("approach_length_m","pocket_length_m","cell_m","duration_s",
 "cycle_s","left_green_s","through_green_s","clearance_s",
 "demand_vph","left_fraction")
EXTRA_FIELDS=("through_B_share","change_zone_m")
SOURCES={"synthetic","map_estimate","field_observed","official_plan","published"}

def read_site(path):
    obj=json.loads(Path(path).read_text(encoding="utf8"))
    if obj.get("schema_version")!="t2_dual_site_v11":
        raise ValueError("wrong site schema")
    if not isinstance(obj.get("site_label"),str) or not obj["site_label"].strip():
        raise ValueError("site_label required")
    params=obj.get("parameters",{})
    vals={};provenance={}
    for key in BASE_FIELDS+EXTRA_FIELDS:
        item=params.get(key)
        if not isinstance(item,dict) or item.get("source_type") not in SOURCES:
            raise ValueError("provenance needed: "+key)
        val=item.get("value")
        if isinstance(val,bool) or not isinstance(val,(int,float)):
            raise ValueError("numeric parameter required: "+key)
        if item["source_type"]!="synthetic" and not item.get("source_note"):
            raise ValueError("external parameter lacks source note: "+key)
        vals[key]=val
        provenance[key]=item
    base=replace(Config(),**{key:vals[key] for key in BASE_FIELDS})
    cfg=DualConfig(base=base,through_B_share=vals["through_B_share"],
           change_zone_m=vals["change_zone_m"],
           allow_lane_changes=bool(obj.get("enable_lane_changes",False)))
    validate(base)
    if not 0<=cfg.through_B_share<=1 or not 0<=cfg.change_zone_m<=base.approach_length_m:
        raise ValueError("invalid dual-lane road")
    return {"label":obj["site_label"],"config":cfg,"provenance":provenance,
      "calibration_status":"NOT_CALIBRATED",
      "input_status":"SYNTHETIC" if all(x["source_type"]=="synthetic" for x in provenance.values())
        else "SOURCE_ASSERTED_NOT_VALIDATED"}
