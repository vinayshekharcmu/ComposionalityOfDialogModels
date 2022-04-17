import torch

class BackTranslation():

    def __init__(self):

        # self.english_german_model = torch.hub.load(
        #     'pytorch/fairseq', 'transformer.wmt18.en-de',
        #     checkpoint_file='wmt18.model1.pt:wmt18.model2.pt:wmt18.model3.pt:wmt18.model4.pt:wmt18.model5.pt',
        #     tokenizer='moses', bpe='subword_nmt').cuda()
        #
        # self.german_english_model = torch.hub.load(
        #     'pytorch/fairseq', 'transformer.wmt19.de-en',
        #     checkpoint_file="model1.pt:model2.pt:model3.pt:model4.pt").cuda()

        self.english_russian_model = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.en-ru', checkpoint_file="model1.pt:model2.pt:model3.pt:model4.pt").cuda()
        self.russian_english_model = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.ru-en', checkpoint_file="model1.pt:model2.pt:model3.pt:model4.pt").cuda()

    def _get_sentence(self, model, sentence):
        return model.translate(sentence)

    def get_back_translated_sentence(self, sentence, intermediate_language = "german"):

        if intermediate_language == "german":
            foreign_sentence =  self._get_sentence(self.english_german_model, sentence)
            translated_english_sentence = self._get_sentence(self.german_english_model, foreign_sentence)

        elif intermediate_language == "russian":
            foreign_sentence = self._get_sentence(self.english_russian_model, sentence)
            translated_english_sentence = self._get_sentence(self.russian_english_model, foreign_sentence)

        return translated_english_sentence

if __name__ == "__main__":
    bk = BackTranslation()
    sentence = bk.get_back_translated_sentence("Hello world")
    print(sentence)
