import string
import json
import argparse
import os

from config import *
from experiments.utils import *

from pdb import set_trace as bp

def drop_words_dataset(fold, fraction_drop):
    for obj in fold:
        obj.drop_stop_words(fraction_drop)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment_name", type=str, default="drop_words")
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--output_dir", type= str, required=True)
    parser.add_argument("--fraction_drop", type=float, required=False, default=1)

    args = parser.parse_args()



    print("Using Dataset ", args.dataset)
    print("Dropping Fraction ", args.fraction_drop)

    if "dailydialog" in args.dataset.lower():
        EXPERIMENT_NAME = os.path.join(args.experiment_name + '_' + str(args.fraction_drop), 'dailydialog')
        train = get_daily_dialog(os.path.join(args.dataset, "train.json"))
        valid = get_daily_dialog(os.path.join(args.dataset, "valid.json"))
        test = get_daily_dialog(os.path.join(args.dataset, "test.json"))

        drop_words_dataset(train, args.fraction_drop)

        serialize_daily_dialog(args.output_dir, EXPERIMENT_NAME, "train", train)
        serialize_daily_dialog(args.output_dir, EXPERIMENT_NAME, "valid", valid)
        serialize_daily_dialog(args.output_dir, EXPERIMENT_NAME, "test", test)

    if "mutualfriends" in args.dataset.lower():
        EXPERIMENT_NAME = os.path.join(args.experiment_name + '_' + str(args.fraction_drop), 'MutualFriends')
        train = get_mutual_friends(os.path.join(args.dataset, "train.json"))
        valid = get_mutual_friends(os.path.join(args.dataset, "valid.json"))
        test = get_mutual_friends(os.path.join(args.dataset, "test.json"))

        drop_words_dataset(train, args.fraction_drop)

        serialize_mutual_friends(args.output_dir, EXPERIMENT_NAME, "train", train)
        serialize_mutual_friends(args.output_dir, EXPERIMENT_NAME, "valid", valid)
        serialize_mutual_friends(args.output_dir, EXPERIMENT_NAME, "test", test)

    if "babi" in args.dataset.lower():
        EXPERIMENT_NAME = os.path.join(args.experiment_name + '_' + str(args.fraction_drop), 'dialog-bAbI/dialog-bAbI-tasks')
        BUILT_PATH = os.path.join(args.experiment_name + '_' + str(args.fraction_drop), 'dialog-bAbI')

        train = get_babi_dialog(os.path.join(args.dataset, "dialog-babi-task5-full-dialogs-trn.txt"))
        valid = get_babi_dialog(os.path.join(args.dataset, "dialog-babi-task5-full-dialogs-dev.txt"))
        test = get_babi_dialog(os.path.join(args.dataset, "dialog-babi-task5-full-dialogs-tst.txt"))

        drop_words_dataset(train, args.fraction_drop)

        serialize_babi(args.output_dir, EXPERIMENT_NAME, BUILT_PATH, "dialog-babi-task5-full-dialogs-trn.txt", train)
        serialize_babi(args.output_dir, EXPERIMENT_NAME, BUILT_PATH, "dialog-babi-task5-full-dialogs-dev.txt", valid)
        serialize_babi(args.output_dir, EXPERIMENT_NAME, BUILT_PATH, "dialog-babi-task5-full-dialogs-tst.txt", test)
        shutil.copy(os.path.join(args.dataset, "dialog-babi-task6-dstc2-candidates.txt"), os.path.join(args.output_dir, EXPERIMENT_NAME))
        shutil.copy(os.path.join(args.dataset, "dialog-babi-candidates.txt"),os.path.join(args.output_dir, EXPERIMENT_NAME))



if __name__ == "__main__":
    main()
