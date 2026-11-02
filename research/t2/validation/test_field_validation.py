import csv, os, tempfile, unittest
from field_validation import FIELDS, read_observations, audit, evaluate

class FieldValidationTests(unittest.TestCase):
    def setUp(self):
        self.f=tempfile.NamedTemporaryFile(mode='w',suffix='.csv',delete=False,newline='',encoding='utf-8')
        writer=csv.writer(self.f);writer.writerow(FIELDS)
        self.a=('C1','2026-11-02','AM','J1','N','TH')
        self.b=('C1','2026-11-03','AM','J1','N','TH')
        for key,dep in ((self.a,8),(self.b,6)):
            writer.writerow([*key,10,dep,1,11-dep,20,2,2.0])
        self.f.close()
    def tearDown(self):os.unlink(self.f.name)
    def test_schema(self):self.assertEqual(len(read_observations(self.f.name)),2)
    def test_conservation(self):
        self.assertEqual([r['conservation_residual'] for r in audit(read_observations(self.f.name))],[0,0])
    def test_holdout(self):
        self.assertEqual(evaluate({self.b:5},read_observations(self.f.name),'2026-11-03')['mae_departures'],1)
    def test_missing_predictions(self):
        with self.assertRaises(ValueError):evaluate({},read_observations(self.f.name),'2026-11-03')
    def test_duplicate(self):
        with open(self.f.name,encoding='utf-8') as f:rows=f.readlines()
        with open(self.f.name,'a',encoding='utf-8') as f:f.write(rows[-1])
        with self.assertRaises(ValueError):read_observations(self.f.name)
    def test_negative(self):
        with open(self.f.name,encoding='utf-8') as f:s=f.read()
        with open(self.f.name,'w',encoding='utf-8') as f:f.write(s.replace(',10,8,',',-10,8,'))
        with self.assertRaises(ValueError):read_observations(self.f.name)
if __name__=='__main__':unittest.main()
