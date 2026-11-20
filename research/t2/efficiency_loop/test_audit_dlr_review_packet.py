from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from zipfile import ZipFile
import json

from audit_dlr_reviews import review_scope


class ReviewPacketTests(TestCase):
    def test_embedded_scope_and_sheet_digest_are_used_without_extraction(self):
        with TemporaryDirectory() as directory:
            path = Path(directory)/"review.zip"
            manifest = {"cases": [{"case": "K047-01"}],
                        "input_hashes": {"dlr_review_sheet.csv": "7"*64}}
            with ZipFile(path, "w") as packet:
                packet.writestr("K047-review.html",
                                '<script id="observations" type="application/json">'
                                + json.dumps(manifest) + '</script>')
            self.assertEqual(review_scope(path), ({"K047-01"}, "7"*64))

    def test_missing_manifest_is_rejected(self):
        with TemporaryDirectory() as directory:
            path = Path(directory)/"review.zip"
            with ZipFile(path, "w") as packet:
                packet.writestr("K047-review.html", "<html></html>")
            with self.assertRaisesRegex(ValueError, "manifest"):
                review_scope(path)
