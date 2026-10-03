# Concatenated Ribosomal Sequence Marker gene (CRiSM)

> [!WARNING]
> CRiSM is a prototype. The source installation below is the documented route; a stable PyPI release is not assumed.

CRiSM (Concatenated Ribosomal Sequence Marker gene) is designed for phylogenetic analysis using concatenated ribosomal protein marker genes, primarily focusing on 16 specific ribosomal proteins in CPR (Candidate Phyla Radiation) genomes. While it is tailored for CPR genomes, CRiSM is flexible enough to accommodate any prokaryotic genomes and user-specified marker genes.

## Features

- **Targeted Analysis**: Specializes in analyzing CPR genomes but is also applicable to other prokaryotic genomes.
- **Flexibility**: Supports user-specified marker genes, allowing for customized phylogenetic studies.
- **Ease of Use**: Provides a simple command-line interface for running comprehensive phylogenetic analyses.

## System Requirements

CRiSM is designed to run on Unix-like operating systems (Linux, macOS). It requires Python 3.6 or newer.

## Installation

### Install Python and Conda

If you do not have Python or Conda installed, we recommend installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html) as it includes both and allows for easy setup of environments.

### Setting up a Conda Environment

Create a new Conda environment to manage the dependencies for CRiSM separately:

```bash
conda create -n crism python=3.8
conda activate crism
```

### Install CRiSM

Install from this repository (in your activated environment):

```bash
git clone https://github.com/DaikiKumakura/CRiSM.git
cd CRiSM
python -m pip install .
```

### Install External Bioinformatics Tools

Install the required bioinformatics tools using Conda from the Bioconda channel:

```bash
conda install -c bioconda -y prodigal hmmer muscle trimal iqtree biopython
```

This will install Prodigal, HMMER, MUSCLE, TrimAl, IQ-TREE2, and biopython which are essential for running the CRiSM pipeline.

## Usage

To run CRiSM, use the following command format:

```bash
crism -i <input_dir> -o <output_dir> --db <markergene.hmm> --list <markergene_list.txt> -t <threads>
```

### Command Line Options

- `-i`, `--input`: Specify the input directory containing the genome files (fna or fasta file).
- `-o`, `--output`: Specify the output directory for the analysis results.
- `--db`: Path to the HMM database file.
- `--list`: Path to the file listing the marker genes.
- `-t`, `--threads`: Number of threads to use for the analysis.

## DESCRIPTION

CRiSM performs the following analysis steps:

1. **Reformat**: Replaces characters such as spaces, ".", ",", ":", ";" in fna file names and read names with "_".
2. **Find**: Annotates using Prodigal and searches with HMMER at E=1E-5.
3. **Extract**: Extracts marker sequences for organisms containing all specified markers from the database input.
4. **Combine**: Combines marker sequences for each marker type.
5. **Reformat**: Same as step 1.
6. **Alignment & Trimming**: Aligns with MUSCLE using "-super5" and trims with TrimAl using "-automated1".
7. **Concatenation**: Concatenates trimmed marker sequences for each organism.
8. **Make tree**: Performs phylogenetic analysis using IQ-TREE2 with "-st AA -bb 1000 -m LG+G4+FO+I".　

## CITATION

If you use CRiSM in your research, please cite the following:

Kumakura, D. (2024). CRiSM: Concatenated Ribosomal Sequence Marker gene package for phylogenetic analysis. GitHub repository. Available at [https://github.com/DaikiKumakura/CRiSM](https://github.com/DaikiKumakura/CRiSM).

## Contributing

Contributions to CRiSM are welcome! If you have suggestions for improvements or new features, please fork the repository, make your changes, and submit a pull request.

## License

CRiSM is released under the MIT License. See the LICENSE file in the project repository for more details.

## Minimal validation

`python -m unittest -q` checks FASTA reformatting from another working directory and failure propagation. These checks do not validate the complete phylogenetic workflow or its scientific results. External tools listed above are still required.
