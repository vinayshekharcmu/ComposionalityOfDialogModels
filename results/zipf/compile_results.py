import csv
import numpy as np
from tabulate import tabulate

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
    # assert len(experiments) == 6  # Including baseline
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
    return means, stds

if __name__ == "__main__":
    means_daily_transformer, std_dialy_transformer = read_results("./dailydialog_transformer.csv", "\small{dailydialog}")
    means_mmf_transformer, std_mmf_transformer = read_results("./mmf_transformer.csv", "\small{MutualFriends}")
    means_babi_transformer, std_babi_transformer = read_results("./babi_transformer.csv", "\small{Babi}")

    means_daily_s2s, std_dialy_s2s = read_results("./dailydialog_s2s.csv",
                                                                  "\small{dailydialog}")
    means_mmf_s2s, std_mmf_s2s = read_results("./mmf_s2s.csv", "\small{MutualFriends}")
    means_babi_s2s, std_babi_s2s = read_results("./babi_s2s.csv", "\small{Babi}")

    means_daily_s2s_attn, std_dialy_s2s_attn = read_results("./dailydialog_s2s_attn.csv",
                                                  "\small{dailydialog}")
    means_mmf_s2s_attn, std_mmf_s2s_attn = read_results("./mmf_s2s_attn.csv", "\small{MutualFriends}")
    means_babi_s2s_attn, std_babi_s2s_attn = read_results("./babi_s2s_attn.csv", "\small{Babi}")

    outputs = []
    EXPERIMENT_NAMES_DAILY = ["\small{0-1}", "\small{1-3}", "\small{0-3}", "\small{500-1000}", "\small{1000-1500}", "\small{500-1500}"]
    MODEL_NAMES = ["Transformer", "S2S", "S2SA"]
    MODEL_NAMES = list(map(lambda x: "\small{" + x + "}", MODEL_NAMES))

    assert len(EXPERIMENT_NAMES_DAILY) == len(means_daily_transformer)
    assert len(EXPERIMENT_NAMES_DAILY) == len(means_daily_s2s)
    assert len(EXPERIMENT_NAMES_DAILY) == len(means_daily_s2s_attn)

    for experiment_name, mean_transformer, mean_s2s, mean_s2s_attn in zip(EXPERIMENT_NAMES_DAILY, means_daily_transformer, means_daily_s2s, means_daily_s2s_attn):
        outputs.append((experiment_name, mean_transformer, mean_s2s, mean_s2s_attn))
    res = tabulate(outputs, tablefmt="latex_raw", floatfmt=".1f")
    print("Daily Dialog")
    print(res)
    print(" & ".join(MODEL_NAMES))

    outputs = []
    EXPERIMENT_NAMES_MMF = ["\small{0-1}", "\small{1-3}", "\small{0-3}", "\small{300-600}",
                              "\small{600-1000}", "\small{300-1000}"]
    MODEL_NAMES = ["Transformer", "S2S", "S2SA"]
    MODEL_NAMES = list(map(lambda x: "\small{" + x + "}", MODEL_NAMES))

    assert len(EXPERIMENT_NAMES_MMF) == len(means_mmf_transformer)
    assert len(EXPERIMENT_NAMES_MMF) == len(means_mmf_s2s)
    assert len(EXPERIMENT_NAMES_MMF) == len(means_mmf_s2s_attn)

    for experiment_name, mean_transformer, mean_s2s, mean_s2s_attn in zip(EXPERIMENT_NAMES_MMF,
                                                                          means_mmf_transformer, means_mmf_s2s,
                                                                          means_mmf_s2s_attn):
        outputs.append((experiment_name, mean_transformer, mean_s2s, mean_s2s_attn))
    res = tabulate(outputs, tablefmt="latex_raw", floatfmt=".1f")
    print("Mutual Friends")
    print(res)
    print(" & ".join(MODEL_NAMES))

    outputs = []
    EXPERIMENT_NAMES_BABI = ["\small{0-1}", "\small{0-2}", "\small{36-44}", "\small{36-55}"]
    MODEL_NAMES = ["Transformer", "S2S", "S2SA"]
    MODEL_NAMES = list(map(lambda x: "\small{" + x + "}", MODEL_NAMES))

    assert len(EXPERIMENT_NAMES_BABI) == len(means_babi_transformer)
    assert len(EXPERIMENT_NAMES_BABI) == len(means_babi_s2s)
    assert len(EXPERIMENT_NAMES_BABI) == len(means_babi_s2s_attn)

    for experiment_name, mean_transformer, mean_s2s, mean_s2s_attn in zip(EXPERIMENT_NAMES_BABI,
                                                                          means_babi_transformer, means_babi_s2s,
                                                                          means_babi_s2s_attn):
        outputs.append((experiment_name, mean_transformer, mean_s2s, mean_s2s_attn))
    res = tabulate(outputs, tablefmt="latex_raw", floatfmt=".1f")
    print("Babi")
    print(res)
    print(" & ".join(MODEL_NAMES))

