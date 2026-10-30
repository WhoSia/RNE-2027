"""Auditable tests for the observation projection and finite enumeration."""
import unittest
from collections import Counter
from observability_court_v06 import Observation, project, hidden_signature, enumerate_witness

class TestObservationCourt(unittest.TestCase):
    def test_projection_only_sees_aggregate_counts(self):
        r={'route_exits':{'L':2,'S':3},'stats':{'fork_block_cap_s':8,
          'fork_block_gap_bay_s':4,'fork_block_gap_downstream_s':3}}
        self.assertEqual(project(r,20,10),Observation(20,10,3,2))
        self.assertEqual(hidden_signature(r),(8,4,3))

    def test_projection_is_not_trivially_a_signature(self):
        a={'route_exits':{'L':2,'S':3},'stats':{'fork_block_cap_s':8}}
        b={'route_exits':{'L':2,'S':3},'stats':{'fork_block_cap_s':15}}
        self.assertEqual(project(a,20,10),project(b,20,10))
        self.assertNotEqual(hidden_signature(a),hidden_signature(b))
        # This proves only properties of the observation operator itself,
        # not that both signatures are reachable in the same traffic model.

    def test_exhaustive_search_is_reproducible_or_explicitly_inconclusive(self):
        a=enumerate_witness(n=8,left=4)
        b=enumerate_witness(n=8,left=4)
        self.assertEqual(a,b)
        self.assertIn(a['status'],{'WITNESS_FOUND','NO_WITNESS_IN_ENUMERATED_DOMAIN'})
        if a['status']=='WITNESS_FOUND':
            x,y=a['A'],a['B']
            self.assertNotEqual(x['hidden_signature'],y['hidden_signature'])
            self.assertEqual(Counter(x['routes']),Counter(y['routes']))
        else:
            self.assertEqual(a['searched'],70)

    def test_search_bounded(self):
        with self.assertRaises(ValueError):
            enumerate_witness(n=30,left=15)

if __name__=='__main__':
    unittest.main()
