from config import *
import math
import random
import html

class Babi:
    def __init__(self, babi_dialog):
        self.dialog = []
        for line in babi_dialog:
            if RESTO in line:
                self.dialog.append({"Options" : line})
            else:
                user_utterance = line.split("\t")[0]
                bot_utterance = line.split("\t")[1]
                if SILENCE in user_utterance:
                    self.dialog.append({"User_Silence": user_utterance})
                    self.dialog.append({"API" : bot_utterance})
                else:
                    self.dialog.append({"User" : user_utterance})
                    self.dialog.append({"Bot" : bot_utterance})

    def serialize(self):
        output_list = []
        i = 0
        while i < len(self.dialog):
            if "Options" in self.dialog[i]:
                output_list.append(self.dialog[i]["Options"])
                i += 1
            else:
                # The space before the tab is a hack to make ParlAi not throw error for empty strings

                turn = list(self.dialog[i].values())[0] + " \t" + list(self.dialog[i + 1].values())[0]
                output_list.append(turn)
                i += 2

        return output_list

    def drop_stop_words(self, fraction_drop = 1):
        for action_dict in self.dialog:
            key = list(action_dict.keys())[0]
            if key in ["User", "Bot"]:
                word_list = action_dict[key].split()

                stop_indices = [i for i, word in enumerate(word_list) if word.lower() in stop_words]
                to_remove = int(math.ceil(len(stop_indices) * fraction_drop))

                random.shuffle(stop_indices)
                stop_indices = stop_indices[0:to_remove]

                word_list = [word for i, word in enumerate(word_list) if i not in stop_indices]
                stop_removed_text = ' '.join(word_list)

                action_dict[key] = stop_removed_text

    def drop_non_stop_words(self, fraction_drop = 1):
        for action_dict in self.dialog:
            key = list(action_dict.keys())[0]
            if key in ["User", "Bot"]:
                word_list = action_dict[key].split()
                id = word_list[0]
                word_list = word_list[1:]

                non_stop_indices = [i for i, word in enumerate(word_list) if word.lower() not in stop_words]
                to_remove = int(math.ceil(len(non_stop_indices) * fraction_drop))

                random.shuffle(non_stop_indices)
                non_stop_indices = non_stop_indices[0:to_remove]

                word_list = [word for i, word in enumerate(word_list) if i not in non_stop_indices]
                if len(word_list) == 0:
                    continue

                word_list = [id] + word_list
                non_stop_removed_text = ' '.join(word_list)

                action_dict[key] = non_stop_removed_text

    def make_small(self, length=2):

        len_count = 0
        for action_dict in self.dialog:
            key = list(action_dict.keys())[0]
            if key in ["User", "Bot"]:

                len_count += 1

                if(len_count > length):
                    word_list = action_dict[key].split()

                    stop_indices = [i for i, word in enumerate(word_list)]
                    to_remove = int(math.ceil(len(stop_indices)))

                    random.shuffle(stop_indices)
                    stop_indices = stop_indices[0:to_remove]

                    word_list = [word for i, word in enumerate(word_list) if i not in stop_indices]
                    stop_removed_text = ' '.join(word_list)
                    action_dict[key] = stop_removed_text

    def drop_freq_words(self, term_set, fraction_drop):

        for action_dict in self.dialog:
            key = list(action_dict.keys())[0]
            if key in ["User", "Bot"]:
                word_list = action_dict[key].split()

                rem_indices = [i for i, word in enumerate(word_list) if word.lower() in term_set]
                to_remove = int(math.ceil(len(rem_indices) * fraction_drop))

                random.shuffle(rem_indices)
                rem_indices = rem_indices[0:to_remove]

                word_list = [word for i, word in enumerate(word_list) if i not in rem_indices]

                removed_text = ' '.join(word_list)
                action_dict[key] = removed_text

    def perform_back_translation(self, back_translation, intermediate_language = "german"):
        for action_dict in self.dialog:
            key = list(action_dict.keys())[0]
            if key in ["User", "Bot"]:
                if key == "Bot":
                    back_translated_sentence = back_translation.get_back_translated_sentence(action_dict[key], intermediate_language)
                else:
                    line_num = action_dict[key].split(" ")[0]
                    back_translated_sentence = back_translation.get_back_translated_sentence(action_dict[key].split(" ")[1], intermediate_language)
                    back_translated_sentence = line_num + " " + back_translated_sentence
                action_dict[key] = back_translated_sentence

    def clean_translation(self):
        for action_dict in self.dialog:
            key = list(action_dict.keys())[0]
            if key in ["User", "Bot"]:
                action_dict[key] = html.unescape(action_dict[key])
                action_dict[key] = action_dict[key].replace("\'", "'")
                if "@" in action_dict[key]:
                    cleaned_sentence = action_dict[key].split("@@ ")
                    cleaned_sentence = "".join(cleaned_sentence)
                    action_dict[key] = cleaned_sentence
