import string
import json
import argparse
import os

from config import *
from experiments.utils import *

from pdb import set_trace as bp

def choose_length_daily(fold, max_length, datatype):

    max_length = 20

    calculated_lengths = []
    for obj in fold:
        dialog_lengths = []
        for dialog in obj.dialog:
            dialog_lengths.append(len(dialog['text'].split()))
        calculated_lengths.append(dialog_lengths)

    count = 0
    final_list_idx = []
    for idx, each in enumerate(calculated_lengths):
        flag = 0

        for every in each:
            if every > max_length:
                flag = 1

        if flag == 0:
            count += 1 
            final_list_idx.append(idx)

    obj_final = []
    for idx, obj in enumerate(fold):
        if datatype == 'train':
            if idx in final_list_idx:
                obj_final.append(obj)
        else:
            if idx not in final_list_idx:
                obj_final.append(obj)

    return obj_final

def choose_length_mutual(fold, max_length, datatype):


    max_length = 9    
    calculated_lengths = []
    for obj in fold:
        dialog_lengths = []
        for dialog in obj.dialog:
            if dialog['action'] == 'message':
                dialog_lengths.append(len(dialog['data'].split()))
        calculated_lengths.append(dialog_lengths)

    count = 0
    final_list_idx = []
    for idx, each in enumerate(calculated_lengths):
        flag = 0

        for every in each:
            if every > max_length:
                flag = 1

        if flag == 0:
            count += 1 
            final_list_idx.append(idx)

    obj_final = []
    for idx, obj in enumerate(fold):
        if datatype == 'train':
            if idx in final_list_idx:
                obj_final.append(obj)
        else:
            if idx not in final_list_idx:
                obj_final.append(obj)

    return obj_final

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment_name", type=str, default="length_change")
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--output_dir", type= str, required=True)
    parser.add_argument("--fraction_drop", type=float, required=False, default=1)
    parser.add_argument("--length_train", type=int, required=False, default=20)
    parser.add_argument("--length_test", type=int, required=False, default=20)
    args = parser.parse_args()



    print("Using Dataset ", args.dataset)
    print("Modifying Context Lengths ", args.fraction_drop)

    if "dailydialog" in args.dataset.lower():
        EXPERIMENT_NAME = os.path.join(args.experiment_name + '_' + str(args.fraction_drop), 'dailydialog')
        train = get_daily_dialog(os.path.join(args.dataset, "train.json"))
        valid = get_daily_dialog(os.path.join(args.dataset, "valid.json"))
        test = get_daily_dialog(os.path.join(args.dataset, "test.json"))


        train = choose_length_daily(train, args.length_train, 'train')
        test = choose_length_daily(test, args.length_test, 'test')
        valid = choose_length_daily(valid, args.length_test, 'valid')


        serialize_daily_dialog(args.output_dir, EXPERIMENT_NAME, "train", train)
        serialize_daily_dialog(args.output_dir, EXPERIMENT_NAME, "valid", valid)
        serialize_daily_dialog(args.output_dir, EXPERIMENT_NAME, "test", test)

    if "mutualfriends" in args.dataset.lower():
        EXPERIMENT_NAME = os.path.join(args.experiment_name + '_' + str(args.fraction_drop), 'MutualFriends')
        train = get_mutual_friends(os.path.join(args.dataset, "train.json"))
        valid = get_mutual_friends(os.path.join(args.dataset, "valid.json"))
        test = get_mutual_friends(os.path.join(args.dataset, "test.json"))


        train = choose_length_mutual(train, args.length_train, 'train')
        test = choose_length_mutual(test, args.length_test, 'test')
        valid = choose_length_mutual(valid, args.length_test, 'valid')


        serialize_mutual_friends(args.output_dir, EXPERIMENT_NAME, "train", train)
        serialize_mutual_friends(args.output_dir, EXPERIMENT_NAME, "valid", valid)
        serialize_mutual_friends(args.output_dir, EXPERIMENT_NAME, "test", test)

if __name__ == "__main__":
    main()
