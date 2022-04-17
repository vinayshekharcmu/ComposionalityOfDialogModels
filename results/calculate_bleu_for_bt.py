from nltk.translate.bleu_score import corpus_bleu
from experiments.utils import get_daily_dialog, get_mutual_friends, get_babi_dialog
import os
import argparse
from config import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_clean", type=str, required=True)
    parser.add_argument("--dataset_back", type=str, required=True)
    args = parser.parse_args()

    if "dailydialog" in args.dataset_clean.lower():
        test_clean = get_daily_dialog(os.path.join(args.dataset_clean, "test.json"))
        test_translated = get_daily_dialog(os.path.join(args.dataset_back, "test.json"))
        list_of_hypothesis = []
        list_of_references = []
        assert len(test_clean) == len(test_translated)
        for ground_truth, translation in zip(test_clean, test_translated):
            assert len(ground_truth.dialog) == len(translation.dialog)
            for utterance_ground, utterance_translation in zip(ground_truth.dialog, translation.dialog):
                references = [utterance_ground[TEXT].split(" ")]
                list_of_references.append(references)
                hypothesis = utterance_translation[TEXT].split(" ")
                list_of_hypothesis.append(hypothesis)
        print(corpus_bleu(list_of_references, list_of_hypothesis))

    elif "mutualfriends" in args.dataset_clean.lower():
        test_clean = get_mutual_friends(os.path.join(args.dataset_clean, "test.json"))
        test_translated = get_mutual_friends(os.path.join(args.dataset_back, "test.json"))
        list_of_hypothesis = []
        list_of_references = []
        assert len(test_clean) == len(test_translated)

        for ground_truth, translation in zip(test_clean, test_translated):
            assert ground_truth.uuid == translation.uuid
            assert len(ground_truth.dialog) == len(translation.dialog)
            for utterance_ground, utterance_translation in zip(ground_truth.dialog, translation.dialog):
                if utterance_ground["action"] == "message":
                    references = [utterance_ground["data"].split(" ")]
                    list_of_references.append(references)
                    hypothesis = utterance_translation["data"].split(" ")
                    list_of_hypothesis.append(hypothesis)
                    print(utterance_ground, utterance_translation)
        print(corpus_bleu(list_of_references, list_of_hypothesis))


    elif "babi" in args.dataset_clean.lower():
        test_clean = get_babi_dialog(os.path.join(args.dataset_clean, "dialog-babi-task5-full-dialogs-tst.txt"))
        test_translated = get_babi_dialog(os.path.join(args.dataset_back, "dialog-babi-task5-full-dialogs-tst.txt"))
        list_of_hypothesis = []
        list_of_references = []
        assert len(test_clean) == len(test_translated)

        for ground_truth, translation in zip(test_clean, test_translated):
            assert len(ground_truth.dialog) == len(translation.dialog)
            for utterance_ground, utterance_translation in zip(ground_truth.dialog, translation.dialog):
                key = list(utterance_ground.keys())[0]
                if key in ["User", "Bot"]:
                    references = [utterance_ground[key].split(" ")]
                    list_of_references.append(references)
                    hypothesis = utterance_translation[key].split(" ")
                    list_of_hypothesis.append(hypothesis)
        print(corpus_bleu(list_of_references, list_of_hypothesis))

