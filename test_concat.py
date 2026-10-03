"""Check concatenation against small alignments and malformed inputs."""
from pathlib import Path
import tempfile
import unittest
from crism.scripts.cat_align import concat_alignments


class ConcatenationTests(unittest.TestCase):
    def run_case(self, first, second, expected=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'markers.txt').write_text('m1\nm2\n')
            (root/'Dataset1_m1.trimmed.aln').write_text(first)
            if second is not None:
                (root/'Dataset1_m2.trimmed.aln').write_text(second)
            args = str(root), str(root/'out'), str(root/'markers.txt')
            if expected is None:
                with self.assertRaises(ValueError):
                    concat_alignments(*args)
                self.assertFalse((root/'out').exists())
            else:
                concat_alignments(*args)
                self.assertEqual((root/'out/Dataset1_cat.trimmed.aln').read_text(), expected)

    def test_order_and_gaps(self):
        self.run_case('>b\nA-\n>a\nAC\n', '>a\nGGG\n>b\nG-G\n', '>a\nACGGG\n>b\nA-G-G\n')

    def test_missing_marker(self):
        self.run_case('>a\nAA\n', None)

    def test_unequal_lengths(self):
        self.run_case('>a\nAA\n>b\nA\n', '>a\nGG\n>b\nGG\n')

    def test_different_samples(self):
        self.run_case('>a\nAA\n', '>b\nGG\n')

    def test_duplicate_sample(self):
        self.run_case('>a\nAA\n>a\nCC\n', '>a\nGG\n')

    def test_empty_alignment(self):
        self.run_case('', '>a\nGG\n')


if __name__ == '__main__':
    unittest.main()
