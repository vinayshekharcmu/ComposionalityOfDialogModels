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

if __name__ == "__main__":
    HEADER_ROW = ["Dataset", "Baseline", "DS-0.75", "DS-0.5", "DS-0.25" , "DNS-0.75", "DNS-0.5", "DNS-0.25", "BT-Russian"]
    HEADER_ROW = list(map(lambda x: "\small{" + x + "}", HEADER_ROW))
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="transformer")
    args = parser.parse_args()

    means_daily, std_dialy = read_results("./dailydialog_" + args.model_name + ".csv", "\small{dailydialog}")
    means_mmf, std_mmf = read_results("./mmf_" + args.model_name + ".csv", "\small{MutualFriends}")
    means_babi, std_babi = read_results("./babi_" + args.model_name + ".csv", "\small{Babi}")
    output = [means_daily, means_mmf, means_babi]
    res = tabulate(output, tablefmt="latex_raw", floatfmt=".1f")
    print(res)
    print(" & ".join(HEADER_ROW))
