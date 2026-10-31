"""Run one provenance-checked site profile across paired bay lengths."""
from dataclasses import replace
from pathlib import Path
import json,sys
from site_config_v09 import read_site
from world_contact_v09 import demand,run

def execute(site_file):
    site=read_site(site_file)
    config=site["config"]
    stream=demand(config)
    results=[]
    for length in (14,28,42,70):
        y=run(replace(config,bay_length_m=length),stream)
        results.append({"bay_length_m":length,"left_exits":y["exits_L"],
            "through_exits":y["exits_S"],
            "still_outside":y["still_outside"],
            "left_block_s":y["blocked_L_seconds"]})
    return {"site_label":site["site_label"],"provenance":site["provenance"],
        "world_contact_status":site["world_contact_status"],
        "field_calibrated":False,"paired_interventions":results}

if __name__=="__main__":
    source=Path(sys.argv[1]);dest=Path(sys.argv[2])
    dest.parent.mkdir(exist_ok=True,parents=True)
    dest.write_text(json.dumps(execute(source),indent=2)+"\n")
    print("wrote",dest)
