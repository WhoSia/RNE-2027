"""Unit tests for the minimal GitHub SUMO crosswalk implementation."""
import tempfile
import unittest
from pathlib import Path
from sumo_remote_contract import parse_plans, parse_controlled_connections, validate_crosswalk

class TestSignalContract(unittest.TestCase):
    def test_link_index_matches_signal_state_width(self):
        with tempfile.TemporaryDirectory() as d:
            sig = Path(d) / "signal.xml"
            net = Path(d) / "network.xml"
            sig.write_text('<add><tlLogic id="J" programID="P"><phase duration="40" state="Gr"/><phase duration="50" state="rG"/></tlLogic></add>')
            net.write_text('<net><connection tl="J" linkIndex="0"/><connection tl="J" linkIndex="1"/></net>')
            self.assertEqual(validate_crosswalk(parse_plans(sig),parse_controlled_connections(net))["J"]["cycle_s"],90)
            net.write_text('<net><connection tl="J" linkIndex="0"/><connection tl="J" linkIndex="2"/></net>')
            with self.assertRaises(ValueError):
                validate_crosswalk(parse_plans(sig),parse_controlled_connections(net))
    def test_nonpositive_phase_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"signal.xml"
            path.write_text('<add><tlLogic id="J"><phase duration="0" state="G"/></tlLogic></add>')
            with self.assertRaises(ValueError):
                parse_plans(path)

if __name__ == "__main__":
    unittest.main()
