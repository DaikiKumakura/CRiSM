import os
import sys
import shutil
from collections import defaultdict

def main():
    args = parse_arguments()
    
    # Make sure output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Load marker genes from file
    with open(args.markers_file, 'r') as file:
        required_markers = {line.strip() for line in file.readlines()}
    
    # Process each file in the input directory
    samples = defaultdict(set)
    for filename in os.listdir(args.input_dir):
        sample_name, marker = os.path.splitext(filename)[0].rsplit('_', 1)
        samples[sample_name].add(marker)
    
    # List to keep track of samples with all required markers
    full_markergenes_samples = []

    # Copy files for samples that contain all required markers
    for sample, markers in samples.items():
        if markers >= required_markers:
            full_markergenes_samples.append(sample)
            for marker in markers:
                source_file = os.path.join(args.input_dir, f"{sample}_{marker}.faa")
                dest_file = os.path.join(args.output_dir, f"{sample}_{marker}.faa")
                shutil.copy2(source_file, dest_file)
    
    # Save the list of samples with all markers to a file
    with open(os.path.join(args.output_dir, "0_full_markergenes_genoms.txt"), 'w') as file:
        for sample in full_markergenes_samples:
            file.write(f"{sample}\n")

def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(description='Extract and copy gene files based on marker genes.')
    parser.add_argument('-i', '--input_dir', required=True, help='Directory containing gene files')
    parser.add_argument('-o', '--output_dir', required=True, help='Directory where matched gene files will be copied')
    parser.add_argument('-r', '--markers_file', required=True, help='File containing list of required marker genes')
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    return parser.parse_args()

if __name__ == '__main__':
    main()
