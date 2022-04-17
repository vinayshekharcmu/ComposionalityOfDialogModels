import argparse
import json

def get_results_of_all_runs(filename):
    results = []
    with open(filename, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        line = line.replace("\n", "")
        if (i+1)%7 == 0 and i != 0:
            print(line)
            results.append(eval(line))
    return results

def print_results_for_excel(results):
    for result in results:
        row = [result["accuracy"], result["f1"], result["bleu"], result["token_acc"], result["ppl"]]
        row = map(lambda x: str(x), row)
        print(",".join(row))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file_path", type=str, default="")
    args = parser.parse_args()

    results = get_results_of_all_runs(args.output_file_path)
    print_results_for_excel(results)
