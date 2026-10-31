import unittest,tempfile,pathlib
from field_compare_v09 import read_aggregate_csv,compare

class FieldValidationTests(unittest.TestCase):
    def test_exact_counts(self):
        x=[{'end_s':120,'exit_L':5,'exit_S':10},{'end_s':240,'exit_L':8,'exit_S':21}]
        y=[{'end_s':120,'left_exits':5,'straight_exits':10},{'end_s':240,'left_exits':3,'straight_exits':11}]
        v=compare(x,y)
        self.assertEqual(v['L']['MAE_veh_per_cycle'],0)
        self.assertEqual(v['S']['bias_veh_per_cycle'],0)
    def test_error_and_bias(self):
        x=[{'end_s':120,'exit_L':5,'exit_S':10},{'end_s':240,'exit_L':8,'exit_S':21}]
        y=[{'end_s':120,'left_exits':3,'straight_exits':11},{'end_s':240,'left_exits':5,'straight_exits':11}]
        v=compare(x,y)
        self.assertEqual(v['L']['signed_residuals'],[2,-2])
        self.assertEqual(v['L']['MAE_veh_per_cycle'],2)
    def test_time_alignment_gate(self):
        with self.assertRaises(ValueError):
            compare([{'end_s':120}],[{'end_s':119}])
    def test_csv_validate(self):
        with tempfile.TemporaryDirectory() as p:
            f=pathlib.Path(p)/'a.csv'
            f.write_text('end_s,left_exits,straight_exits\n120,5,10\n240,6,8\n')
            self.assertEqual(len(read_aggregate_csv(f)),2)
            f.write_text('end_s,left_exits,straight_exits\n120,-2,10\n')
            with self.assertRaises(ValueError): read_aggregate_csv(f)

if __name__=='__main__':unittest.main()
