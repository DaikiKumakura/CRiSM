#!/bin/bash

# ヘルプメッセージを表示する関数
print_help() {
    echo "Usage: bash extract_full_marker_genomes.sh -i input_dir -o output_dir -r reference_file"
    echo "-i input_dir      Specify the input directory containing .faa files."
    echo "-o output_dir     Specify the output directory where the files will be copied."
    echo "                  If the directory does not exist, it will be created."
    echo "-r reference_file Specify the file containing the list of sample names to be copied."
}

# コマンドラインオプションを解析
while getopts ":i:o:r:h" opt; do
    case ${opt} in
        i )
            input_dir=$OPTARG
            ;;
        o )
            output_dir=$OPTARG
            ;;
        r )
            reference_file=$OPTARG
            ;;
        h )
            print_help
            exit 0
            ;;
        \? )
            echo "Invalid option: $OPTARG" 1>&2
            print_help
            exit 1
            ;;
        : )
            echo "Option -$OPTARG requires an argument." 1>&2
            exit 1
            ;;
    esac
done

# 入力ディレクトリ、出力ディレクトリ、参照ファイルが指定されているか確認
if [ -z "$input_dir" ] || [ -z "$output_dir" ] || [ -z "$reference_file" ]; then
    echo "Input directory, output directory, and reference file must all be specified." 1>&2
    print_help
    exit 1
fi

# 出力ディレクトリが存在しない場合は作成
mkdir -p "$output_dir"

# リファレンスファイルからサンプル名を読み込む
while IFS= read -r sample; do
    # 対応する.fnaファイルをコピー
    if [ -f "$input_dir/$sample.faa" ]; then
        cp "$input_dir/$sample.faa" "$output_dir/"
    fi
done < "$reference_file"
