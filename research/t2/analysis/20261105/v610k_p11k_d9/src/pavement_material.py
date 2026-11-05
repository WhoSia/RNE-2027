"""ASAM OpenDRIVE 1.8.1 lane material subset; provenance-preserving, no guesses.

A `friction` attribute is an application-dependent source value, not a verified
vehicle-tire coefficient under actual weather. CRG/object overrides fail closed.
"""
from __future__ import annotations
from dataclasses import dataclass
from bisect import bisect_right
from math import isfinite
from xml.etree import ElementTree as ET

@dataclass(frozen=True)
class PavementObservation:
    road_id: str
    section_start_m: float
    lane_id: int
    offset_m: float
    mu_source: float
    surface: str | None
    roughness_source: float | None
    authority: str = 'XODR_LANE_MATERIAL_APPLICATION_DEPENDENT'

class MaterialMap:
    def __init__(self, xml: str):
        if '<!DOCTYPE' in xml.upper() or '<!ENTITY' in xml.upper():
            raise ValueError('external entities/DOCTYPE prohibited')
        root=ET.fromstring(xml)
        if root.tag!='OpenDRIVE':raise ValueError('OpenDRIVE root required')
        self.data={};self.unresolved=set()
        for road in root.findall('road'):
            rid=road.get('id');length=float(road.get('length','nan'))
            if not isfinite(length) or length<=0:raise ValueError('invalid road length')
            if road.find('./surface/CRG') is not None:
                # CRG purpose=friction can override lane material; do not misrepresent.
                self.unresolved.add((rid,'EXTERNAL_CRG_SURFACE_UNRESOLVED'))
            if road.find('.//objects/object/material') is not None:
                self.unresolved.add((rid,'OBJECT_MATERIAL_PATCH_UNRESOLVED'))
            sections=road.findall('./lanes/laneSection')
            prev=-1.
            for index,sec in enumerate(sections):
                ss=float(sec.get('s','nan'))
                if not isfinite(ss) or ss<0 or ss>=length or ss<=prev:
                    raise ValueError('unordered lane section')
                prev=ss
                section_end=float(sections[index+1].get('s')) if index+1<len(sections) else length
                for lane in sec.findall('.//lane'):
                    lid=int(lane.get('id'))
                    values=[];prev_offset=-1.
                    mats=lane.findall('material')
                    if lid==0 and mats:raise ValueError('center lane cannot define material')
                    for m in mats:
                        off=float(m.get('sOffset','nan'))
                        mu=float(m.get('friction','nan'))
                        rough=float(m.get('roughness')) if m.get('roughness') is not None else None
                        if not isfinite(off) or off<0 or off<=prev_offset or off>=section_end-ss:
                            raise ValueError('invalid material sOffset')
                        if not isfinite(mu) or mu<0 or (rough is not None and (not isfinite(rough) or rough<0)):
                            raise ValueError('invalid material attributes')
                        prev_offset=off
                        values.append(PavementObservation(rid,ss,lid,off,mu,m.get('surface'),rough))
                    self.data[(rid,ss,lid)]=(section_end,tuple(values))

    def at(self,road_id:str,s_m:float,lane_id:int):
        matching=[(ss,end,entries) for (rid,ss,lid),(end,entries) in self.data.items()
                  if rid==road_id and lid==lane_id and ss<=s_m<end]
        if len(matching)!=1:
            return {'status':'UNKNOWN','reason':'NO_UNIQUE_LANE_SECTION'}
        ss,end,entries=matching[0]
        if (road_id,'EXTERNAL_CRG_SURFACE_UNRESOLVED') in self.unresolved:
            return {'status':'UNKNOWN','reason':'POSSIBLE_CRG_OVERRIDE'}
        if (road_id,'OBJECT_MATERIAL_PATCH_UNRESOLVED') in self.unresolved:
            return {'status':'UNKNOWN','reason':'POSSIBLE_OBJECT_PATCH_OVERRIDE'}
        i=bisect_right([x.offset_m for x in entries],s_m-ss)-1
        if i<0:return {'status':'UNKNOWN','reason':'NO_EXPLICIT_MATERIAL_AT_STATION'}
        p=entries[i]
        return {'status':'DECLARED_ONLY','mu_source':p.mu_source,'surface':p.surface,
                'roughness_source':p.roughness_source,'source':p.authority,
                'weather_verified':False,'tire_verified':False,'effective_mu':None}
