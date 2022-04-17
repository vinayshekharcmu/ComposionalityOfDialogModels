import csv
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt

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


def read_results(filename):
    rows = read_csv(filename)
    experiments = list(divide_chunks(rows, 7))
    means = []
    stds = []
    assert len(experiments) == 5  # Including baseline
    for experiment in experiments:
        experiment.pop(0)
        experiment.pop(0)
        assert len(experiment) == 5
        ppls = [float(res[-1]) for res in experiment]
        means.append(np.mean(ppls))
        stds.append(np.std(ppls))
    return means, stds

def create_graph(context_lengths, baseline_perplexities, perplexities_models, filename):
    """
    :param context_lengths: A list of experiments which the context length was changed for 2,4,6,8,10
    :param baseline_perplexities: A dictionary of three things with baseline perplexity to show on graph -
    :param perplexities_models: A dictionary with keys as list - pointing to different perplexities for different context length change
    :return:
    """
    plt.style.use("ggplot")
    title = "{}".format("Context lengths")
    plt.title(title)
    plt.xlabel("Contexts provided")
    plt.ylabel("% change in Perplexity")
    for key in perplexities_models:
        # plt.annotate("Baseline - " + key, (0, baseline_perplexities[key]))
        perplexities_models[key] = list(map(lambda x: (x - baseline_perplexities[key]) / baseline_perplexities[key] * 100, perplexities_models[key]))
        plt.plot(context_lengths, perplexities_models[key], label=key)
    plt.legend()
    plt.savefig(filename)
    plt.close()
    plt.clf()


if __name__ == "__main__":
    context_lengths = [2, 4, 6, 8, 10]

    means_daily_transformer, std_dialy_transformer = read_results("./dailydialog_transformer.csv")
    means_mmf_transformer, std_mmf_transformer = read_results("./mmf_transformer.csv")
    means_babi_transformer, std_babi_transformer = read_results("./babi_transformer.csv")

    means_daily_s2s, std_dialy_s2s = read_results("./dailydialog_s2s.csv")
    means_mmf_s2s, std_mmf_s2s = read_results("./mmf_s2s.csv")
    means_babi_s2s, std_babi_s2s = read_results("./babi_s2s.csv")

    means_daily_s2s_attn, std_dialy_s2s_attn = read_results("./dailydialog_s2s_attn.csv")
    means_mmf_s2s_attn, std_mmf_s2s_attn = read_results("./mmf_s2s_attn.csv")
    means_babi_s2s_attn, std_babi_s2s_attn = read_results("./babi_s2s_attn.csv")

    baseline_perplexities_daily = {"Transformer" : 33.2, "S2S" : 29.4, "S2SA" : 26.8}
    baseline_perplexities_mmf = {"Transformer": 12.5, "S2S": 13.3, "S2SA" : 10.3}
    baseline_perplexities_babi = {"Transformer": 1, "S2S": 1.2, "S2SA" : 1}

    perplexities_models_daily = {"Transformer":means_daily_transformer, "S2S" : means_daily_s2s, "S2SA" : means_daily_s2s_attn}
    perplexities_models_mmf = {"Transformer": means_mmf_transformer, "S2S" : means_mmf_s2s, "S2SA" : means_mmf_s2s_attn}
    perplexities_models_babi = {"Transformer" : means_babi_transformer, "S2S" : means_babi_s2s, "S2SA" : means_mmf_s2s_attn}

    create_graph(context_lengths, baseline_perplexities_daily, perplexities_models_daily, "daily.png")
    create_graph(context_lengths, baseline_perplexities_mmf, perplexities_models_mmf, "mmf.png")
    create_graph(context_lengths, baseline_perplexities_babi, perplexities_models_babi, "babi.png")
