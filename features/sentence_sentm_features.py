from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from nltk.corpus import opinion_lexicon
from nltk import word_tokenize


class SentenceSentimentFeatures():

  def __init__(self, logger):

    self.logger = logger
    self.colnames = ["VaderS_Neg", "VaderS_Neu", "VaderS_Pos", "Opinion_Pos", "Opinion_Neg"]
    self.logger.log("Init sentence sentiment feats extractor with feats list: {}".format(self.colnames))


  def _get_vader_scores(self, text):

    vader_analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = vader_analyzer.polarity_scores(text)
    return [sentiment_scores["neg"], sentiment_scores["neu"], sentiment_scores["pos"]]


  def _get_pos_neg_words_count(self, text):

    words = word_tokenize(text)
    pos_opinion_count = len(set(opinion_lexicon.positive()) & set(words))
    neg_opinion_count = len(set(opinion_lexicon.negative()) & set(words))

    return [pos_opinion_count, neg_opinion_count]


  def compute_features_per_sentence(self, text):

    if len(text) == 0:
      return [-1 for i in range(len(self.colnames))]

    feats  = self._get_vader_scores(text)
    feats += self._get_pos_neg_words_count(text)

    return feats


  def end_computing_features(self):

    return self.colnames
