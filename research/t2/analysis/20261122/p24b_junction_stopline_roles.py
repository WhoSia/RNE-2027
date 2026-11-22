"""P24b: classify static type294 features by *structural* relation to a junction.

Not a vehicle-right-of-way or light-controller map. Use exact P24 source gate.
"""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
from p24_xodr_static_signal_audit import MAP_SHA, PDF_SHA, verify, pose

def structural_roles(map_file,document_pdf):
    verify(map_file,MAP_SHA);verify(document_pdf,PDF_SHA)
    root=ET.parse(map_file).getroot()
    items=[]
    for road in root.findall("road"):
        successor=road.find("link/successor")
        predecessor=road.find("link/predecessor")
        s_len=float(road.get("length"))
        for sig in road.findall("signals/signal"):
            s=float(sig.get("s"))
            if sig.get("type")!="294" or sig.get("dynamic")!="no":
                raise ValueError("unsupported marker")
            if road.get("junction")!="-1":
                role="WITHIN_JUNCTION_CONNECTOR"
            elif (successor is not None and successor.get("elementType")=="junction"
                  and s_len-s<=1.0):
                role="INBOUND_ROAD_APPROACH_END"
            elif (predecessor is not None and predecessor.get("elementType")=="junction"
                  and s<=1.0):
                role="OUTBOUND_ROAD_JUNCTION_START"
            else:role="UNDETERMINED"
            valid=sig.findall("validity")
            items.append({"road_id":road.get("id"),"marker_id":sig.get("id"),
                "role":role,"s_m":round(s,3),"distance_to_road_end_m":round(s_len-s,3),
                "junction_road_attribute":road.get("junction"),
                "explicit_lane_validity_count":len(valid),
                "lane_scope_verified":False,"controller_id":None,
                "right_of_way_verified":False})
    counts={k:sum(r["role"]==k for r in items) for k in
        ("INBOUND_ROAD_APPROACH_END","OUTBOUND_ROAD_JUNCTION_START",
         "WITHIN_JUNCTION_CONNECTOR","UNDETERMINED")}
    if len(items)!=7:raise ValueError("unexpected map feature census")
    return {"protocol":"P24B_STATIC_STOPLINE_STRUCTURAL_CANDIDATES",
        "source_sha256":{"map":MAP_SHA,"pdf":PDF_SHA},
        "marker_count":len(items),"roles":counts,"features":items,
        "inbound_candidate_road_ids":sorted(x["road_id"] for x in items
            if x["role"]=="INBOUND_ROAD_APPROACH_END"),
        "gates":{"structural_role_rule_executed":True,
          "stopline_lane_validity_explicit":False,
          "observed_light_id_crosswalk":False,
          "movement_specific_discharge":False},
        "caveat":"Role is based on road junction connectivity and s position; not proof that a signal head controls the road lane."}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("map",type=Path);p.add_argument("pdf",type=Path);p.add_argument("output",type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(structural_roles(a.map,a.pdf),sort_keys=True,indent=2)+"\n")
