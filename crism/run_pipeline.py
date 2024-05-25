import subprocess

def run_pipeline(input_dir, output_dir, hmm_file, list_file, threads):
    # Step 1: Reformat fna files
    subprocess.call([
        'python', 'crism/scripts/reformat.py',
        '-i', input_dir,
        '-o', f'{output_dir}/01_reformat_fna'
    ])
    
    # Step 2: Annotation and searching for marker genes
    subprocess.call([
        'python', 'crism/scripts/finder.py',
        '-i', f'{output_dir}/01_reformat_fna',
        '-o', f'{output_dir}/02_finder',
        '--db', hmm_file
    ])
    
    # Step 3: Extract full marker gene faa files
    subprocess.call([
        'python', 'crism/scripts/extract_markers.py',
        '-i', f'{output_dir}/02_finder/marker',
        '-o', f'{output_dir}/03_extract_markers',
        '--list', list_file
    ])
    
    # Step 4: Combine marker genes
    subprocess.call([
        'python', 'crism/scripts/combine.py',
        '-i', f'{output_dir}/03_extract_markers',
        '-o', f'{output_dir}/04_combine',
        '--list', list_file
    ])
    
    # Step 5: Reformat faa files
    subprocess.call([
        'python', 'crism/scripts/reformat.py',
        '-i', f'{output_dir}/04_combine',
        '-o', f'{output_dir}/05_reformat_faa'
    ])
    
    # Step 6: Alignment and trimmed
    subprocess.call([
        'python', 'crism/scripts/align.py',
        '-i', f'{output_dir}/05_reformat_faa',
        '-o', f'{output_dir}/06_align',
        '-t', str(threads)
    ])
    
    # Step 7: Concatenated aln files
    subprocess.call([
        'python', 'crism/scripts/cat_align.py',
        '-i', f'{output_dir}/06_align/trim',
        '-o', f'{output_dir}/07_cat',
        '--list', list_file
    ])
    
    # Step 8: Phylogenetic tree
    subprocess.call([
        'python', 'crism/scripts/tree.py',
        '-i', f'{output_dir}/07_cat/Dataset1_cat.trimmed.aln',
        '-o', f'{output_dir}/08_tree',
        '-t', str(threads)
    ])
    
    print("Pipeline completed successfully.")

if __name__ == '__main__':
    import sys
    run_pipeline(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
