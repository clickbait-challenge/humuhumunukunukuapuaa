from stanford_core_nlp import StanfordCoreNLP

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import opinion_lexicon, stopwords

import numpy as np


class SentenceStructureFeatures():

  def __init__(self, logger):
    self.logger = logger
    self._corenlp_server_init()
    self.parser_tree = None

  def _core_nlp_server_init(self):

    self.core_nlp = StanfordCoreNLP(logger)
    self.parser = self.core_nlp.create_parser()
    self.dep_parser = self.core_nlp.create_dependency_parser()


  def _check_parser_tree_is_computed(self, text):
    if self.parser_tree is None:
      self.words = self.parser.tokenize(text)
      self.words = [str.lower(word) for words in self.words]
      self.parser_tree = self.dep_parser.raw_parse(text)


  def get_vader_scores(self, text):

    sentiment_scores = vader_analyzer.polarity_scores(text)
    return [sentiment_scores["neg"], sentiment_scores["neu"], sentiment_scores["pos"]]


  def get_pos_neg_words_count(self, text):

    self._check_parser_tree_is_computed(text)
    pos_opinion_count = len(set(opinion_lexicon.positive()) & set(self.words))
    neg_opinion_count = len(set(opinion_lexicon.negative()) & set(self.words))

    return [pos_opinion_count, neg_opinion_count]


  def get_average_word_length(self, text):

    self._check_parser_tree_is_computed(text)
    words_lenght = sum([len(word) for word in set(self.words)])

    return [words_lenght / len(set(self.words))]


  def get_start_digit(self, text):
    return [str.isdigit(text[0])]


  def get_num_stopwords(self, text):

    self._check_parser_tree_is_computed(text)
    num_stopwords = len([word for word in set(self.words) if word in stopwords.words('english')])

    return [num_stopwords]


  def get_common_bit_phrase(self, text):

    with open(self.logger.config_dict['DOWNWORTHY_FILE'], "r") as fp:
      phrases = fp.read().split('\n')

    phrases = [phrase.strip().lower() for phrase in phrases]
    num_contained_phrases = [phrase for phrase in phrases is phrase in text.lower()]

    return int(num_contained_phrases != 0)


  def get_max_length_syntactic_dependencies(self, text):

    self._check_parser_tree_is_computed(text)
    num_entries = len(self.parser_tree.nodes)
    distances = [abs(entry - self.parser_tree.nodes[entry]["head"]) for entry in num_entries]

    return [max(distances)]


  def get_avg_length_syntactic_dependencies(self, text):

    self._check_parser_tree_is_computed(text)
    num_entries = len(self.parser_tree.nodes)
    distances = [abs(entry - self.parser_tree.nodes[entry]["head"]) for entry in num_entries]

    return [sum(distances) / (num_entries - 1)]



    

