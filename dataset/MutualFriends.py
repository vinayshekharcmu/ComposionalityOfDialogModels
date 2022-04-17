import math
import random
from config import  *
from experiments.back_translation import BackTranslation

from pdb import set_trace as bp

class MutualFriends:
    def __init__(self, dialogue):
        self.uuid = dialogue[UUID]
        self.scenario = dialogue[SCENARIO]
        self.scenario_uuid = dialogue[SCENARIO_UUID]
        self.agents = dialogue[AGENTS]
        self.outcome = dialogue[OUTCOME]
        self.dialog = dialogue[EVENTS]

    def serialize(self):
        dict = {}
        dict[UUID] = self.uuid
        dict[SCENARIO] = self.scenario
        dict[SCENARIO_UUID] = self.scenario_uuid
        dict[AGENTS] = self.agents
        dict[OUTCOME] = self.outcome
        dict[EVENTS] = self.dialog
        return dict


    def perform_back_translation(self, back_translation, intermediate_language="german"):
        for action_dict in self.dialog:

            if action_dict['action'] == "message":
                text = action_dict['data']
                back_translated_sentence = back_translation.get_back_translated_sentence(text, intermediate_language)
                action_dict['data'] = back_translated_sentence

    def drop_stop_words(self, fraction_drop=1):

        for action_dict in self.dialog:

            if action_dict['action'] == 'message':

                word_list = action_dict['data'].split()

                stop_indices = [i for i, word in enumerate(word_list) if word.lower() in stop_words]
                to_remove = int(math.ceil(len(stop_indices) * fraction_drop))

                random.shuffle(stop_indices)
                stop_indices = stop_indices[0:to_remove]

                word_list = [word for i, word in enumerate(word_list) if i not in stop_indices]
                stop_removed_text = ' '.join(word_list)
                action_dict['data'] = stop_removed_text

    def drop_non_stop_words(self, fraction_drop=1):

        for action_dict in self.dialog:

            if action_dict['action'] == 'message':

                word_list = action_dict['data'].split()

                non_stop_indices = [i for i, word in enumerate(word_list) if word.lower() not in stop_words]
                to_remove = int(math.ceil(len(non_stop_indices) * fraction_drop))

                random.shuffle(non_stop_indices)
                non_stop_indices = non_stop_indices[0:to_remove]

                word_list = [word for i, word in enumerate(word_list) if i not in non_stop_indices]
                non_stop_removed_text = ' '.join(word_list)
                action_dict['data'] = non_stop_removed_text

    def make_dialog_empty(self):

        bp()
        for action_dict in self.dialog:

            if action_dict['action'] == 'message':

                word_list = action_dict['data'].split()

                stop_indices = [i for i, word in enumerate(word_list)]
                to_remove = int(math.ceil(len(stop_indices)))

                random.shuffle(stop_indices)
                stop_indices = stop_indices[0:to_remove]

                word_list = [word for i, word in enumerate(word_list) if i not in stop_indices]
                stop_removed_text = ' '.join(word_list)
                action_dict['data'] = stop_removed_text

    def make_small(self, length=2):

        len_count = 0
        for action_dict in self.dialog:
            if action_dict['action'] == 'message':

                len_count += 1

                if(len_count > length):
                    word_list = action_dict['data'].split()

                    stop_indices = [i for i, word in enumerate(word_list)]
                    to_remove = int(math.ceil(len(stop_indices)))

                    random.shuffle(stop_indices)
                    stop_indices = stop_indices[0:to_remove]

                    word_list = [word for i, word in enumerate(word_list) if i not in stop_indices]
                    stop_removed_text = ' '.join(word_list)
                    action_dict['data'] = stop_removed_text


    def drop_freq_words(self, term_set, fraction_drop):

        for action_dict in self.dialog:

            if action_dict['action'] == 'message':

                word_list = action_dict['data'].split()

                rem_indices = [i for i, word in enumerate(word_list) if word.lower() in term_set]
                to_remove = int(math.ceil(len(rem_indices) * fraction_drop))

                random.shuffle(rem_indices)
                rem_indices = rem_indices[0:to_remove]

                word_list = [word for i, word in enumerate(word_list) if i not in rem_indices]
                removed_text = ' '.join(word_list)
                action_dict['data'] = removed_text
