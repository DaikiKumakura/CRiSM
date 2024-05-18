import argparse
import subprocess
from crism.run_pipeline import run_pipeline

def main():
    parser = argparse.ArgumentParser(description="CRiSM Pipeline")
    parser.add_argument('-i', '--input', required=True, help="Input directory")
    parser.add_argument('-o', '--output', required=True, help="Output directory")
    parser.add_argument('--hmm', required=True, help="HMM database file")
    parser.add_argument('--list', required=True, help="Marker genes list file")
    parser.add_argument('-t', '--threads', type=int, default=1, help="Number of threads")
    args = parser.parse_args()

    # Run the pipeline with the specified arguments
    run_pipeline(args.input, args.output, args.hmm, args.list, args.threads)

if __name__ == "__main__":
    main()
