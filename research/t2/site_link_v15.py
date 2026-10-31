"""Read a provenance-annotated downstream signal and receiving-road profile.

Input is an extension of an existing t2_dual_site_v11 geometry profile.
Missing downstream section preserves the legacy FIFO configuration.
A documented source label is still NOT field calibration.
"""
from dataclasses import replace
from pathlib import Path
import json
from site_v11 import read_site
from receiving_cells_v15 import LinkConfig

ALLOWED_SOURCES={"synthetic","map_estimate","field_observed","official_plan","published"}
NUMERIC=("receiver_slots","receiver_headway_s","downstream_cycle_s",
         "downstream_green_s","downstream_offset_s")

def read_link_site(path):
    path=Path(path)
    base=read_site(path)
    raw=json.loads(path.read_text(encoding="utf8"))
    downstream=raw.get("spatial_downstream")
    if downstream is None:
        return base
    if downstream.get("mode")!="cells":
        raise ValueError("only cells downstream extension supported")
    values={}
    for key in NUMERIC:
        item=downstream.get(key)
        if not isinstance(item,dict) or item.get("source_type") not in ALLOWED_SOURCES:
            raise ValueError("downstream parameter needs provenance: "+key)
        value=item.get("value")
        if type(value) is not int:
            raise ValueError("downstream temporal/geometry value must be integer: "+key)
        if item["source_type"]!="synthetic" and not item.get("source_note"):
            raise ValueError("downstream external source note required: "+key)
        values[key]=value
    LinkConfig(cells=values["receiver_slots"],
        downstream_cycle_s=values["downstream_cycle_s"],
        downstream_green_s=values["downstream_green_s"],
        downstream_offset_s=values["downstream_offset_s"],
        exit_headway_s=values["receiver_headway_s"])
    cfg=replace(base["config"],receiver_mode="cells",**values)
    result=dict(base)
    result["config"]=cfg
    result["calibration_status"]="NOT_CALIBRATED"
    result["downstream_mode"]="CELLULAR_LINK_UNCALIBRATED"
    result["downstream_provenance"]={key:downstream[key] for key in NUMERIC}
    return result
