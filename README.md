# CRiSM

**Concatenated Ribosomal Sequence Marker gene: a phylogenetic tree from
genome FASTA files with one command, using concatenated marker genes.**

## Installation

CRiSM runs on Linux and macOS with Python 3.6 or later. A Conda environment
keeps it and its tools together:

```bash
conda create -n crism python=3.8
conda activate crism
conda install -c bioconda -y prodigal hmmer muscle trimal iqtree biopython

git clone https://github.com/DaikiKumakura/CRiSM.git
cd CRiSM
python -m pip install .
```

## Quick start

```bash
crism -i genomes/ -o output/ \
  --db crism/data/marker_and_list/rp16_marker.hmm \
  --list crism/data/marker_and_list/rp16_marker_list.txt \
  -t 8
```

**What goes in.** A folder with one nucleotide FASTA file per genome (`.fna` or `.fasta`); no example genomes are
bundled, so use any prokaryotic genomes you have, for example from NCBI. **What comes out.** One numbered folder
per step in `output/` (`01_reformat_fna` to `08_tree`). The tree is
`output/08_tree/Dataset1_cat.trimmed.treefile` (Newick, with IQ-TREE's 1000 ultrafast bootstrap supports); the
concatenated alignment it was built from is in `output/07_cat/`. The run ends with the line
`Pipeline completed successfully.` These names come from the pipeline code; the complete run has not been
validated on real genomes (see [Validation and limitations](#validation-and-limitations)).

## Documentation

[Usage guide](https://github.com/DaikiKumakura/CRiSM/blob/main/README-GUIDE.md)

## Validation and limitations

- **Validation:** Ran unit tests for FASTA reformatting, concatenation and failure propagation; checked an isolated wheel installation.
- **Results:** The wheel exposed the CLI and bundled marker files, and the local checks completed.
- **Limitations:** End-to-end marker discovery, alignment and tree inference on real genomes remain unverified.
- **Reproduction:** [README-GUIDE.md](https://github.com/DaikiKumakura/CRiSM/blob/main/README-GUIDE.md).

## Citation

Kumakura, D. (2024). *CRiSM: Concatenated Ribosomal Sequence Marker gene* [Software]. [GitHub repository](https://github.com/DaikiKumakura/CRiSM).

Citation metadata: [CITATION.cff](CITATION.cff).

Also cite Prodigal, HMMER, MUSCLE, trimAl and IQ-TREE as applicable.

## License

This project is licensed under MIT. See [LICENSE](LICENSE) for the license terms.
