#!/bin/bash

show_help() {
    echo "Usage: bash $0 -i input_dir -o output_dir"
    echo "       bash $0 -h"
    echo
    echo "Options:"
    echo "  -i   Input directory containing the .fna files"
    echo "  -o   Output directory where the reformatted files will be saved"
    echo "  -h   Display this help message"
}

while getopts "hi:o:" opt; do
    case $opt in
        h)
            show_help
            exit 0
            ;;
        i)
            input_dir=$OPTARG
            ;;
        o)
            output_dir=$OPTARG
            ;;
        \?)
            show_help
            exit 1
            ;;
    esac
done

# Check if input_dir is specified
if [ -z "$input_dir" ]; then
    echo "Error: Input directory not specified."
    show_help
    exit 1
fi

# Create output directory if it doesn't exist
if [ -z "$output_dir" ]; then
    output_dir="./output"
fi
mkdir -p "$output_dir"

# Process each .fasta file in the input directory
for file in "$input_dir"/*.fna; do
    filename=$(basename "$file")
    output_file="$output_dir/$filename"
    
    # Reformat the fasta file
    awk '/^>/ {gsub(/[.,'\''\"]/,"_",$0)} {print}' "$file" > "$output_file"
done

echo "Reformatting completed. Reformatted files are saved in $output_dir."
