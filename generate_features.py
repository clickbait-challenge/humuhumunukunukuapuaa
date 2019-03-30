'''
from features import gen_feat1, ..., gen_featsn
'''

'''
CODE UNDER CONSTRUCTION. Nothing to see here yet
'''


from data_preprocess import generate_data

from logger import Logger

import pandas as pd

def generate_training_data(dataset, logger):
  # call all features methods
  # create pandas dataframe
  # save it as csv 
  pass

if __name__ == '__main__':

  logger = Logger(config = "config.txt")
  small_dataset = generate_data(logger.config_dict['folder'], 
    logger.config_dict['data_file'], logger.config_dict['target_file'])
  large_dataset = generate_data(logger.config_dict[''], logger.config_dict[''])

  small_df = generate_training_data(small_dataset, logger)
  large_df = generate_training_data(large_dataset, logger)












