import csv
import numpy as np
from tabulate import tabulate
import argparse

def read_csv(file_name):
    output = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            output.append(row)
    return output

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def read_results(filename, dataset):
    rows = read_csv(filename)
    experiments = list(divide_chunks(rows, 7))
    means = []
    stds = []
    assert len(experiments) == 8  # Including baseline
    for experiment in experiments:
        experiment.pop(0)
        experiment.pop(0)
        assert len(experiment) == 5
        ppls = [float(res[-1]) for res in experiment]
        means.append(np.mean(ppls))
        stds.append(np.std(ppls))
    means = np.around(means, decimals=1).tolist()
    stds = np.around(stds, decimals=1).tolist()
    means = list(map(lambda x : str(x), means))
    for i in range(len(means)):
        means[i] = "\small{" + means[i] + "}" + "$_{[" + str(stds[i]) + "]}$"
    return [dataset] + means, stds


def split_by_dataset(all_lines):
    assert  len(all_lines) == 451
    ENDS = [155, 311, 451]
    dailydialog_experiments = all_lines[:ENDS[0]]
    mutualfriends_experiments = all_lines[ENDS[0] + 1:ENDS[1]]
    babi_experiments = all_lines[ENDS[1] + 1:ENDS[2]]

    return dailydialog_experiments, mutualfriends_experiments, babi_experiments

def get_in_numerical_format(list_of_experiments):
    all_experiments = []
    for experiment in list_of_experiments:
        current_experiment = []
        name_of_the_table = experiment[0]
        current_experiment.append(name_of_the_table)
        header = experiment[1]
        header.pop(3) # Popping Bleu
        current_experiment.append(header)
        experiment.pop(-1)
        for row in experiment[2:]:
            row.pop(3)

            for i in range(len(row)):
                if i ==0:
                    row[i] = int(row[i])
                else:
                    row[i] = float(row[i])

            current_experiment.append(row)
        all_experiments.append(current_experiment)
    return all_experiments

def generate_latex_for_experiment(rows):
    rows[0][0] = "\multicolumn{6}{c}{\\textbf{" + rows[0][0] + "}}"
    rows[1][0] = "Id"
    rows[1][3] = "token acc"
    res = tabulate(rows, tablefmt="latex_raw", floatfmt=".1f")
    mod_res = res.split("\n")
    mod_res[2] = mod_res[2].replace("&", "")
    mod_res[2] = mod_res[2].replace("\t", "")
    mod_res.insert(3, "\hline")
    print("\n".join(mod_res))
    print("\n")
    print("\\vspace{1em}")

if __name__ == "__main__":
    HEADER_ROW = ["RUN ID", "acc", "f1", "belu", "token_acc", "ppl"]
    HEADER_ROW = list(map(lambda x: "\small{" + x + "}", HEADER_ROW))
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="S2S")
    args = parser.parse_args()

    filename = args.model_name + "-appendix.csv"
    all_lines = read_csv(filename)
    dailydialog_experiments, mutualfriends_experiments, babi_experiments = split_by_dataset(all_lines)

    dailydialog_experiments = list(divide_chunks(dailydialog_experiments[3:], 8))
    numerical_dailydialog_experiments = get_in_numerical_format(dailydialog_experiments)

    mutualfriends_experiments = list(divide_chunks(mutualfriends_experiments[3:], 8))
    numerical_mutualfriends_experiments = get_in_numerical_format(mutualfriends_experiments)

    babi_experiments = list(divide_chunks(babi_experiments[3:], 8))
    numerical_babi_experiments = get_in_numerical_format(babi_experiments)

    print("\\subsubsection{Daily Dialog}")
    for experiment in numerical_dailydialog_experiments:
        generate_latex_for_experiment(experiment)

    print("\\subsubsection{Mutual Friends}")
    for experiment in numerical_mutualfriends_experiments:
        generate_latex_for_experiment(experiment)

    print("\\subsubsection{Babi}")
    for experiment in numerical_babi_experiments:
        generate_latex_for_experiment(experiment)
