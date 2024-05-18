# Concatenated Ribosomal Sequence Marker gene (CRiSM)

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

Install CRiSM directly from PyPI:

```bash
pip install crism
```

### Install External Bioinformatics Tools

Install the required bioinformatics tools using Conda from the Bioconda channel:

```bash
conda install -c bioconda prodigal hmmer muscle trimal iqtree2
```

This will install Prodigal, HMMER, MUSCLE, TrimAl, and IQ-TREE2, which are essential for running the CRiSM pipeline.

## Usage

To run CRiSM, use the following command format:

```bash
crism -i <input_dir> -o <output_dir> --hmm <markergenes.hmm> --list <markergenes_list.txt> -t <threads>
```

### Command Line Options

- `-i`, `--input`: Specify the input directory containing the genome files.
- `-o`, `--output`: Specify the output directory for the analysis results.
- `--hmm`: Path to the HMM database file.
- `--list`: Path to the file listing the marker genes.
- `-t`, `--threads`: Number of threads to use for the analysis.

## Contributing

Contributions to CRiSM are welcome! If you have suggestions for improvements or new features, please fork the repository, make your changes, and submit a pull request.

## License

CRiSM is released under the MIT License. See the LICENSE file in the project repository for more details.
