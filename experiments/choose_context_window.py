import string
import json
import argparse
import os

from config import *
from experiments.utils import *

from pdb import set_trace as bp

def choose_length_daily(fold, max_length, datatype):

    for obj in fold:
        obj.make_small(max_length)

    return fold

# def choose_length_mutual(fold, max_length, datatype):
#     max_length = 8
#     calculated_lengths = []
#     for obj in fold:
#         temp_c = 0
#         for dialog in obj.dialog:
#             if dialog['action'] == 'message':
#                 temp_c += 1
#         calculated_lengths.append(temp_c)
#
#     count = 0
#     final_list_idx = []
#     for idx, each in enumerate(calculated_lengths):
#         if each <= max_length:
#             final_list_idx.append(idx)
#
#     obj_final = []
#     for idx, obj in enumerate(fold):
#         if datatype == 'train':
#             if idx in final_list_idx:
#                 obj_final.append(obj)
#             else:
#                 obj.make_dialog_empty()
#                 obj_final.append(obj)
#         else:
#             if idx not in final_list_idx:
#                 obj_final.append(obj)
#
#     return obj_final

def choose_length_mutual(fold, max_length, datatype):

    calculated_lengths = []
    for obj in fold:
        obj.make_small(max_length)

    return fold


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment_name", type=str, default="context_change")
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--output_dir", type= str, required=True)
    parser.add_argument("--length_train", type=int, required=False, default=20)
    parser.add_argument("--length_test", type=int, required=False, default=20)
    parser.add_argument("--length", type=int, required=False, default=2)
    args = parser.parse_args()



    print("Using Dataset ", args.dataset)
    print("Modifying Context Lengths ", args.length)

    if "dailydialog" in args.dataset.lower():
        EXPERIMENT_NAME = os.path.join(args.experiment_name + '_' + str(args.length), 'dailydialog')
        train = get_daily_dialog(os.path.join(args.dataset, "train.json"))
        valid = get_daily_dialog(os.path.join(args.dataset, "valid.json"))
        test = get_daily_dialog(os.path.join(args.dataset, "test.json"))


        train = choose_length_daily(train, args.length, 'train')


        serialize_daily_dialog(args.output_dir, EXPERIMENT_NAME, "train", train)
        serialize_daily_dialog(args.output_dir, EXPERIMENT_NAME, "valid", valid)
        serialize_daily_dialog(args.output_dir, EXPERIMENT_NAME, "test", test)

    if "mutualfriends" in args.dataset.lower():
        EXPERIMENT_NAME = os.path.join(args.experiment_name + '_' + str(args.length), 'MutualFriends')
        train = get_mutual_friends(os.path.join(args.dataset, "train.json"))
        valid = get_mutual_friends(os.path.join(args.dataset, "valid.json"))
        test = get_mutual_friends(os.path.join(args.dataset, "test.json"))


        train = choose_length_mutual(train, args.length, 'train')


        serialize_mutual_friends(args.output_dir, EXPERIMENT_NAME, "train", train)
        serialize_mutual_friends(args.output_dir, EXPERIMENT_NAME, "valid", valid)
        serialize_mutual_friends(args.output_dir, EXPERIMENT_NAME, "test", test)

    if "babi" in args.dataset.lower():
        EXPERIMENT_NAME = os.path.join(args.experiment_name + '_' + str(args.length),
                                       'dialog-bAbI/dialog-bAbI-tasks')
        BUILT_PATH = os.path.join(args.experiment_name + '_' + str(args.length), 'dialog-bAbI')

        train = get_babi_dialog(os.path.join(args.dataset, "dialog-babi-task5-full-dialogs-trn.txt"))
        valid = get_babi_dialog(os.path.join(args.dataset, "dialog-babi-task5-full-dialogs-dev.txt"))
        test = get_babi_dialog(os.path.join(args.dataset, "dialog-babi-task5-full-dialogs-tst.txt"))

        train = choose_length_mutual(train, args.length, 'train')

        serialize_babi(args.output_dir, EXPERIMENT_NAME, BUILT_PATH, "dialog-babi-task5-full-dialogs-trn.txt", train)
        serialize_babi(args.output_dir, EXPERIMENT_NAME, BUILT_PATH, "dialog-babi-task5-full-dialogs-dev.txt", valid)
        serialize_babi(args.output_dir, EXPERIMENT_NAME, BUILT_PATH, "dialog-babi-task5-full-dialogs-tst.txt", test)
        shutil.copy(os.path.join(args.dataset, "dialog-babi-task6-dstc2-candidates.txt"),
                    os.path.join(args.output_dir, EXPERIMENT_NAME))
        shutil.copy(os.path.join(args.dataset, "dialog-babi-candidates.txt"),
                    os.path.join(args.output_dir, EXPERIMENT_NAME))


if __name__ == "__main__":
    main()
