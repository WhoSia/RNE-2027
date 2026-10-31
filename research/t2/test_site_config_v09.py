import unittest,tempfile,pathlib,json
from site_config_v09 import KEYS,read_site
from world_contact_v09 import Params

class SiteTests(unittest.TestCase):
    def sample(self):
        c=Params()
        return {"schema_version":"t2_site_v09","site_label":"Hypothetical A",
            "parameters":{k:{"value":getattr(c,k),"source_type":"synthetic"}
                          for k in KEYS}}
    def load(self,doc):
        with tempfile.TemporaryDirectory() as name:
            f=pathlib.Path(name)/"site.json"
            f.write_text(json.dumps(doc))
            return read_site(f)
    def test_synthetic(self):
        self.assertEqual(self.load(self.sample())["world_contact_status"],"SYNTHETIC_ONLY")
    def test_observed_requires_source(self):
        doc=self.sample()
        doc["parameters"]["bay_length_m"]={"value":42,"source_type":"field_observed"}
        with self.assertRaises(ValueError):self.load(doc)
    def test_estimated_not_calibrated(self):
        doc=self.sample()
        doc["parameters"]["bay_length_m"]={"value":42,"source_type":"estimated",
                                           "source_note":"map measurement only"}
        val=self.load(doc)
        self.assertFalse(val["field_calibrated"])
        self.assertEqual(val["world_contact_status"],"UNVERIFIED_MODEL_INPUT")
    def test_missing_parameter(self):
        doc=self.sample()
        del doc["parameters"]["cycle_s"]
        with self.assertRaises(ValueError):self.load(doc)
if __name__=="__main__":
    unittest.main(verbosity=2)
