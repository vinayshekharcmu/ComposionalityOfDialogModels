#!/bin/sh
DATASET_NAME=$1
OUTPUT_PATH=$2
DATASET_PATH=$3
for id in 1 2 3 4 5
do
    echo $OUTPUT_PATH"/eval_log_files_"$id"/refs.txt"
    echo $OUTPUT_PATH"save_dir_run_"$id"/model_"$DATASET_NAME"_transformer"
    python3 examples/display_model.py -t $DATASET_NAME -mf $OUTPUT_PATH"save_dir_run_"$id"/model_"$DATASET_NAME"_transformer" --datapath $DATASET_PATH > $OUTPUT_PATH"/eval_log_files_"$id"/refs_raw"
done
