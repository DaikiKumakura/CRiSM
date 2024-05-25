#!/usr/bin/python

import sys
import os
import glob
import argparse
import subprocess
from Bio import SeqIO

def main():
    parser = argparse.ArgumentParser(description="Identify marker genes in protein sequences of genomes.")
    parser.add_argument('-i', '--input_dir', required=True, help="Directory containing target files with '.fna' extension.")
    parser.add_argument('-o', '--output_dir', required=True, help="Directory to save output files.")
    parser.add_argument('--db', required=True, help='HMM file of markers. Markers should have a descriptive ID name.')
    parser.add_argument('-E', help='Set E-Value to be used in hmmsearch. Default: 1E-5', default='1E-5')
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    Evalue = args.E
    markerdb = args.db

    # Create output subdirectories if they do not exist
    faa_dir = os.path.join(output_dir, "faa")
    tbl_dir = os.path.join(output_dir, "tbl")
    marker_dir = os.path.join(output_dir, "marker")
    for directory in [faa_dir, tbl_dir, marker_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    input_fasta = glob.glob(os.path.join(input_dir, "*.fna"))
    for in_fna in input_fasta:
        sample_name = os.path.basename(in_fna).rsplit('.', 1)[0]
        faa_path = os.path.join(faa_dir, f"{sample_name}.faa")
        temp_faa_path = os.path.join(output_dir, "temp1.orfs.faa")
        temp_txt_path = os.path.join(output_dir, "temp1.txt")
        prodigal_cmd = ["prodigal", "-a", temp_faa_path, "-i", in_fna, "-m", "-o", temp_txt_path, "-p", "meta", "-q"]
        print(f"Running Prodigal: {' '.join(prodigal_cmd)}")
        subprocess.call(prodigal_cmd)
        if os.path.exists(temp_faa_path):
            with open(faa_path, "w") as outfile:
                subprocess.call(["cut", "-f1", "-d", " ", temp_faa_path], stdout=outfile)
            os.remove(temp_faa_path)
            os.remove(temp_txt_path)
            print(f"Prodigal created {faa_path}")
        else:
            print(f"Prodigal failed to create {temp_faa_path}")

    input_proteins = glob.glob(os.path.join(faa_dir, "*.faa"))
    if not input_proteins:
        print("No .faa files found. Prodigal may not have run correctly or input files may be missing.")
        sys.exit(1)

    marker_list = []
    with open(markerdb, "r") as marker_file:
        for line in marker_file:
            line = line.rstrip()
            if line.startswith("NAME"):
                marker_list.append(line.split()[1])
    num_markers = len(marker_list)
    print(f"Number of markers: {num_markers}")

    for in_faa in input_proteins:
        sample_name = os.path.basename(in_faa).rsplit('.', 1)[0]
        log_file = os.path.join(tbl_dir, f"{sample_name}_hmmsearch-log.txt")
        tbl_file = os.path.join(tbl_dir, f"{sample_name}.ribomarkers.tbl")
        with open(log_file, "w") as hmmer_log:
            hmmsearch_cmd = ["hmmsearch", "--cut_tc", "--tblout", tbl_file, "--notextw", markerdb, in_faa]
            print(f"Running hmmsearch: {' '.join(hmmsearch_cmd)}")
            subprocess.call(hmmsearch_cmd, stdout=hmmer_log)
            if os.path.exists(tbl_file):
                print(f"hmmsearch created {tbl_file}")
            else:
                print(f"hmmsearch failed to create {tbl_file}")

    genome_marker_count = {}
    hmm_names = glob.glob(os.path.join(tbl_dir, "*.ribomarkers.tbl"))
    if not hmm_names:
        print("No .tbl files found. hmmsearch may not have run correctly.")
        sys.exit(1)

    for active_hmm in hmm_names:
        sample_name = os.path.basename(active_hmm).rsplit('.', 2)[0]
        if os.stat(active_hmm).st_size < 1000:
            genome_marker_count[sample_name] = {}
        with open(active_hmm, "r") as hmm_file:
            for line in hmm_file:
                line = line.rstrip()
                if not line.startswith("#"):
                    line_info = line.split()
                    try:
                        if line_info[2] in genome_marker_count[sample_name]:
                            if line_info[0] != genome_marker_count[sample_name][line_info[2]]:
                                genome_marker_count[sample_name][line_info[2]] = "empty"
                        else:
                            genome_marker_count[sample_name][line_info[2]] = line_info[0]
                    except KeyError:
                        genome_marker_count[sample_name] = {}
                        genome_marker_count[sample_name][line_info[2]] = line_info[0]

    for genome in genome_marker_count:
        remove = [i for i in genome_marker_count[genome] if genome_marker_count[genome][i] == "empty"]
        for x in remove:
            del genome_marker_count[genome][x]
        if len(genome_marker_count[genome]) >= 1:
            reverse_gene_info = {v: k for k, v in genome_marker_count[genome].items()}
            faa_path = os.path.join(faa_dir, f"{genome}.faa")
            if not os.path.exists(faa_path):
                print(f"FASTA file for {genome} not found.")
                continue
            with open(faa_path, "r") as input_handle:
                for record in SeqIO.parse(input_handle, "fasta"):
                    if record.id in reverse_gene_info:
                        marker = reverse_gene_info[record.id]
                        marker_faa_path = os.path.join(marker_dir, f"{genome}_{marker}.faa")
                        print(f"Writing to {marker_faa_path}")
                        with open(marker_faa_path, "a") as out_file:
                            out_file.write(f">{genome}\n{str(record.seq)}\n")
        else:
            print(f"{genome} markers = {len(genome_marker_count[genome])}")

if __name__ == "__main__":
    main()
