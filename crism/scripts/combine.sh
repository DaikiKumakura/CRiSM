#!/bin/bash

# ヘルプメッセージの表示
usage() {
  echo "Usage: $0 -i input_dir -o output_dir -r list_file"
  echo "  -i input_dir    Specify the input directory containing the files."
  echo "  -o output_dir   Specify the output directory to save the results."
  echo "  -r list_file    Specify the file containing the list of markers."
  echo "  -h              Display this help message."
}

# 入力ディレクトリ、出力ディレクトリ、リストファイルの初期化
input_dir=""
output_dir=""
list_file=""

# 引数のパース
while getopts "i:o:r:h" opt; do
  case $opt in
    i) input_dir=$OPTARG ;;
    o) output_dir=$OPTARG ;;
    r) list_file=$OPTARG ;;
    h) usage
       exit 0 ;;
    *) usage
       exit 1 ;;
  esac
done

# 入力ディレクトリ、出力ディレクトリ、リストファイルが指定されていない場合のエラーメッセージ
if [ -z "$input_dir" ] || [ -z "$output_dir" ] || [ -z "$list_file" ]; then
  usage
  exit 1
fi

# 出力ディレクトリが存在しない場合は作成
mkdir -p "$output_dir"

# ファイルの結合処理
while read p; do
  for file in "$input_dir"/*_"$p".faa; do
    cat "$file" >> "$output_dir/Dataset1_$p.faa"
  done
done < "$list_file"

echo "Processing completed. Results are saved in $output_dir."
