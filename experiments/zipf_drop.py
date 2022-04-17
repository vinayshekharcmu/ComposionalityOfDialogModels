import string
import json
import argparse
import os
import pickle

from config import *
from experiments.utils import *

from pdb import set_trace as bp

def drop_freq_words_dataset(fold, fraction_drop, left, right, sorted_rank_list):

    #fp = open('mutualtermlist.pkl', 'wb')
    #pickle.dump(sorted_rank_list, fp)
    #fp.close()

    total_words = len(sorted_rank_list)
    start_rank = left
    end_rank = right
    selected_words = sorted_rank_list[start_rank:end_rank]
    term_set = set([each[0] for each in selected_words])
    for obj in fold:
        obj.drop_freq_words(term_set, fraction_drop)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment_name", type=str, default="zipf_drop")
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--output_dir", type= str, required=True)
    parser.add_argument("--range_left", type=int, default=0)
    parser.add_argument("--range_right", type=int, default=10)
    parser.add_argument("--fraction_drop", type=float, default=1)

    args = parser.parse_args()



    print("Using Dataset ", args.dataset)
    print("Dropping Terms with rank in range (percentage) ", args.range_left, args.range_right)
    print("Fraction of Drop ", args.fraction_drop)

    if "dailydialog" in args.dataset.lower():
        EXPERIMENT_NAME = os.path.join(args.experiment_name + "_" + str(args.range_left) + "_" + str(args.range_right) , 'dailydialog')

        train = get_daily_dialog(os.path.join(args.dataset, "train.json"))
        valid = get_daily_dialog(os.path.join(args.dataset, "valid.json"))
        test = get_daily_dialog(os.path.join(args.dataset, "test.json"))

        sorted_rank_list = get_sorted_list_dailydialog(train)
        drop_freq_words_dataset(train, args.fraction_drop, \
                                args.range_left, args.range_right, sorted_rank_list)


        serialize_daily_dialog(args.output_dir, EXPERIMENT_NAME, "train", train)
        serialize_daily_dialog(args.output_dir, EXPERIMENT_NAME, "valid", valid)
        serialize_daily_dialog(args.output_dir, EXPERIMENT_NAME, "test", test)

    if "mutualfriends" in args.dataset.lower():
        EXPERIMENT_NAME = os.path.join(args.experiment_name + "_" + str(args.range_left) + "_" + str(args.range_right),
                                       'MutualFriends')
        train = get_mutual_friends(os.path.join(args.dataset, "train.json"))
        valid = get_mutual_friends(os.path.join(args.dataset, "valid.json"))
        test = get_mutual_friends(os.path.join(args.dataset, "test.json"))


        sorted_rank_list = get_sorted_list_mutual_friends(train)
        drop_freq_words_dataset(train, args.fraction_drop, \
                                args.range_left, args.range_right, sorted_rank_list)

        serialize_mutual_friends(args.output_dir, EXPERIMENT_NAME, "train", train)
        serialize_mutual_friends(args.output_dir, EXPERIMENT_NAME, "valid", valid)
        serialize_mutual_friends(args.output_dir, EXPERIMENT_NAME, "test", test)

    if "babi" in args.dataset.lower():
        EXPERIMENT_NAME = os.path.join(args.experiment_name + '_' + str(args.range_left) + "_" + str(args.range_right),
                                       'dialog-bAbI/dialog-bAbI-tasks')
        BUILT_PATH = os.path.join(args.experiment_name + '_' + str(args.range_left) + "_" + str(args.range_right), 'dialog-bAbI')

        train = get_babi_dialog(os.path.join(args.dataset, "dialog-babi-task5-full-dialogs-trn.txt"))
        valid = get_babi_dialog(os.path.join(args.dataset, "dialog-babi-task5-full-dialogs-dev.txt"))
        test = get_babi_dialog(os.path.join(args.dataset, "dialog-babi-task5-full-dialogs-tst.txt"))

        sorted_rank_list = get_sorted_list_babi(train)

        with open("babi-stat.pkl", "wb") as f:
            pickle.dump(sorted_rank_list, f)

        drop_freq_words_dataset(train, args.fraction_drop, \
                                args.range_left, args.range_right, sorted_rank_list)

        serialize_babi(args.output_dir, EXPERIMENT_NAME, BUILT_PATH, "dialog-babi-task5-full-dialogs-trn.txt", train)
        serialize_babi(args.output_dir, EXPERIMENT_NAME, BUILT_PATH, "dialog-babi-task5-full-dialogs-dev.txt", valid)
        serialize_babi(args.output_dir, EXPERIMENT_NAME, BUILT_PATH, "dialog-babi-task5-full-dialogs-tst.txt", test)
        shutil.copy(os.path.join(args.dataset, "dialog-babi-task6-dstc2-candidates.txt"),
                    os.path.join(args.output_dir, EXPERIMENT_NAME))
        shutil.copy(os.path.join(args.dataset, "dialog-babi-candidates.txt"),
                    os.path.join(args.output_dir, EXPERIMENT_NAME))


if __name__ == "__main__":
    main()
