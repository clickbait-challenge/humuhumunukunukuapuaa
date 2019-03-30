from nltk.parse.corenlp import CoreNLPServer
from nltk.parse.corenlp import CoreNLPDependencyParser, CoreNLPParser

import nltk

class StanfordCoreNLP():

  def __init__(self, logger):
    self.logger = logger
    nltk.internals.config_java(logger.config_dict['JAVA_PATH'])

    self._create_server()

  def _create_server(self):
    stanford_jar = self.logger.get_data_file(self.logger.config_dict['STANFORD_JAR'])
    stanford_models_jar = self.logger.get_data_file(self.logger.config_dict['STANFORD_MODELS_JAR'])

    self.server = CoreNLPServer(stanford_jar, stanford_models_jar)
    self.server.start()

  def create_parser(self):
    self.parser = CoreNLPParser()
    return self.parser

  def create_dependency_parser(self):
    self.dep_parser = CoreNLPDependencyParser()
    return self.parser

  def create_pos_tagger(self):
    self.tagger = CoreNLPParser(tagtype = 'pos')
    return self.tagger

  def close_server(self):
    self.server.stop()






