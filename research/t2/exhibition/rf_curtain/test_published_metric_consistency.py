import math
import unittest
from published_metric_consistency import (
    harmonic_f1, check_reported_row, shahid_2025_reported_bilstm_leguna
)


class PublishedRFMetricAudits(unittest.TestCase):
    def test_reported_leguna_f1_is_arithmetically_incompatible(self):
        row=shahid_2025_reported_bilstm_leguna()
        self.assertAlmostEqual(row['harmonic_f1'], 2*.67*.57/(.67+.57))
        self.assertGreater(row['absolute_discrepancy'], .35)
        self.assertTrue(row['flagged'])
        self.assertEqual(row['evidence_status'],
                         'ORIGINAL_TABLE_TEXT_ARITHMETIC_ONLY_NOT_RF_REPLICATION')

    def test_valid_rounded_values_not_marked(self):
        row=check_reported_row('bike',.99,.98,.98)
        self.assertFalse(row['flagged'])

    def test_zero_recall_and_precision(self):
        self.assertEqual(harmonic_f1(0,0),0)
        self.assertEqual(harmonic_f1(.5,0),0)

    def test_invalid_probabilities_and_nan_rejected(self):
        for vals in ((-1,.5),(1.01,.8),(float('nan'),.5),
                     (True,.5),("1",.8)):
            with self.subTest(vals=vals),self.assertRaises(ValueError):
                harmonic_f1(*vals)
        for bad in (False, -0.1, 1.2, math.inf):
            with self.subTest(bad=bad),self.assertRaises(ValueError):
                check_reported_row('a', .5, .5, bad)


if __name__=='__main__':
    unittest.main()
