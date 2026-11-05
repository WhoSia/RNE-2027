"""Generate reproducible synthetic road geometry audit; no traffic policy run."""
import json,math,sys
from pathlib import Path
from scipy.integrate import quad
from opendrive_ir import Geometry,_simpson_clothoid
from opendrive_lateral import parse_lateral
ROOT=Path(__file__).resolve().parents[1]
X='''<OpenDRIVE><header revMajor="1" revMinor="8"/><road id="synthetic" length="20" junction="-1"><planView><geometry s="0" x="0" y="0" hdg="0" length="20"><spiral curvStart="0" curvEnd="0.1"/></geometry></planView><elevationProfile><elevation s="0" a="3" b="0.01" c="0" d="0"/></elevationProfile><lateralProfile><superelevation s="0" a="0.1" b="0" c="0" d="0"/></lateralProfile><lanes><laneOffset s="0" a="0.5" b="0" c="0" d="0"/><laneSection s="0"><left><lane id="1" type="driving"><width sOffset="0" a="3.5" b="0" c="0" d="0"/></lane></left><right><lane id="-1" type="driving"><width sOffset="0" a="3" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road></OpenDRIVE>'''
net,cross=parse_lateral(X);road=net.roads[0];cs=cross['synthetic']
worst=0.
for k0 in (-.2,-.02,0.,.05,.2):
 for k1 in (-.2,0.,.01,.2):
  for L in (5.,20.,50.,100.):
   a=Geometry(0,0,0,0,L,'spiral',k0,k1);x,y,_=_simpson_clothoid(a,L)
   sl=(k1-k0)/L
   xx=quad(lambda s:math.cos(k0*s+.5*sl*s*s),0,L,epsabs=1e-11)[0]
   yy=quad(lambda s:math.sin(k0*s+.5*sl*s*s),0,L,epsabs=1e-11)[0]
   worst=max(worst,abs(x-xx),abs(y-yy))
out={'research_date':'2026-11-05','kind':'SYNTHETIC_COMPUTATIONAL_AUDIT','road_type':'spiral+elevation+laneOffset+superelevation','independent_reference':'scipy.integrate.quad and scipy.special.fresnel (unit test)','spiral_stress_cases':80,'max_coordinate_abs_error_m':worst,'first_reference_point':road.reference_at(0),'endpoint_reference_point':road.reference_at(20),'right_lane_center_s0':cs.lane_center(road,0,-1),'left_lane_center_s10':cs.lane_center(road,10,1),'policy_executed':False,'external_xodr_raw_tested':False,'sumo_executed':False,'jurisdiction_law_certified':False,'notes':['Lateral point assumes simple roll and no shape, lane height, CRG surface, or level=true','Numerical grid not a global numerical error bound; no external OpenDRIVE certification']}
(ROOT/'results'/'H_audit.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:out[k] for k in ['spiral_stress_cases','max_coordinate_abs_error_m','endpoint_reference_point','right_lane_center_s0']},indent=2))
