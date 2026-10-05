"""Prevent data loss when FASTA filenames are normalized."""
from pathlib import Path
import tempfile
import unittest

from crism.scripts.reformat import main


class ReformatSafetyTests(unittest.TestCase):
    def test_colliding_names_stop_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inputs = root / "input"
            inputs.mkdir()
            for name in ("sample.a.fna", "sample_a.fna"):
                (inputs / name).write_text(">sample\nACGT\n")
            output = root / "output"
            with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
                main(str(inputs), str(output))
            self.assertFalse(output.exists())

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inputs = root / "input"
            output = root / "output"
            inputs.mkdir()
            output.mkdir()
            (inputs / "sample.fna").write_text(">new\nACGT\n")
            existing = output / "sample.fna"
            existing.write_text(">original\nAAAA\n")
            with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
                main(str(inputs), str(output))
            self.assertEqual(existing.read_text(), ">original\nAAAA\n")
