import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from road_ir import *

CF={'roads':[{'id':'a','points':[{'x':0,'y':0},{'x':100,'y':0}],'lanes':[{'maxSpeed':10},{'maxSpeed':11}]},{'id':'b','points':[{'x':100,'y':0},{'x':100,'y':40}],'lanes':[{'maxSpeed':8}]}], 'intersections':[{'id':'J','roadLinks':[{'startRoad':'a','endRoad':'b','type':'turn_right','laneLinks':[{'startLaneIndex':1,'endLaneIndex':0}]}]}]}
SUMO='''<net><edge id="a"><lane id="a_0" speed="10" length="100"/></edge><edge id="b"><lane id="b_0" speed="8" length="40"/></edge><connection from="a" to="b" fromLane="0" toLane="0" dir="r" tl="J" linkIndex="0"/></net>'''
class TestRoadIR(unittest.TestCase):
 def test_cityflow_lane_topology(self):
  r=import_cityflow(CF);self.assertEqual(r.summary()['lanes'],3);self.assertEqual(r.summary()['connections'],1);self.assertTrue(r.route_exists(['a_1','b_0']))
 def test_sumo_lane_topology(self):
  r=import_sumo_net(SUMO);self.assertEqual(r.summary()['signaled_links'],1);self.assertTrue(r.route_exists(['a_0','b_0']))
 def test_sumo_no_route(self):
  self.assertFalse(import_sumo_net(SUMO).route_exists(['b_0','a_0']))
 def test_unknown_conflicts_explicit(self):
  self.assertIn('geometric_conflicts_not_inferred',import_sumo_net(SUMO).unresolved)
 def test_cityflow_bad_lane_index(self):
  import copy
  x=copy.deepcopy(CF);x['intersections'][0]['roadLinks'][0]['laneLinks'][0]['startLaneIndex']=99
  with self.assertRaises(ValueError):import_cityflow(x)
 def test_sumo_dangling_edge(self):
  with self.assertRaises(KeyError):import_sumo_net(SUMO.replace('to="b"','to="missing"'))
 def test_duplicate_ids(self):
  with self.assertRaises(ValueError):RoadIR((RoadLane('x',1,1),RoadLane('x',2,2)),(), 'test')
 def test_invalid_speed(self):
  with self.assertRaises(ValueError):RoadLane('x',3,0)
 def test_sumo_bad_root(self):
  with self.assertRaises(ValueError):import_sumo_net('<roads/>')
 def test_cityflow_empty(self):
  with self.assertRaises(ValueError):import_cityflow({'roads':[]})
if __name__=='__main__':unittest.main()

class OSMnxAdapterTests(unittest.TestCase):
 def test_osmnx_road_segments_only(self):
  import networkx as nx
  from road_ir import import_osmnx_graph
  g=nx.MultiDiGraph();g.add_edge(1,2,key=0,length=90,speed_kph=36)
  r=import_osmnx_graph(g)
  self.assertEqual(len(r.lanes),1);self.assertEqual(r.lanes[0].speed_mps,10)
  self.assertEqual(len(r.connections),0);self.assertIn('turn_restrictions_unverified',r.unresolved)
 def test_missing_osmnx_speed_fails_closed(self):
  import networkx as nx
  from road_ir import import_osmnx_graph
  g=nx.MultiDiGraph();g.add_edge(1,2,length=80)
  with self.assertRaises(ValueError):import_osmnx_graph(g)
