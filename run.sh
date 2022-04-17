#!/bin/sh

if [ -z "$4" ]
then
        echo "No Run id provided. Suported : 1,2,3,4,5,6"
        echo "Example train command : sh run.sh train <model_type> <dataset> <run_id>"
        echo "Example perturb command : sh run.sh perturb <model_type> <dataset> <run_id>"
        echo "Example perturb command : sh run.sh last_few_only <model_type> <dataset> <run_id>"
        exit 0
else
        RUN_ID=$4

fi

EXPERIMENT_NAME=$5
DATASET_PATH=$6
DATASET_NAME=$3
echo "RUN : "$RUN_ID
LOGDIR=$DATASET_NAME"/"$EXPERIMENT_NAME"/eval_log_files_"$RUN_ID"/"
SAVEDIR=$DATASET_NAME"/"$EXPERIMENT_NAME"/save_dir_run_"$RUN_ID"/"


GPU="0"
mkdir -p $LOGDIR

if [ -z "$1" ]
then
    echo "No Run mode provided. Supported : train, perturb, last_few_only"
    echo "Example train command : sh run.sh train <model_type> <dataset> <run_id>"
    echo "Example perturb command : sh run.sh perturb <model_type> <dataset> <run_id>"
    echo "Example perturb command : sh run.sh last_few_only <model_type> <dataset> <run_id>"
    exit 0

else
    RUN_MODE=$1
fi

GPU_ARGS=" --gpu "$GPU
if [ "$2" = "s2s" ]
then
    echo "MODELTYPE: "$2
    COMMON_ARGS=$GPU_ARGS" -m seq2seq"
    EVAL_MODEL_ARGS=$COMMON_ARGS" -bs 1 -d False -ne 1000"
    TRAIN_MODEL_ARGS=$COMMON_ARGS" -vmt loss -eps 60 -veps 1 -stim 600 -bs 32 --optimizer adam --lr-scheduler invsqrt -lr 0.005 --dropout 0.3 --warmup-updates 4000"
elif [ "$2" = "s2s_bidir" ]
then
    echo "MODELTYPE: "$2
    COMMON_ARGS=$GPU_ARGS" -m seq2seq --bidirectional true --hiddensize 256"
    EVAL_MODEL_ARGS=$COMMON_ARGS" -bs 1 -d False -ne 1000"
    TRAIN_MODEL_ARGS=$COMMON_ARGS" -vmt loss -eps 60 -veps 1 -stim 600 -bs 32 --optimizer adam --lr-scheduler invsqrt -lr 0.005 --dropout 0.3 --warmup-updates 4000"
elif [ "$2" = "s2s_att_general" ]
then
    echo "MODELTYPE: "$2
    COMMON_ARGS=$GPU_ARGS" -m seq2seq -att general"
    EVAL_MODEL_ARGS=$COMMON_ARGS" -bs 1 -d False -ne 1000"
    TRAIN_MODEL_ARGS=$COMMON_ARGS" -vmt loss -eps 60 -veps 1 -stim 600 -bs 32 --optimizer adam --lr-scheduler invsqrt -lr 0.005 --dropout 0.3 --warmup-updates 4000"
elif [ "$2" = "s2s_att_general_bidir" ]
then
    echo "MODELTYPE: "$2
    COMMON_ARGS=$GPU_ARGS" -m seq2seq -att general --bidirectional true --hiddensize 256"
    EVAL_MODEL_ARGS=$COMMON_ARGS" -bs 1 -d False -ne 1000"
    TRAIN_MODEL_ARGS=$COMMON_ARGS" -vmt loss -eps 60 -veps 1 -stim 600 -bs 32 --optimizer adam --lr-scheduler invsqrt -lr 0.005 --dropout 0.3 --warmup-updates 4000"
elif [ "$2" = "transformer" ]
then
    echo "MODELTYPE: "$2
    COMMON_ARGS=$GPU_ARGS" -m transformer/generator"
    EVAL_MODEL_ARGS=$COMMON_ARGS" -bs 1 -d False -ne 1000"
    TRAIN_MODEL_ARGS=$COMMON_ARGS" -bs 64 --optimizer adam -lr 0.001 --lr-scheduler invsqrt --warmup-updates 4000 -eps 15 -veps 1 -stim 200 -vmt loss"
else
    echo "INVALID modeltype : "$2" Supported : s2s, s2s_att_general, transformer"
    echo "Example train command : sh run.sh train <model_type> <dataset> <run_id>"
    echo "Example perturb command : sh run.sh perturb <model_type> <dataset>"
    exit 0
fi

if [ -z "$3" ]
then
    echo "No dataset type specified supplied"
    echo "Example train command : sh run.sh train <model_type> <dataset> <run_id>"
    echo "Example perturb command : sh run.sh perturb <model_type> <dataset> <run_id>"
    exit 0
else
    DATASET=$3
    MF=$SAVEDIR"/model_"$3"_"$2
fi

if [ $RUN_MODE = "last_few_only" ]
then
    echo "MODE: "$RUN_MODE
    for MODEL_TYPE in $2
    do
        for DATATYPE in "test" #valid
        do
	   echo "---------------------"
	   echo "CONFIG : "$DATASET"_"$MODEL_TYPE"_"$DATATYPE"_NoPerturb"
	   LOGFILE=$LOGDIR/log_$DATASET"_"$MODEL_TYPE"_"$DATATYPE"_no_perturb.txt"
	   grep FINAL_REPORT $LOGFILE

            for NUM_TURNS_TO_RETAIN in 1 2 3 4 5 6
            do
                echo "---------------------"
                echo "CONFIG : "$DATASET"_"$MODEL_TYPE"_"$DATATYPE"_last_few_only__"$NUM_TURNS_TO_RETAIN
                LOGFILE=$LOGDIR/log_$DATASET"_"$MODEL_TYPE"_"$DATATYPE"_last_few_only__"$NUM_TURNS_TO_RETAIN".txt"
                python -W ignore examples/eval_model.py $EVAL_MODEL_ARGS -t $DATASET -mf $MF -sft True -pb "last_few_only__"$NUM_TURNS_TO_RETAIN --datatype $DATATYPE > $LOGFILE
                grep FINAL_REPORT $LOGFILE

            done
        done
    done

elif [ $RUN_MODE = "eval" ]
then
    echo "MODE : "$RUN_MODE
    for MODEL_TYPE in $2
    do
        for DATATYPE in "test" #valid
        do
            echo "---------------------"
            echo "CONFIG : "$DATASET"_"$MODEL_TYPE"_"$DATATYPE"_NoPerturb"
            LOGFILE=$LOGDIR/log_$DATASET"_"$MODEL_TYPE"_"$DATATYPE"_no_perturb.txt"
            echo $EVAL_MODEL_ARGS
            python -W ignore examples/eval_model.py $EVAL_MODEL_ARGS -t $DATASET -mf $MF --datatype $DATATYPE --datapath $DATASET_PATH  > $LOGFILE
            tail -n 1 $LOGFILE

#            for PERTURB_TYPE in "only_last" "shuffle" "reverse_utr_order" "drop_first" "drop_last" "worddrop_random" "verbdrop_random" "noundrop_random" "wordshuf_random" "wordreverse_random"
#            do
#                echo "---------------------"
#                echo "CONFIG : "$DATASET"_"$MODEL_TYPE"_"$DATATYPE"_"$PERTURB_TYPE
#                LOGFILE=$LOGDIR/log_$DATASET"_"$MODEL_TYPE"_"$DATATYPE"_"$PERTURB_TYPE".txt"
#                python -W ignore ./examples/eval_model.py $EVAL_MODEL_ARGS -t $DATASET -mf $MF -sft True -pb $PERTURB_TYPE --datatype $DATATYPE > $LOGFILE
#                grep FINAL_REPORT $LOGFILE
#            done
        done
    done
elif [ $RUN_MODE = "train" ]
then
    echo $TRAIN_MODEL_ARGS
    echo $DATASET_PATH
    python examples/train_model.py -t $DATASET -mf $MF $TRAIN_MODEL_ARGS --datapath $DATASET_PATH
else
    echo "Invalid Run mode provided. Supported : train, perturb, last_few_only"
    echo "Example train command : sh run.sh train <model_type> <dataset> <run_id>"
    echo "Example perturb command : sh run.sh perturb <model_type> <dataset> <run_id>"
    echo "Example perturb command : sh run.sh last_few_only <model_type> <dataset> <run_id>"
    exit 0
fi
