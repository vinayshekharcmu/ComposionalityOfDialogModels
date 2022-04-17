import json
import string
from config import *
from operator import itemgetter
from dataset.DailyDialog import DailyDialog
from dataset.MutualFriends import MutualFriends
from dataset.Babi import Babi
import os
import shutil

from pdb import set_trace as bp

def get_sorted_list_mutual_friends(obj_list):

    print("Computing Term Frequencies")
    puncts = set(string.punctuation)

    term_dict = {}
    for obj in obj_list:
        for action_dict in obj.dialog:
            if action_dict['action'] == 'message':
                word_list = action_dict['data'].lower().split()
                for word in word_list:
                    if word not in puncts:
                        if word not in term_dict:
                            term_dict[word] = 0
                        term_dict[word] += 1

    sorted_list = sorted(term_dict.items(), key=itemgetter(1), reverse=True)
    return sorted_list

def get_sorted_list_babi(obj_list):

    print("Computing Term Frequencies")
    puncts = set(string.punctuation)

    term_dict = {}
    for obj in obj_list:
        for action_dict in obj.dialog:
            key = list(action_dict.keys())[0]
            if key in ["User", "Bot"]:
                if key == "Bot":
                    word_list = action_dict[key].lower().split()
                else:
                    word_list = action_dict[key].split(" ")[1].lower().split()
                for word in word_list:
                    if word not in puncts:
                        if word not in term_dict:
                            term_dict[word] = 0
                        term_dict[word] += 1

    sorted_list = sorted(term_dict.items(), key=itemgetter(1), reverse=True)
    return sorted_list


def get_mutual_friends(path_to_file):

    print("Opening File", path_to_file)

    lines = open(path_to_file).readlines()
    data = json.loads(lines[0])

    mutual_friends_objects = []
    for data_point in data:
        mutual_friends_objects.append(MutualFriends(data_point))

    return mutual_friends_objects

def serialize_mutual_friends(path_to_directory, experiment_name, fold_name, examples):
    if not os.path.exists(os.path.join(path_to_directory, experiment_name)):
        os.makedirs(os.path.join(path_to_directory, experiment_name))

    output = []
    for example in examples:
        serialized_example_dict = example.serialize()
        output.append(serialized_example_dict)

    #print(output)

    built_fp = open(os.path.join(os.path.join(path_to_directory, experiment_name), '.built'), 'w')
    built_fp.write("2019-11-08 16:52:09.154801\n")
    built_fp.write("None\n")
    built_fp.close()

    file_path = os.path.join(os.path.join(path_to_directory, experiment_name), fold_name + ".json")
    print("Writing File", file_path)

    fp = open(file_path, 'w')
    fp.write(json.dumps(output))
    fp.write('\n')
    fp.close()

def get_sorted_list_dailydialog(obj_list):

    print("Computing Term Frequencies")
    puncts = set(string.punctuation)

    term_dict = {}
    for obj in obj_list:
        for utterance in obj.dialog:
            word_list = utterance[TEXT].lower().split()
            for word in word_list:
                if word not in puncts:
                    if word not in term_dict:
                        term_dict[word] = 0
                    term_dict[word] += 1

    sorted_list = sorted(term_dict.items(), key=itemgetter(1), reverse=True)
    return sorted_list

def get_daily_dialog(path_to_file):

    print("Opening File", path_to_file)

    data = []
    with open(path_to_file) as f:
        for line in f:
            data.append(json.loads(line))

    daily_dialog_objects = []
    for data_point in data:
        daily_dialog = DailyDialog(data_point)
        daily_dialog_objects.append(daily_dialog)

    return daily_dialog_objects


def serialize_daily_dialog(path_to_directory, experiment_name, fold_name, examples):
    if not os.path.exists(os.path.join(path_to_directory, experiment_name)):
        os.makedirs(os.path.join(path_to_directory, experiment_name))

    output = []
    for example in examples:
        serialized_example_dict = example.serialize()
        output.append(serialized_example_dict)

    #print(output)

    built_fp = open(os.path.join(os.path.join(path_to_directory, experiment_name), '.built'), 'w')
    built_fp.write("2019-11-08 16:52:09.154801\n")
    built_fp.write("None\n")
    built_fp.close()

    file_path = os.path.join(os.path.join(path_to_directory, experiment_name), fold_name + ".json")

    print("Writing File", file_path)
    with open(file_path, 'w') as sample:
        for dict in output:
            sample.write('{}\n'.format(json.dumps(dict)))

def get_babi_dialog(path_to_file):

    print("Opening File", path_to_file)

    dialogs = []
    current_dialog = []
    with open(path_to_file) as f:
        for line in f:
            line=line.strip()
            if len(line) == 0:
                dialogs.append(current_dialog)
                current_dialog = []
            else:
                current_dialog.append(line)

    babi_dialog_objects = []
    for dialog in dialogs:
        babi_dialog = Babi(dialog)
        babi_dialog_objects.append(babi_dialog)

    return babi_dialog_objects

def serialize_babi(path_to_directory, experiment_name, built_path, fold_name, examples):
    if not os.path.exists(os.path.join(path_to_directory, experiment_name)):
        os.makedirs(os.path.join(path_to_directory, experiment_name))

    built_fp = open(os.path.join(os.path.join(path_to_directory, built_path), '.built'), 'w')
    built_fp.write("2019-11-08 16:52:09.154801\n")
    built_fp.write("None\n")
    built_fp.close()

    output = []
    for example in examples:
        serialized_output_list = example.serialize()
        output.append(serialized_output_list)

    file_path = os.path.join(os.path.join(path_to_directory, experiment_name), fold_name)
    print("Writing File", file_path)

    with open(file_path, "w") as f:
        for dialog in output:
            for line in dialog:
                f.write(line + "\n")
            f.write("\n")
