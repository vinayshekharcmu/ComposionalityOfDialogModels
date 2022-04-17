#!/usr/bin/env bash
#!/bin/sh
DATASET_NAME=$1
EXPERIMENT_NAME=$2
OUTPUT_PATH=$3
for id in 1 2 3 4 5
do
    bert-score -r $OUTPUT_PATH"/save_dir_run_"$id"refs.txt" -c $OUTPUT_PATH"/save_dir_run_"$id"hyps.txt" --lang en > ./bert-score/$id
done

python3 ./bert-score/parse_bert_score_output.py
