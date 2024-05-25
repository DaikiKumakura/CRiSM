#!/usr/bin/python

import os
import argparse
import glob

def usage():
    help_message = """
Usage: python combine.py -i input_dir -o output_dir --list list_file.txt
  -i input_dir        Specify the input directory containing the files.
  -o output_dir       Specify the output directory to save the results.
  --list list_file    Specify the file containing the list of markers.
"""
    print(help_message)

def main(input_dir, output_dir, list_file):
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory {input_dir} does not exist.")
        usage()
        exit(1)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.isfile(list_file):
        print(f"Error: List file {list_file} does not exist.")
        usage()
        exit(1)

    with open(list_file, 'r') as lf:
        markers = lf.read().splitlines()

    for marker in markers:
        output_file_path = os.path.join(output_dir, f"Dataset1_{marker}.faa")
        with open(output_file_path, 'w') as output_file:
            for file in glob.glob(os.path.join(input_dir, f"*_{marker}.faa")):
                with open(file, 'r') as input_file:
                    output_file.write(input_file.read())

    print(f"Processing completed. Results are saved in {output_dir}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine specific .faa files based on a list of markers.")
    parser.add_argument('-i', '--input_dir', required=True, help="Specify the input directory containing the files.")
    parser.add_argument('-o', '--output_dir', required=True, help="Specify the output directory to save the results.")
    parser.add_argument('--list', required=True, help="Specify the file containing the list of markers.")

    args = parser.parse_args()

    main(args.input_dir, args.output_dir, args.list)
