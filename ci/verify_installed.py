"""Check the installed wheel, without importing the repository checkout."""
from pathlib import Path
import tempfile

import crism
from crism.run_pipeline import run_step


def main():
    package = Path(crism.__file__).resolve().parent
    checkout = Path(__file__).resolve().parents[1]
    if package == checkout / "crism":
        raise RuntimeError("Expected an installed package, not the checkout")

    marker_dir = package / "data" / "marker_and_list"
    for marker in ("16SrRNA", "gyrA", "recA", "rp15", "rp16", "rps3"):
        for suffix in ("_marker.hmm", "_marker_list.txt"):
            path = marker_dir / (marker + suffix)
            if not path.is_file() or not path.stat().st_size:
                raise RuntimeError("Missing or empty installed resource: " + str(path))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        inputs = root / "input"
        inputs.mkdir()
        (inputs / "sample.fna").write_text(">sample name\nACGT\n", encoding="utf-8")
        output = root / "output"
        run_step("reformat.py", "-i", str(inputs), "-o", str(output))
        actual = (output / "sample.fna").read_text(encoding="utf-8")
        if actual != ">sample_name\nACGT\n":
            raise RuntimeError("Installed reformat script returned unexpected FASTA")
    print("Installed wheel: 12 marker resources and bundled script verified")


if __name__ == "__main__":
    main()
