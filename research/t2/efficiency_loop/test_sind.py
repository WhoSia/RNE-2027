from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from sind_signal import audit


class SinD(TestCase):
    def test_rejects_an_lfs_pointer_in_place_of_csv(self):
        with TemporaryDirectory() as directory:
            file = Path(directory) / "traffic.csv"
            file.write_text("version https://git-lfs.github.com/spec/v1\n")
            with self.assertRaisesRegex(ValueError,"Git LFS object"):
                audit(file,"tianjin")
