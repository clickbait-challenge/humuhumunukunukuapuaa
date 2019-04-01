from nltk.parse.corenlp import CoreNLPServer
from nltk.parse.corenlp import CoreNLPDependencyParser, CoreNLPParser

import nltk

class StanfordCoreNLP():

  def __init__(self, logger, nlp_options):

    self.logger = logger
    self.nlp_options = nlp_options
    '''
    nltk.internals.config_java(bin = logger.config_dict['JAVA_PATH'], 
      options = ["-Xmx1024m"])
    '''
    #self._create_server()


  def _create_server(self):

    stanford_jar = self.logger.get_data_file(self.logger.config_dict['STANFORD_JAR'])
    stanford_models_jar = self.logger.get_data_file(self.logger.config_dict['STANFORD_MODELS_JAR'])

    self.server = CoreNLPServer(stanford_jar, stanford_models_jar, 
      corenlp_options = self.nlp_options)
    self.server.start()


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
    pass
    #self.server.stop()