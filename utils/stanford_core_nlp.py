from nltk.parse.corenlp import CoreNLPDependencyParser, CoreNLPParser


class StanfordCoreNLP():

  def __init__(self, logger):

    self.logger = logger
   
  def create_parser(self):

    self.parser = CoreNLPParser(url = 'http://localhost:9000/')
    return self.parser


  def create_dependency_parser(self):

    self.dep_parser = CoreNLPDependencyParser(url = 'http://localhost:9000/')
    return self.dep_parser


  def create_pos_tagger(self):

    self.tagger = CoreNLPParser(tagtype = 'pos', url = 'http://localhost:9000/')
    return self.tagger


  def close_server(self):

    self.logger("Closing server wrapper")