import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from pavement_material import MaterialMap
M='''<OpenDRIVE><road id="r" length="40"><lanes><laneSection s="0"><right><lane id="-1" type="driving"><material sOffset="0" friction="0.8" surface="asphalt"/><material sOffset="20" friction="0.5" surface="concrete"/></lane></right></laneSection></lanes></road></OpenDRIVE>'''
class Materials(unittest.TestCase):
 def test_first_station(self):self.assertEqual(MaterialMap(M).at('r',0,-1)['mu_source'],.8)
 def test_knot_right_continuous(self):self.assertEqual(MaterialMap(M).at('r',20,-1)['mu_source'],.5)
 def test_knot_left(self):self.assertEqual(MaterialMap(M).at('r',19.99,-1)['mu_source'],.8)
 def test_effective_unknown(self):self.assertIsNone(MaterialMap(M).at('r',25,-1)['effective_mu'])
 def test_surface_not_inferred(self):self.assertEqual(MaterialMap(M.replace(' surface="asphalt"','')).at('r',1,-1)['surface'],None)
 def test_missing_material(self):self.assertEqual(MaterialMap(M.replace('<material sOffset="0" friction="0.8" surface="asphalt"/>','')).at('r',10,-1)['status'],'UNKNOWN')
 def test_negative_friction_rejected(self):
  with self.assertRaises(ValueError):MaterialMap(M.replace('friction="0.8"','friction="-0.8"'))
 def test_unsorted_rejected(self):
  with self.assertRaises(ValueError):MaterialMap(M.replace('sOffset="20"','sOffset="0"'))
 def test_section_end_boundary(self):self.assertEqual(MaterialMap(M).at('r',40,-1)['status'],'UNKNOWN')
 def test_crg_override_unknown(self):
  changed=M.replace('<lanes>','<surface><CRG purpose="friction" file="absent.crg"/></surface><lanes>')
  self.assertEqual(MaterialMap(changed).at('r',10,-1)['reason'],'POSSIBLE_CRG_OVERRIDE')
 def test_object_patch_unknown(self):
  changed=M.replace('<lanes>','<objects><object><material friction="0.3"/></object></objects><lanes>')
  self.assertEqual(MaterialMap(changed).at('r',10,-1)['reason'],'POSSIBLE_OBJECT_PATCH_OVERRIDE')
 def test_doctype_denied(self):
  with self.assertRaises(ValueError):MaterialMap('<!DOCTYPE OpenDRIVE>'+M)
if __name__=='__main__':unittest.main()
