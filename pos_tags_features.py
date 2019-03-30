from stanford_core_nlp import StanfordCoreNLP
import numpy as np

class POSTagFeatures():

  def __init__(self, logger):
    self.logger = logger
    self._corenlp_server_init()
    self.tags = None


  def _core_nlp_server_init(self):

    self.core_nlp = StanfordCoreNLP(logger)
    self.parser = self.core_nlp.create_parser()
    self.tagger = self.core_nlp.create_pos_tagger()


  def _check_tags_is_computed(self, text):
    if self.tags is None:
      self.words = self.parser.tokenize(text)
      self.tags  = [elem[1] for elem in list(self.tagger.tag(words))]
      self.core_nlp.close_server()


  def get_pnouns_proportion(self, text):

    self._check_tags_is_computed(text)
    pnouns_count  = sum(np.array(self.tags) == "NNP")
    pnouns_count += sum(np.array(self.tags) == "NNPS")

    return [pnouns_count / len(self.words)]


  def get_adverbs_determiners(self, text):

    self._check_tags_is_computed(text)
    adverbs_determiners_count  = sum(np.array(self.tags) == "RB")
    adverbs_determiners_count += sum(np.array(self.tags) == "DT")
    adverbs_determiners_count += sum(np.array(self.tags) == "WDT")

    return [adverbs_determiners_count / len(self.words)]


  def get_per_pos_pronouns(self, text):

    self._check_tags_is_computed(text)
    per_pos_pronouns_count  = sum(np.array(self.tags) == "PRP")
    per_pos_pronouns_count += sum(np.array(self.tags) == "PRP$")

    return [per_pos_pronouns_count / len(self.words)]


  def get_past_3rdpsing_verbs(self, text):

    self._check_tags_is_computed(text)
    past_3rdpsing_verbs_count  = sum(np.array(self.tags) == "VBN")
    past_3rdpsing_verbs_count += sum(np.array(self.tags) == "VBZ")

    return [past_3rdpsing_verbs_count / len(self.words)]