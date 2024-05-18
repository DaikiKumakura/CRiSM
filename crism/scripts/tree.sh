#!/bin/bash

# 05_tree.sh

# Display help message
function show_help() {
    echo "Usage: bash 05_tree.sh -i input_dir -o output_dir -r list_file.txt"
    echo ""
    echo "Options:"
    echo "  -i input_dir    Directory containing trimmed alignment files"
    echo "  -o output_dir   Directory to store output files (will be created if it doesn't exist)"
    echo "  -r list_file    File containing list of gene names"
    echo "  -h              Display this help message"
}

# Parse command line arguments
while getopts ":i:o:r:h" opt; do
    case ${opt} in
        i ) input_dir=$OPTARG ;;
        o ) output_dir=$OPTARG ;;
        r ) list_file=$OPTARG ;;
        h ) show_help; exit 0 ;;
        \? ) echo "Invalid option: -$OPTARG" 1>&2; show_help; exit 1 ;;
        : ) echo "Invalid option: -$OPTARG requires an argument" 1>&2; show_help; exit 1 ;;
    esac
done

# Check for mandatory arguments
if [ -z "$input_dir" ] || [ -z "$output_dir" ] || [ -z "$list_file" ]; then
    echo "Error: Missing required arguments" 1>&2
    show_help
    exit 1
fi

# Create output directories if they don't exist
mkdir -p "$output_dir/single"
mkdir -p "$output_dir/concat"

# Perform phylogenetic analysis for each gene in the list
while read -r gene; do
    for file in "$input_dir"/*_"$gene".trimmed.aln; do
        sample_name=$(basename "$file" | cut -d'_' -f1)
        iqtree2 -s "$file" --prefix "$sample_name"_"$gene" -m MFP -alrt 1000 -bb 1000 -T AUTO
        mv "${sample_name}_${gene}.uniqueseq.phy" "${sample_name}_${gene}.treefile" "${sample_name}_${gene}.splits.nex" "${sample_name}_${gene}.model.gz" "${sample_name}_${gene}.mldist" "${sample_name}_${gene}.log" "${sample_name}_${gene}.iqtree" "${sample_name}_${gene}.contree" "${sample_name}_${gene}.ckp.gz" "${sample_name}_${gene}.bionj" "${sample_name}_${gene}.best_scheme.nex" "${sample_name}_${gene}.best_scheme" "${sample_name}_${gene}.best_model.nex" "$output_dir/single/"
    done
done < "$list_file"

# Perform phylogenetic analysis for concatenated genes
iqtree2 -p "$input_dir" --prefix "concat" -m MFP -alrt 1000 -bb 1000 -T AUTO
mv "concat.treefile" "concat.splits.nex" "concat.model.gz" "concat.mldist" "concat.log" "concat.iqtree" "concat.contree" "concat.ckp.gz" "concat.bionj" "concat.best_scheme.nex" "concat.best_scheme" "concat.best_model.nex" "$output_dir/concat/"
