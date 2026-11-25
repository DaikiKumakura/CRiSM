# CRiSM guide

**Concatenated Ribosomal Sequence Marker gene: a phylogenetic tree from
genome FASTA files with one command, using concatenated marker genes.**

> [!WARNING]
> CRiSM is a prototype. Installation from source is the documented route, and
> the complete workflow with the external tools has not been validated (see
> [Status](#status)).

CRiSM finds marker genes in prokaryotic genomes, extracts them for the genomes
that contain all of them, aligns and trims each marker, concatenates the
alignments and infers a maximum-likelihood tree. It was designed for the 16
ribosomal proteins used for CPR (Candidate Phyla Radiation) genomes, and works
with any prokaryotic genomes and with your own marker sets.

- **One command** from a folder of genomes to a tree.
- **Marker sets included:** 16 and 15 ribosomal proteins, RpS3, 16S rRNA,
  GyrA and RecA, as HMM profiles with their marker lists.
- **Strict concatenation:** a genome is used only when it has every listed
  marker, and inconsistent alignments stop the run before any output is
  written.

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

The pipeline calls `prodigal`, `hmmsearch`, `cut`, `muscle`, `trimal` and
`iqtree2` by these names, so they must be on `PATH`:

- MUSCLE must be version 5 (the `-super5` option); MUSCLE 3 does not work.
- Check `iqtree2 --version`: the Conda package name alone does not guarantee
  this executable.
- `cut` comes with the Unix environment.

<a id="usage"></a>

## Quick start

```bash
crism -i genomes/ -o output/ \
  --db crism/data/marker_and_list/rp16_marker.hmm \
  --list crism/data/marker_and_list/rp16_marker_list.txt \
  -t 8
```

| Option | Meaning |
|---|---|
| `-i`, `--input` | folder with the genome files (`.fna` or `.fasta`) |
| `-o`, `--output` | folder for the results |
| `--db` | HMM profile file of the markers |
| `--list` | file listing the marker names to use |
| `-t`, `--threads` | number of threads |

## Documentation

[Workflow](#workflow) · [Marker sets](#marker-sets)

## Workflow

```text
   genomes/*.fna
        │  reformat      clean file and sequence names
        │  find          genes with Prodigal, markers with HMMER (E = 1e-5)
        │  extract       genomes that contain every listed marker
        │  combine       one FASTA per marker
        │  align, trim   MUSCLE (-super5), trimAl (-automated1)
        │  concatenate   one supermatrix row per genome
        │  tree          IQ-TREE 2 (-st AA -bb 1000 -m LG+G4+FO+I)
        ▼
   output/  marker alignments, supermatrix, tree
```

## Marker sets

The files are in [`crism/data/marker_and_list/`](crism/data/marker_and_list/);
each set is an `.hmm` file and a `_list.txt` file.

| Set | Files |
|---|---|
| 16 ribosomal proteins | `rp16_marker.hmm`, `rp16_marker_list.txt` |
| 15 ribosomal proteins | `rp15_marker.hmm`, `rp15_marker_list.txt` |
| Ribosomal protein S3 | `rps3_marker.hmm`, `rps3_marker_list.txt` |
| 16S rRNA | `16SrRNA_marker.hmm`, `16SrRNA_marker_list.txt` |
| GyrA | `gyrA_marker.hmm`, `gyrA_marker_list.txt` |
| RecA | `recA_marker.hmm`, `recA_marker_list.txt` |

For your own markers, give an HMM file with profiles for them and a list of
their names.

<a id="status"></a>

## Validation and limitations

- `python -m unittest -q` checks FASTA reformatting from another working
  directory, concatenation rules and failure propagation; these checks run on
  GitHub Actions for every push. They do not need the external tools.
- On 2026-10-03, the wheel was built and installed into an isolated folder;
  the command-line help, FASTA reformatting and the bundled HMM files were
  checked.
- Marker discovery, alignment and tree inference on real genomes have **not**
  been run in these checks, so the complete workflow and its scientific
  results are not validated.

## Citation

Kumakura, D. (2024). *CRiSM: Concatenated Ribosomal Sequence Marker gene* [Software]. [GitHub repository](https://github.com/DaikiKumakura/CRiSM).

Citation metadata: [CITATION.cff](CITATION.cff).

Also cite Prodigal, HMMER, MUSCLE, trimAl and IQ-TREE as applicable.

## License

This project is licensed under MIT. See [LICENSE](LICENSE) for the license terms.
