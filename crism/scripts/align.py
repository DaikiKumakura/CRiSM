#!/usr/bin/env python

import os
import glob
import argparse
import subprocess

def show_help():
    help_message = """
Usage: python align.py -i input_dir -o output_dir -t threads

Options:
  -i    Input directory containing .faa files
  -o    Output directory for alignment and trimmed files
  -t    Number of threads to use for muscle
  -h    Show this help message
"""
    print(help_message)

def main(input_dir, output_dir, threads):
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory {input_dir} does not exist.")
        show_help()
        exit(1)
    
    os.makedirs(os.path.join(output_dir, "aln"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "trim"), exist_ok=True)

    for faa_file in glob.glob(os.path.join(input_dir, "*.faa")):
        base_name = os.path.basename(faa_file).rsplit('.', 1)[0]
        
        aln_output = os.path.join(output_dir, "aln", f"{base_name}.aln")
        trim_output = os.path.join(output_dir, "trim", f"{base_name}.trimmed.aln")

        muscle_cmd = ["muscle", "-super5", faa_file, "-output", aln_output, "-threads", str(threads)]
        print(f"Running muscle: {' '.join(muscle_cmd)}")
        subprocess.call(muscle_cmd)
        
        trimal_cmd = ["trimal", "-automated1", "-in", aln_output, "-out", trim_output]
        print(f"Running trimal: {' '.join(trimal_cmd)}")
        subprocess.call(trimal_cmd)
    
    print("Processing completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run muscle and trimal on .faa files in a directory.")
    parser.add_argument('-i', '--input_dir', required=True, help="Input directory containing .faa files")
    parser.add_argument('-o', '--output_dir', required=True, help="Output directory for alignment and trimmed files")
    parser.add_argument('-t', '--threads', required=True, type=int, help="Number of threads to use for muscle")
    parser.add_argument('-h', '--help', action='store_true', help="Show this help message")

    args = parser.parse_args()

    if args.help:
        show_help()
        exit(0)

    main(args.input_dir, args.output_dir, args.threads)
