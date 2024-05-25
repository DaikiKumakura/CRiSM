#!/usr/bin/python

import os
import sys
import argparse
import shutil

def show_help():
    help_message = """
Usage: python reformat.py -i input_dir -o output_dir
       python reformat.py -h

Options:
  -i   Input directory containing the .fna or .faa files
  -o   Output directory where the reformatted files will be saved
  -h   Display this help message
"""
    print(help_message)

def reformat_fasta(file_path, output_path):
    with open(file_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            if line.startswith('>'):
                line = line.replace(' ', '_').replace('.', '_').replace(',', '_').replace(';', '_').replace(':', '_')
            outfile.write(line)

def main(input_dir, output_dir):
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory {input_dir} does not exist.")
        sys.exit(1)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for ext in ('*.fna', '*.faa'):
        for file in glob.glob(os.path.join(input_dir, ext)):
            filename = os.path.basename(file)
            filename_without_ext = os.path.splitext(filename)[0]
            new_filename = filename_without_ext.replace('.', '_') + os.path.splitext(filename)[1]
            output_file = os.path.join(output_dir, new_filename)
            reformat_fasta(file, output_file)
    
    print(f"Reformatting completed. Reformatted files are saved in {output_dir}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reformat .fna and .faa files.")
    parser.add_argument('-i', '--input_dir', required=True, help="Input directory containing the .fna or .faa files")
    parser.add_argument('-o', '--output_dir', required=False, default="./output", help="Output directory where the reformatted files will be saved")
    parser.add_argument('-h', '--help', action='store_true', help="Display this help message")

    args = parser.parse_args()

    if args.help:
        show_help()
        sys.exit(0)

    main(args.input_dir, args.output_dir)
