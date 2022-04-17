import math
import random
from config import  *
from experiments.back_translation import BackTranslation
from pdb import set_trace as bp

class DailyDialog:
    def __init__(self, dialogue):
        self.fold = dialogue[FOLD]
        self.topic = dialogue[TOPIC]

        # dialog here is a list of utterances #Each utterance is given in a form of json
        self.dialog = dialogue[DIALOGUE]


    def serialize(self):
        dict = {}
        dict[FOLD] = self.fold
        dict[TOPIC] = self.topic
        dict[DIALOGUE] = self.dialog
        return dict


    def drop_stop_words(self, fraction_drop=1):
        #AN example to write for other experiments

        for utterance in self.dialog:
            word_list = utterance[TEXT].split()

            stop_indices = [i for i, word in enumerate(word_list) if word.lower() in stop_words]
            to_remove = int(math.ceil(len(stop_indices) * fraction_drop))

            random.shuffle(stop_indices)
            stop_indices = stop_indices[0:to_remove]

            if len(stop_indices) == len(word_list):
                continue

            word_list = [word for i, word in enumerate(word_list) if i not in stop_indices]
            stop_removed_text = ' '.join(word_list)
            utterance[TEXT] = stop_removed_text

    def drop_non_stop_words(self, fraction_drop=1):
        #AN example to write for other experiments

        for utterance in self.dialog:
            word_list = utterance[TEXT].split()

            non_stop_indices = [i for i, word in enumerate(word_list) if word.lower() not in stop_words]
            to_remove = int(math.ceil(len(non_stop_indices) * fraction_drop))

            random.shuffle(non_stop_indices)
            non_stop_indices = non_stop_indices[0:to_remove]

            if len(non_stop_indices) == len(word_list):
                continue

            word_list = [word for i, word in enumerate(word_list) if i not in non_stop_indices]
            non_stop_removed_text = ' '.join(word_list)
            utterance[TEXT] = non_stop_removed_text

    def perform_back_translation(self, back_translation, intermediate_language = "german"):
        for utterance in self.dialog:
            back_translated_sentence = back_translation.get_back_translated_sentence(utterance[TEXT], intermediate_language)
            utterance[TEXT] = back_translated_sentence

    def drop_freq_words(self, term_set, fraction_drop):

        for utterance in self.dialog:
            word_list = utterance[TEXT].split()

            rem_indices = [i for i, word in enumerate(word_list) if word.lower() in term_set]
            to_remove = int(math.ceil(len(rem_indices) * fraction_drop))

            random.shuffle(rem_indices)
            rem_indices = rem_indices[0:to_remove]

            if len(word_list) == len(rem_indices):
                continue

            word_list = [word for i, word in enumerate(word_list) if i not in rem_indices]
            removed_text = ' '.join(word_list)
            utterance[TEXT] = removed_text

    def make_small(self, length = 2):
        self.dialog = self.dialog[:length]

