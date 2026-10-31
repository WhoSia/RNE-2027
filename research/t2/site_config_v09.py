"""Site profile reader: every model input retains its provenance.

Input JSON must be labeled synthetic, field_observed, published or
estimated per parameter. This does not *verify* the asserted source note
or confer calibration, and field data should be anonymous aggregates.
"""
import json
from dataclasses import replace
from pathlib import Path
from world_contact_v09 import Params,check

KEYS=("bay_length_m","straight_storage_m","upstream_storage_m","pitch_m",
      "cycle_s","left_green_s","straight_green_s","clearance_s",
      "arrival_rate_vph","turn_share")
SOURCE_TYPES={"synthetic","field_observed","published","estimated"}

def read_site(path):
    obj=json.loads(Path(path).read_text(encoding="utf8"))
    if obj.get("schema_version")!="t2_site_v09":
        raise ValueError("schema version")
    if not obj.get("site_label") or not isinstance(obj.get("parameters"),dict):
        raise ValueError("missing site label/parameters")
    values={};provenance={}
    for key in KEYS:
        item=obj["parameters"].get(key)
        if not isinstance(item,dict):
            raise ValueError("missing provenance for "+key)
        origin=item.get("source_type")
        if origin not in SOURCE_TYPES:
            raise ValueError("unrecognized source type for "+key)
        if origin!="synthetic" and not item.get("source_note"):
            raise ValueError("external parameter lacks source note for "+key)
        val=item.get("value")
        if isinstance(val,bool) or not isinstance(val,(int,float)):
            raise ValueError("invalid numeric parameter "+key)
        values[key]=val
        provenance[key]={"source_type":origin,"source_note":item.get("source_note","")}
    config=replace(Params(),**values)
    check(config)
    return {"config":config,"site_label":obj["site_label"],"provenance":provenance,
        "field_calibrated":False,
        "world_contact_status":("UNVERIFIED_MODEL_INPUT" if any(
            p["source_type"]!="synthetic" for p in provenance.values())
            else "SYNTHETIC_ONLY")}
