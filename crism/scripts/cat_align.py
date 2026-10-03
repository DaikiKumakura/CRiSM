#!/usr/bin/env python

from Bio import SeqIO
import os
import argparse
from collections import defaultdict

def concat_alignments(input_dir, output_dir, marker_genes_file):
    # Read the marker genes list
    with open(marker_genes_file, "r") as f:
        marker_genes = [line.strip() for line in f if line.strip()]
    if not marker_genes or len(set(marker_genes)) != len(marker_genes):
        raise ValueError("Marker list must contain unique, nonempty names")

    # Dictionary to hold concatenated sequences
    concatenated_sequences = defaultdict(str)
    bacteria_names = None

    # Process each marker gene in the specified order
    for gene in marker_genes:
        file_name = f"Dataset1_{gene}.trimmed.aln"
        file_path = os.path.join(input_dir, file_name)
        
        if not os.path.exists(file_path):
            raise ValueError(f"Required marker alignment is missing: {file_path}")
        
        # Read each sequence in the file
        with open(file_path) as handle:
            records = list(SeqIO.parse(handle, "fasta"))
        ids = [record.id for record in records]
        if not ids or len(ids) != len(set(ids)):
            raise ValueError(f"Empty alignment or duplicate sample IDs: {file_path}")
        if len({len(record.seq) for record in records}) != 1 or not len(records[0].seq):
            raise ValueError(f"Marker alignment must have equal, positive sequence lengths: {file_path}")
        if bacteria_names is None:
            bacteria_names = set(ids)
        elif bacteria_names != set(ids):
            raise ValueError(f"Sample IDs differ across marker alignments: {file_path}")
        for record in records:
            concatenated_sequences[record.id] += str(record.seq)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "Dataset1_cat.trimmed.aln")
    
    # Write the concatenated sequences to the output file
    with open(output_file, "w") as output_handle:
        for bacteria in sorted(bacteria_names):
            output_handle.write(f">{bacteria}\n{concatenated_sequences[bacteria]}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Concatenate sequences for the same bacteria from multiple .trimmed.aln files based on the order of marker genes in the provided list.")
    parser.add_argument("-i", "--input_dir", required=True, help="Directory containing .trimmed.aln files.")
    parser.add_argument("-o", "--output_dir", required=True, help="Directory to store the output concatenated file.")
    parser.add_argument("--list", required=True, help="Specify the file containing the list of markers.")
    
    args = parser.parse_args()
    
    concat_alignments(args.input_dir, args.output_dir, args.list)
