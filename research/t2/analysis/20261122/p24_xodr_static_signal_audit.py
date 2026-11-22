"""P24: source-locked DLR XODR static map markers versus official head coordinates.
Geometric near neighbors only; NOT traffic light control assignments.
"""
from pathlib import Path
from collections import Counter
import hashlib, json, math, xml.etree.ElementTree as ET
from pyproj import CRS,Transformer

MAP_SHA="256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4"
PDF_SHA="94fd9ebd32d04a9c35b02be526fbd11a8d5a613933d7961fde800386853b34f3"
# Official PDF pp.12-13 Table 3. Repeated coordinates are distinct heads.
HEADS={
 1:[(604755.480,5792814.102),(604749.966,5792812.211)],
 2:[(604761.424,5792815.793)],
 3:[(604790.745,5792814.817),(604792.294,5792809.095),(604793.765,5792806.195)],
 4:[(604795.332,5792803.053),(604796.300,5792798.214)],
 5:[(604793.626,5792779.886),(604787.472,5792776.873)],
 6:[(604784.549,5792776.031)],
 7:[(604780.221,5792775.418),(604775.881,5792774.066)],
 8:[(604748.909,5792774.532),(604748.134,5792780.177)],
 9:[(604746.834,5792783.266),(604745.843,5792786.123),(604744.122,5792790.989)]}

def verify(path,digest):
    if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=digest:
        raise ValueError("source SHA256 mismatch")

def pose(road,s):
    if not 0<=s<=float(road.get("length"))+1e-7:raise ValueError("out of road")
    geometry=None
    for g in road.findall("planView/geometry"):
        if float(g.get("s"))<=s+1e-8:geometry=g
        else:break
    if geometry is None:raise ValueError("missing geometry")
    ds=s-float(geometry.get("s"))
    if ds < -1e-7 or ds>float(geometry.get("length"))+1e-6:
        raise ValueError("geometry gap")
    x,y,h=map(float,(geometry.get("x"),geometry.get("y"),geometry.get("hdg")))
    if geometry.find("line") is not None:
        return x+ds*math.cos(h),y+ds*math.sin(h),h
    arc=geometry.find("arc")
    if arc is None:raise ValueError("unsupported geometry")
    k=float(arc.get("curvature"))
    if abs(k)<1e-12:return x+ds*math.cos(h),y+ds*math.sin(h),h
    e=h+k*ds
    return x+(math.sin(e)-math.sin(h))/k,y-(math.cos(e)-math.cos(h))/k,e

def audit(map_file,pdf_file):
    verify(map_file,MAP_SHA);verify(pdf_file,PDF_SHA)
    root=ET.parse(map_file).getroot()
    if root.tag!="OpenDRIVE":raise ValueError("not OpenDRIVE")
    head=root.find("header")
    geo=head.findtext("geoReference")
    if not geo or "+proj=tmerc" not in geo:raise ValueError("projection missing")
    proj=CRS.from_proj4(geo)
    forward=Transformer.from_crs(CRS.from_epsg(32632),proj,always_xy=True)
    inverse=Transformer.from_crs(proj,CRS.from_epsg(32632),always_xy=True)
    roads=root.findall("road")
    signals=[]
    for road in roads:
        for s in road.findall("signals/signal"):
            x,y,h=pose(road,float(s.get("s")))
            t=float(s.get("t"))
            east,north=inverse.transform(x-t*math.sin(h),y+t*math.cos(h))
            signals.append({"road_id":road.get("id"),"feature_id":s.get("id"),
                "dynamic":s.get("dynamic"),"type":s.get("type"),
                "utm":[round(east,3),round(north,3)]})
    if len(signals)!=7 or any(v["dynamic"]!="no" for v in signals):
        raise ValueError("map features changed: re-review")
    ids=sorted(set(s["feature_id"] for s in signals))
    if set(ids)&set(map(str,range(1,31))):
        raise ValueError("unexpected observed-ID overlap")
    candidates=[]
    for identifier,xy in sorted(HEADS.items()):
        for index,(east,north) in enumerate(xy,1):
            x,y=forward.transform(east,north)
            close=sorted(({"feature_id":s["feature_id"],"road_id":s["road_id"],
                "distance_m":round(math.hypot(east-s["utm"][0],north-s["utm"][1]),3)}
                for s in signals),key=lambda a:a["distance_m"])[:3]
            candidates.append({"observed_light_id":identifier,"head_index":index,
                "utm":[east,north],"local_xy":[round(x,3),round(y,3)],
                "nearest_static_map_features":close,
                "controlling_lane":None,"movement":None,
                "verdict":"UNVERIFIED_NEAR_NEIGHBOR_ONLY"})
    return {"status":"P24_GEOMETRIC_NEAR_NEIGHBORS_ONLY","map_sha256":MAP_SHA,
        "documentation_sha256":PDF_SHA,"map_version":head.get("version"),
        "map_date":head.get("date"),"roads":len(roads),
        "junctions":len(root.findall("junction")),
        "static_signals":signals,"unique_static_ids":ids,
        "original_motor_vehicle_heads":len(candidates),"candidates":candidates,
        "gates":{"source_verified":True,"utm_projection_verified":True,
            "signal_lanes_verified":False,"signal_movements_verified":False,
            "vehicle_headways_verified":False,"sumo_external_comparison":False},
        "warning":"2015 map dynamic=no ID3006xx != observed 2023 signal ID1..30. Distance is not a controller crosswalk."}

if __name__=="__main__":
    import argparse
    a=argparse.ArgumentParser()
    a.add_argument("map",type=Path);a.add_argument("pdf",type=Path);a.add_argument("out",type=Path)
    v=a.parse_args()
    v.out.write_text(json.dumps(audit(v.map,v.pdf),indent=2,sort_keys=True)+"\n")
