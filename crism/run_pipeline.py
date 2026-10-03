import subprocess
import sys
from pathlib import Path

def run_step(script, *arguments):
    """Resolve installed scripts independently of the caller's working directory."""
    script_path = Path(__file__).resolve().parent / 'scripts' / script
    subprocess.run([sys.executable, str(script_path), *arguments], check=True)

def run_pipeline(input_dir, output_dir, hmm_file, list_file, threads):
    # Step 1: Reformat fna files
    run_step('reformat.py',
        '-i', input_dir,
        '-o', f'{output_dir}/01_reformat_fna'
    )
    
    # Step 2: Annotation and searching for marker genes
    run_step('finder.py',
        '-i', f'{output_dir}/01_reformat_fna',
        '-o', f'{output_dir}/02_finder',
        '--db', hmm_file
    )
    
    # Step 3: Extract full marker gene faa files
    run_step('extract_markers.py',
        '-i', f'{output_dir}/02_finder/marker',
        '-o', f'{output_dir}/03_extract_markers',
        '--list', list_file
    )
    
    # Step 4: Combine marker genes
    run_step('combine.py',
        '-i', f'{output_dir}/03_extract_markers',
        '-o', f'{output_dir}/04_combine',
        '--list', list_file
    )
    
    # Step 5: Reformat faa files
    run_step('reformat.py',
        '-i', f'{output_dir}/04_combine',
        '-o', f'{output_dir}/05_reformat_faa'
    )
    
    # Step 6: Alignment and trimmed
    run_step('align.py',
        '-i', f'{output_dir}/05_reformat_faa',
        '-o', f'{output_dir}/06_align',
        '-t', str(threads)
    )
    
    # Step 7: Concatenated aln files
    run_step('cat_align.py',
        '-i', f'{output_dir}/06_align/trim',
        '-o', f'{output_dir}/07_cat',
        '--list', list_file
    )
    
    # Step 8: Phylogenetic tree
    run_step('tree.py',
        '-i', f'{output_dir}/07_cat/Dataset1_cat.trimmed.aln',
        '-o', f'{output_dir}/08_tree',
        '-t', str(threads)
    )
    
    print("Pipeline completed successfully.")

if __name__ == '__main__':
    import sys
    run_pipeline(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
