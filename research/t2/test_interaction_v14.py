import unittest
from interaction_v14 import analyze

class InteractionTests(unittest.TestCase):
    def test_exact_matched_difference_in_differences(self):
        rows=[]
        for rate in ('steady','surge'):
            for turn in ('steady','shift'):
                for arrival_offset in (0,30):
                    for seed in range(6):
                        for signal_offset in (0,20,40):
                            for pocket in (14.,70.):
                                value=100+10*(pocket==70.)+3*(signal_offset==40 and pocket==70.)
                                rows.append({'rate':rate,'turn':turn,'arrival_offset':arrival_offset,
                                  'seed':seed,'signal_offset':signal_offset,
                                  'pocket_m':pocket,'network_total':value})
        r=analyze(rows)
        self.assertEqual(len(r),8)
        self.assertTrue(all(x['interaction_signal40_vs_0']==3 for x in r))
    def test_missing_cells_rejected(self):
        with self.assertRaises(KeyError):analyze([])

if __name__=='__main__':unittest.main(verbosity=2)
