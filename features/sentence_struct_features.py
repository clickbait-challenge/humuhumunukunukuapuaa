from utils.stanford_core_nlp import StanfordCoreNLP

from nltk.corpus import stopwords
import numpy as np
import re


class SentenceStructureFeatures():

  def __init__(self, logger):
    self.logger = logger
    self.parser_tree = None
    self.words = None
    self.colnames = ["WordLen_Avg", "Start_Digit", "Num_StopW", 
      "CBait_Phrase", "Synt_DepMax", "Synt_DepAvg"]
    self.logger.log("Init sentence structure feats extractor with feats list: {}".format(
      self.colnames))
    self._core_nlp_server_init()


  def _core_nlp_server_init(self):

    self.core_nlp = StanfordCoreNLP(self.logger)
    self.parser = self.core_nlp.create_parser()
    self.dep_parser = self.core_nlp.create_dependency_parser()


  def _compute_using_server(self, text):

    self.words = list(self.parser.tokenize(text))
    self.words = [str.lower(word) for word in self.words]
    self.parser_tree = next(self.dep_parser.raw_parse(text))
      

  def _get_average_word_length(self, text):

    words_lenght = sum([len(word) for word in set(self.words)])

    return [words_lenght / len(set(self.words))]


  def _get_start_digit(self, text):

    return [int(str.isdigit(text[0]))]


  def _get_num_stopwords(self, text):

    num_stopwords = len([word for word in set(self.words) if word in stopwords.words('english')])

    return [num_stopwords]


  def _get_common_bit_phrase(self, text):

    with open(self.logger.get_data_file(self.logger.config_dict['DOWNWORTHY_FILE']), "r") as fp:
      phrases = fp.read().split('\n')

    phrases = [phrase.strip().lower() for phrase in phrases if phrase != '']
    num_contained_phrases = 0
    for phrase in phrases:
      if list(re.finditer(r'\b%s\b' % re.escape(phrase), text.lower())) != []:
        return [1]

    return [0]
    

  def _get_max_length_syntactic_dependencies(self, text):

    num_entries = len(self.parser_tree.nodes)
    distances = [abs(entry - self.parser_tree.nodes[entry]["head"]) for entry in range(1, num_entries)]

    return [max(distances)]


  def _get_avg_length_syntactic_dependencies(self, text):

    num_entries = len(self.parser_tree.nodes)
    distances = [abs(entry - self.parser_tree.nodes[entry]["head"]) for entry in range(1, num_entries)]

    return [sum(distances) / (num_entries - 1)]


  def compute_features_per_sentence(self, text):

    if len(text) == 0:
      return [-1 for i in range(len(self.colnames))]

    self._compute_using_server(text)
    feats  = self._get_average_word_length(text)
    feats += self._get_start_digit(text)
    feats += self._get_num_stopwords(text)
    feats += self._get_common_bit_phrase(text)
    feats += self._get_max_length_syntactic_dependencies(text)
    feats += self._get_avg_length_syntactic_dependencies(text)

    return feats


  def get_server_instance(self):
    
    return self.core_nlp.server


  def end_computing_features(self):

    self.core_nlp.close_server()
    
    return self.colnames