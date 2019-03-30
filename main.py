'''
CODE UNDER CONSTRUCTION. Nothing to see here yet
'''


from data_preprocess import generate_data
from logger import Logger

logger = Logger(show = True, html_output = True, config_file = "config.txt")
#small_dataset = generate_data("small", logger)
#large_dataset = generate_data("large", logger)


from stanford_core_nlp import StanfordCoreNLP

stanford_cnlp = StanfordCoreNLP(logger)
parser = stanford_cnlp.create_dependency_parser()
tagger = stanford_cnlp.create_pos_tagger()

