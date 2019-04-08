from nltk import word_tokenize

class OriginalFeatures():

  def __init__(self, logger):
    self.logger = logger
    self.colnames = ['PostTitleWordsNumber', 'PostTitleCharsNumber',
      'DiffNoWordsPostTitleAndKeywords', 'DiffNoCharsPostTitleAndKeywords',
      'RatioNoWordsArticleDescriptionAndPostTitle',
      'QuestionMarksNoPostTitle', 'RatioNoCharArticleParagraphPostTitle',
      'RatioNoCharArticleDescriptionPostTitle', 'RatioNoCharArticleTitlePostTitle',
      'RatioNoWordsArticleTitlePostTitle', 'RatioNoWordsPostImagePostTitle',
      'DiffCharsPostTitlePostImage', 'RatioCharPostImagePostTitle', 'FormalWordsPostTitle',
      'RatioNoCharArticleParagraphArticleDescription']
    self.logger.log("Init sentence structure feats extractor with feats list: {}".format(
      self.colnames))

  '''
  @return list of features
  '''
  def compute_features_per_entry(self, data_dict):
    pass


  def end_computing_features(self):
    return self.colnames



