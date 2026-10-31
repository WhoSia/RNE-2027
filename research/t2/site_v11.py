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
DOWNSTREAM_FIELDS=("downstream_conflict_gap_s","receiver_slots","receiver_headway_s")
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
    # Optional v1.3 downstream inputs are explicit synthetic defaults if omitted.
    for key in DOWNSTREAM_FIELDS:
        item=params.get(key)
        if item is None:
            item={"value":getattr(DualConfig(),key),"source_type":"synthetic",
                  "source_note":"default model setting"}
        if not isinstance(item,dict) or item.get("source_type") not in SOURCES:
            raise ValueError("downstream provenance required: "+key)
        value=item.get("value")
        if isinstance(value,bool) or not isinstance(value,(int,float)):
            raise ValueError("invalid downstream value: "+key)
        if item["source_type"]!="synthetic" and not item.get("source_note"):
            raise ValueError("downstream source note required: "+key)
        vals[key]=value
        provenance[key]=item
    base=replace(Config(),**{key:vals[key] for key in BASE_FIELDS})
    cfg=DualConfig(base=base,through_B_share=vals["through_B_share"],
           change_zone_m=vals["change_zone_m"],
           allow_lane_changes=bool(obj.get("enable_lane_changes",False)),
           downstream_conflict_gap_s=vals["downstream_conflict_gap_s"],
           receiver_slots=vals["receiver_slots"],
           receiver_headway_s=vals["receiver_headway_s"])
    validate(base)
    if not 0<=cfg.through_B_share<=1 or not 0<=cfg.change_zone_m<=base.approach_length_m:
        raise ValueError("invalid dual-lane road")
    if (not isinstance(cfg.downstream_conflict_gap_s,int) or cfg.downstream_conflict_gap_s<0 or
        not isinstance(cfg.receiver_slots,int) or cfg.receiver_slots<0 or
        not isinstance(cfg.receiver_headway_s,int) or cfg.receiver_headway_s<1):
        raise ValueError("invalid downstream receiver")
    return {"label":obj["site_label"],"config":cfg,"provenance":provenance,
      "downstream_mode":("FINITE_RECEIVER" if cfg.receiver_slots else
          "VIRTUAL_COMMON_GAP" if cfg.downstream_conflict_gap_s else "INDEPENDENT"),
      "calibration_status":"NOT_CALIBRATED",
      "input_status":"SYNTHETIC" if all(x["source_type"]=="synthetic" for x in provenance.values())
        else "SOURCE_ASSERTED_NOT_VALIDATED"}
