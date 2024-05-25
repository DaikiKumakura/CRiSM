import argparse
import subprocess
from crism.run_pipeline import run_pipeline

def main():
    # コマンドライン引数を設定
    parser = argparse.ArgumentParser(description="Run the CRiSM pipeline for phylogenetic analysis using concatenated ribosomal marker genes.")
    parser.add_argument('-i', '--input', required=True, help="Specify the input directory containing genomic data.")
    parser.add_argument('-o', '--output', required=True, help="Specify the output directory for the analysis results.")
    parser.add_argument('--db', required=True, help="Specify the path to the HMM database file used for gene identification.")
    parser.add_argument('--list', required=True, help="Specify the path to the list of marker genes.")
    parser.add_argument('-t', '--threads', type=int, default=1, help="Specify the number of CPU threads to use during analysis.")

    # 引数を解析
    args = parser.parse_args()

    # パイプラインの実行
    run_pipeline(args.input, args.output, args.db, args.list, args.threads)

if __name__ == "__main__":
    main()
