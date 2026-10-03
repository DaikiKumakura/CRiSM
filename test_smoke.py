"""Small regression checks; no external bioinformatics tools or data required."""
import contextlib
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from crism.run_pipeline import run_pipeline, run_step

class SmokeTests(unittest.TestCase):
    def test_installed_script_from_other_directory(self):
        import os
        before=Path.cwd()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'input').mkdir()
            (root/'input'/'sample.fna').write_text('>a b\nACGT\n')
            try:
                os.chdir(root)
                run_step('reformat.py','-i','input','-o','output')
                self.assertEqual((root/'output/sample.fna').read_text(),'>a_b\nACGT\n')
            finally: os.chdir(before)

    def test_failed_first_stage_stops_pipeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'result'
            with self.assertRaises(subprocess.CalledProcessError):
                run_pipeline(str(Path(tmp)/'missing'),str(output),'unused.hmm','unused.txt',1)
            self.assertFalse(output.exists())

    def test_external_alignment_failure_stops_before_trimming(self):
        from crism.scripts.align import main
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'sample.faa').write_text('>a\nAAA\n')
            with patch('crism.scripts.align.subprocess.run',side_effect=subprocess.CalledProcessError(1,'muscle')) as call:
                with self.assertRaises(subprocess.CalledProcessError):main(tmp,str(root/'out'),1)
                self.assertEqual(call.call_count,1)

if __name__=='__main__':unittest.main()
