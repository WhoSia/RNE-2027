import csv, os, tempfile, unittest
from d42_multibatch import volume_summary

class DynamicMovementSchema(unittest.TestCase):
    def create(self,keys,vals):
        h=tempfile.NamedTemporaryFile(mode='w',suffix='.csv',delete=False,newline='')
        with h:
            w=csv.writer(h);w.writerow(['timestamp']+keys)
            for i in range(900):w.writerow([f'2023-09-24 12:{i//60:02}:{i%60:02}+00:00']+ ([*vals] if i==0 else [0]*len(vals)))
        self.addCleanup(lambda:os.unlink(h.name))
        return h.name
    def test_27_cols(self):
        p=self.create(['East0South0']+['West1East0']*0,[2])
        r=volume_summary(p);self.assertEqual(r['columns'],1);self.assertEqual(r['total'],2)
    def test_zero_not_reported(self):
        p=self.create(['South0West0'],[0]);self.assertEqual(volume_summary(p)['counts']['North'],0)
    def test_unknown_origin_rejected(self):
        p=self.create(['Bad0East0'],[2]);
        with self.assertRaises(ValueError):volume_summary(p)
    def test_duplicate_column_rejected(self):
        p=self.create(['East0South0','East0South0'],[1,2]);
        with self.assertRaises(ValueError):volume_summary(p)
    def test_negative_count_rejected(self):
        p=self.create(['East0South0'],[-1]);
        with self.assertRaises(ValueError):volume_summary(p)
    def test_900_rows_required(self):
        p=self.create(['East0South0'],[1]);
        with open(p,'a') as f:f.write('2023-09-24 12:15:00+00:00,0\n')
        with self.assertRaises(ValueError):volume_summary(p)
    def test_nonnumeric_rejected(self):
        p=self.create(['West0West1'],['bad']);
        with self.assertRaises(ValueError):volume_summary(p)
if __name__=='__main__':unittest.main()
