import subprocess

def run_pipeline(input_dir, output_dir, hmm_file, list_file, threads):
    # Step 1: Reformat fna files
    subprocess.call([
        'bash', 'crism/scripts/reformat_fna.sh',
        '-i', input_dir,
        '-o', f'{output_dir}/01_reformat_fna'
    ])
    
    # Step 2: Annotation and searching for marker genes
    subprocess.call([
        'python', 'crism/scripts/finder.py',
        '-i', f'{output_dir}/01_reformat_fna',
        '-o', f'{output_dir}/02_finder',
        '--markerdb', hmm_file,
        '--performProdigal'
    ])
    
    # Step 3: Extract full marker gene faa files
    subprocess.call([
        'python', 'crism/scripts/extract_markers.py',
        '-i', f'{output_dir}/02_finder/marker',
        '-o', f'{output_dir}/03_extract_markers',
        '-r', list_file
    ])
    
    # Step 4: Extract genomes faa files with full marker genes
    subprocess.call([
        'bash', 'crism/scripts/extract_genomes.sh',
        '-i', f'{output_dir}/02_finder/faa',
        '-o', f'{output_dir}/04_extract_genomes',
        '-r', f'{output_dir}/03_extract_markers/0_full_markergenes_genoms.txt'
    ])
    
    # Step 5: Combine marker genes
    subprocess.call([
        'bash', 'crism/scripts/combine.sh',
        '-i', f'{output_dir}/03_extract_markers',
        '-o', f'{output_dir}/05_combine',
        '-r', list_file
    ])
    
    # Step 6: Reformat faa files
    subprocess.call([
        'bash', 'crism/scripts/reformat_faa.sh',
        '-i', f'{output_dir}/05_combine',
        '-o', f'{output_dir}/06_reformat_faa'
    ])
    
    # Step 7: Align and trim
    subprocess.call([
        'bash', 'crism/scripts/align_trimmed.sh',
        '-i', f'{output_dir}/06_reformat_faa',
        '-o', f'{output_dir}/07_align_trimmed',
        '-t', str(threads)
    ])
    
    # Step 8: Phylogenetic tree construction
    subprocess.call([
        'bash', 'crism/scripts/tree.sh',
        '-i', f'{output_dir}/07_align_trimmed/trim',
        '-o', f'{output_dir}/08_tree',
        '-r', list_file
    ])
    
    print("Pipeline completed successfully.")

if __name__ == '__main__':
    import sys
    run_pipeline(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
