#!/usr/bin/env python

from Bio import SeqIO
import os
import argparse
from collections import defaultdict

def concat_alignments(input_dir, output_dir, marker_genes_file):
    # Read the marker genes list
    with open(marker_genes_file, "r") as f:
        marker_genes = [line.strip() for line in f]

    # Dictionary to hold concatenated sequences
    concatenated_sequences = defaultdict(str)
    bacteria_names = set()

    # Process each marker gene in the specified order
    for gene in marker_genes:
        file_name = f"Dataset1_{gene}.trimmed.aln"
        file_path = os.path.join(input_dir, file_name)
        
        if not os.path.exists(file_path):
            print(f"Warning: {file_path} does not exist and will be skipped.")
            continue
        
        # Read each sequence in the file
        for record in SeqIO.parse(file_path, "fasta"):
            bacteria_names.add(record.id)
            concatenated_sequences[record.id] += str(record.seq)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "Dataset1_cat.trimmed.aln")
    
    # Write the concatenated sequences to the output file
    with open(output_file, "w") as output_handle:
        for bacteria in bacteria_names:
            output_handle.write(f">{bacteria}\n{concatenated_sequences[bacteria]}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Concatenate sequences for the same bacteria from multiple .trimmed.aln files based on the order of marker genes in the provided list.")
    parser.add_argument("-i", "--input_dir", required=True, help="Directory containing .trimmed.aln files.")
    parser.add_argument("-o", "--output_dir", required=True, help="Directory to store the output concatenated file.")
    parser.add_argument("--list", "--list_file", required=True, help="Specify the file containing the list of markers.")
    
    args = parser.parse_args()
    
    concat_alignments(args.input_dir, args.output_dir, args.marker_genes)
