#!/bin/bash

# Function to display help
show_help() {
    echo "Usage: $0 -i input_dir -o output_dir -t threads"
    echo ""
    echo "Options:"
    echo "  -i    Input directory containing .faa files"
    echo "  -o    Output directory for alignment and trimmed files"
    echo "  -t    Number of threads to use for muscle"
    echo "  -h    Show this help message"
}

# Parse command line arguments
while getopts "hi:o:t:" opt; do
    case ${opt} in
        h )
            show_help
            exit 0
            ;;
        i )
            input_dir=$OPTARG
            ;;
        o )
            output_dir=$OPTARG
            ;;
        t )
            threads=$OPTARG
            ;;
        \? )
            show_help
            exit 1
            ;;
    esac
done

# Check if required arguments are provided
if [ -z "$input_dir" ] || [ -z "$output_dir" ] || [ -z "$threads" ]; then
    echo "Error: Missing required arguments"
    show_help
    exit 1
fi

# Create output directories if they don't exist
mkdir -p "$output_dir/aln"
mkdir -p "$output_dir/trim"

# Process each .faa file in the input directory
for faa_file in "$input_dir"/*.faa; do
    # Extract base name
    base_name=$(basename "$faa_file" .faa)

    # Run muscle
    muscle -super5 "$faa_file" -output "$output_dir/aln/${base_name}.aln" -threads "$threads"

    # Run trimal
    trimal -automated1 -in "$output_dir/aln/${base_name}.aln" -out "$output_dir/trim/${base_name}.trimmed.aln"
done
