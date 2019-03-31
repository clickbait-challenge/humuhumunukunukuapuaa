from features.pos_tags_features import POSTagFeatures
from features.sentence_struct_features import SentenceStructureFeatures
from features.sentence_sentm_features import SentenceSentimentFeatures
from features.sentence_word_emb import GloVeFeatures

from tqdm import tqdm
import pandas as pd
import traceback

from data_preprocess import generate_data
from logger import Logger


pos_extractor = None
structure_extractor = None

def generate_training_data(dataset, file_to_save, logger):
 
  try:
    pos_extractor = POSTagFeatures(logger)
    sentiment_extractor = SentenceSentimentFeatures(logger)
    structure_extractor = SentenceStructureFeatures(logger)
    glove_extractor = GloVeFeatures(logger)

    features_list = []
    logger.log("Start calculating features ...")
    for row in tqdm(dataset):
      crt_feats = []
      crt_sentence = row['postText'][-1]

      crt_feats  = [row['id']]
      crt_feats += pos_extractor.compute_features_per_sentence(crt_sentence)
      crt_feats += sentiment_extractor.compute_features_per_sentence(crt_sentence)
      crt_feats += structure_extractor.compute_features_per_sentence(crt_sentence)
      crt_feats += glove_extractor.compute_features_per_sentence(crt_sentence)

      features_list.append(crt_feats)
  except:
    traceback.print_exc()
    logger.log("Error generated at {}".format(row['postText'][-1]))
    pos_extractor.core_nlp.close_server()
    structure_extractor.core_nlp.close_server()
  
  logger.log("Finish calculating {} features for {} entries".format(
    len(features_list[-1]) -1, len(features_list)), show_time = True)

  colnames  = ["ID"]
  colnames += pos_extractor.end_computing_features()
  colnames += sentiment_extractor.end_computing_features()
  colnames += structure_extractor.end_computing_features()
  colnames += glove_extractor.end_computing_features()  

  df = pd.DataFrame(features_list, columns = colnames)
  logger.log("Features dataframe snippet \n {}".format(df.head()))
  file_to_save = logger.get_data_file(file_to_save)
  logger.log("Save features to {}".format(file_to_save))
  df.to_csv(file_to_save, index = False)

  return df

if __name__ == '__main__':

  logger = Logger(show = True, html_output = True, config_file = "config.txt")
  small_dataset = generate_data("small", logger)  
  small_df = generate_training_data(small_dataset[:15], "small_train.csv", logger)
  
  '''
  large_dataset = generate_data(logger.config_dict[''], logger.config_dict[''])
  '''
  '''
  large_df = generate_training_data(large_dataset, logger)
  '''