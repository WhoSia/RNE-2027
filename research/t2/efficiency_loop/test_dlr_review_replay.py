import json
from unittest import TestCase

from audit_dlr_reviews import FIELDS, compare
from dlr_review_replay import CLOCK, source_for
from render_dlr_review import MARKER, render


class ReviewTools(TestCase):
    def test_source_window_is_half_open(self):
        before = "trajectories_230924-121500_230924-123000.csv"
        after = "trajectories_230924-123000_230924-124500.csv"
        self.assertEqual(source_for(CLOCK,[before,after]),(after,900))
        with self.assertRaises(ValueError):
            source_for(CLOCK,[before])

    def test_payload_cannot_close_its_own_script_tag(self):
        html = render("<script>"+MARKER+"</script>",{"test":"</script>"})
        self.assertEqual(html.count("</script>"),1)
        self.assertEqual(json.loads(html.removeprefix("<script>").removesuffix("</script>")),{"test":"</script>"})

    def test_unknown_agreement_kept_separate_and_missing_visible(self):
        base = {key:"unknown" for key in FIELDS} | {"evidence":"test observation"}
        aa = {"reviewer":"R1","cases":{"C1":base,"C2":base|{"leader_movement":"through"}}}
        bb = {"reviewer":"R2","cases":{"C1":base,"C2":base|{"leader_movement":"left"}}}
        result = compare(aa,bb,{"C1","C2","C3"})
        self.assertEqual(result["fields"]["leader_movement"],{
            "joint_cases":2,"agree_including_unknown":1,"joint_determinate":1,
            "agree_given_joint_determinate":0})
        self.assertEqual(result["missing_by_reviewer"],{"R1":["C3"],"R2":["C3"]})
        self.assertEqual(result["disputes"]["C2"]["fields"]["leader_movement"],["through","left"])
        with self.assertRaises(ValueError):
            compare(aa,aa,{"C1","C2"})
