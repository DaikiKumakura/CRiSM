#!/bin/bash

# ヘルプメッセージを表示する関数
print_help() {
    echo "Usage: bash reformat_faa.sh -i input_dir -o output_dir"
    echo "-i input_dir   Specify the input directory containing .faa files."
    echo "-o output_dir  Specify the output directory where the processed files will be saved."
    echo "               If the directory does not exist, it will be created."
}

# コマンドラインオプションを解析
while getopts ":i:o:h" opt; do
    case ${opt} in
        i )
            input_dir=$OPTARG
            ;;
        o )
            output_dir=$OPTARG
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

# 入力ディレクトリと出力ディレクトリが指定されているか確認
if [ -z "$input_dir" ] || [ -z "$output_dir" ]; then
    echo "Both input and output directories must be specified." 1>&2
    print_help
    exit 1
fi

# 出力ディレクトリが存在しない場合は作成
mkdir -p "$output_dir"

# 入力ディレクトリ内のfaaファイルを処理
for file in "$input_dir"/*.faa; do
    if [ -f "$file" ]; then
        # '*'を削除して出力ファイルに保存
        sed 's/\*//g' "$file" > "$output_dir/$(basename "$file")"
    fi
done
