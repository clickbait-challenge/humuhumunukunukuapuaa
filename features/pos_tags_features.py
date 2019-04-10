from utils.stanford_core_nlp import StanfordCoreNLP

import numpy as np


class POSTagFeatures():

  def __init__(self, logger):
    self.logger = logger
    self.tags = None
    self.words = None
    self.colnames = ["Prop_Nouns", "Advb_Determ", "PerPos_Pronouns", "Past3rdSing_Verbs"]
    self.logger.log("Init POS feats extractor with feats list: {}".format(self.colnames))
    self._core_nlp_server_init()


  def _core_nlp_server_init(self):

    self.core_nlp = StanfordCoreNLP(self.logger)
    self.parser = self.core_nlp.create_parser()
    self.tagger = self.core_nlp.create_pos_tagger()
    

  def _compute_using_server(self, text):
    
    self.words = list(self.parser.tokenize(text))
    self.tags  = [elem[1] for elem in list(self.tagger.tag(self.words))]


  def _get_prop_nouns(self, text):

    pnouns_count  = sum(np.array(self.tags) == "NNP")
    pnouns_count += sum(np.array(self.tags) == "NNPS")

    return [pnouns_count / len(self.words)]


  def _get_adverbs_determiners(self, text):

    adverbs_determiners_count  = sum(np.array(self.tags) == "RB")
    adverbs_determiners_count += sum(np.array(self.tags) == "DT")
    adverbs_determiners_count += sum(np.array(self.tags) == "WDT")

    return [adverbs_determiners_count / len(self.words)]


  def _get_per_pos_pronouns(self, text):

    per_pos_pronouns_count  = sum(np.array(self.tags) == "PRP")
    per_pos_pronouns_count += sum(np.array(self.tags) == "PRP$")

    return [per_pos_pronouns_count / len(self.words)]


  def _get_past_3rdpsing_verbs(self, text):

    past_3rdpsing_verbs_count  = sum(np.array(self.tags) == "VBN")
    past_3rdpsing_verbs_count += sum(np.array(self.tags) == "VBZ")

    return [past_3rdpsing_verbs_count / len(self.words)]


  def compute_features_per_sentence(self, text):

    if len(text) == 0:
      return [-1 for i in range(len(self.colnames))]

    self._compute_using_server(text)
    feats  = self._get_prop_nouns(text)
    feats += self._get_adverbs_determiners(text)
    feats += self._get_per_pos_pronouns(text)
    feats += self._get_past_3rdpsing_verbs(text)

    return feats


  def get_server_instance(self):
    
    return self.core_nlp.server


  def end_computing_features(self):
    
    self.core_nlp.close_server()

    return self.colnames