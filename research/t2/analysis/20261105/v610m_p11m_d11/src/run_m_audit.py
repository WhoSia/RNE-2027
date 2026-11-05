import sys, json, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from variable_lane_curvature import lane_curvature_variable
from opendrive_lateral import parse_lateral

def case(kind, offset,station):
 return f'<OpenDRIVE><road id="a" length="20"><planView><geometry s="0" x="0" y="0" hdg="0" length="20">{kind}</geometry></planView><elevationProfile><elevation s="0" a="0" b="0" c="0" d="0"/></elevationProfile><lanes><laneOffset s="0" a="{offset[0]}" b="{offset[1]}" c="{offset[2]}" d="{offset[3]}"/><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="4" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road></OpenDRIVE>'

def independent_xy_curvature(xml,s,h=0.002):
 net,cross=parse_lateral(xml);r=net.roads[0]
 def xy(q):
  p=r.reference_at(q);t=cross['a'].offset(q)-2
  return p['x_m']-t*math.sin(p['hdg_rad']),p['y_m']+t*math.cos(p['hdg_rad'])
 l,m,u=xy(s-h),xy(s),xy(s+h)
 dx=(u[0]-l[0])/(2*h);dy=(u[1]-l[1])/(2*h)
 ddx=(u[0]-2*m[0]+l[0])/h**2;ddy=(u[1]-2*m[1]+l[1])/h**2
 return (dx*ddy-dy*ddx)/math.hypot(dx,dy)**3

if __name__=='__main__':
 cases=[('ARC_CUBIC','<arc curvature=".02"/>',[.2,.03,.001,-.00002],9),('SPIRAL_QUAD','<spiral curvStart=".01" curvEnd=".07"/>',[.2,.02,.002,0],8),('LINE_QUAD','<line/>',[0,0,.01,0],7),('ARC_CONSTANT','<arc curvature=".02"/>',[0,0,0,0],10)]
 results=[]
 for name,kind,offset,s in cases:
  x=case(kind,offset,s);v=lane_curvature_variable(x,'a',-1,s);num=independent_xy_curvature(x,s)
  results.append({'case':name,'s_m':s,'symbolic_inv_m':v['k_lane_inv_m'],'numerical_sampled_xy_inv_m':num,'absolute_difference_inv_m':abs(v['k_lane_inv_m']-num)})
 out={'study':'T2 M synthetic variable-offset planar geometry','source_type':'SYNTHETIC_NO_REAL_ROAD','independent_method':'finite difference on sampled OpenDRIVE XY coordinates; h=0.002 m','tests':results,'max_absolute_difference_inv_m':max(v['absolute_difference_inv_m'] for v in results),'scope':'Planar reference curves and local regular offset only. No 3D roll/grade, legal turn or safe-speed claims.'}
 p=Path(__file__).parents[1]/'results';p.mkdir(exist_ok=True)
 (p/'M_geometry_independent_audit.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
