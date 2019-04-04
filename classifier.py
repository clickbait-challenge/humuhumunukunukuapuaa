from features.pos_tags_features import POSTagFeatures
from features.sentence_struct_features import SentenceStructureFeatures
from features.sentence_sentm_features import SentenceSentimentFeatures
from features.sentence_word_emb import GloVeFeatures

import argparse, sys
import pandas as pd
import pickle as pkl

from logger import Logger

import json
import os


def start_server():
  from time import sleep
  os.popen('java -mx2g -cp "stanford-corenlp-full-2018-10-05/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,parse,depparse -status_port 9000 -port 9000 -timeout 500000 &> /dev/null')
  sleep(15)


def generate_data(path_to_file, logger):

  data = []
  
  logger.log("Start reading data file from {} ...".format(path_to_file))
  data_file = open(path_to_file, mode = "r", encoding = "utf8")
  for line in data_file:
    data.append(json.loads(line))
  data_file.close()
  logger.log("Finish reading", show_time = True)

  return data


def generate_test_data(data, logger):

  pos_extractor = POSTagFeatures(logger)
  sentiment_extractor = SentenceSentimentFeatures(logger)
  structure_extractor = SentenceStructureFeatures(logger)
  glove_extractor = GloVeFeatures(logger)

  features_list = []
  logger.log("Start calculating features ...")
  for row in tqdm(data):
    crt_feats = []
    crt_sentence = row['postText'][-1]

    crt_feats  = [row['id']]
    crt_feats += pos_extractor.compute_features_per_sentence(crt_sentence)
    crt_feats += sentiment_extractor.compute_features_per_sentence(crt_sentence)
    crt_feats += structure_extractor.compute_features_per_sentence(crt_sentence)
    crt_feats += glove_extractor.compute_features_per_sentence(crt_sentence)

    features_list.append(crt_feats)

  logger.log("Finish calculating {} features for {} entries".format(
    len(features_list[-1]) -1, len(features_list)), show_time = True)

  colnames  = ["ID"]
  colnames += pos_extractor.end_computing_features()
  colnames += sentiment_extractor.end_computing_features()
  colnames += structure_extractor.end_computing_features()
  colnames += glove_extractor.end_computing_features()  

  df = pd.DataFrame(features_list, columns = colnames)


def load_model(model_filename, logger):

  with open(logger.get_model_file(model_filename), "rb") as fp:
    model = pkl.load(fp)

    return model


if __name__ == '__main__':

  logger = Logger(show = True, html_output = True, config_file = "config.txt")

  parser = argparse.ArgumentParser()
  parser.add_argument('--input', '-i', type = str)
  parser.add_argument('--output', '-o', type = str)

  args = parser.parse_args()

  data = generate_data(args.input, logger)

  start_server()

  test_df = generate_test_data(data, logger)
  del data

  X_test = test_df.iloc[:, 1:].values

  model = load_model("best_model.pkl", logger)

  y_pred = model.predict_proba(X_test)
  y_pred = [elem[1] for elem in y_pred]

  ids = test_df.ID.values

  with open(args.output, "w") as fp:
    for i in range(len(y_pred)):
      json.dump({'id': str(ids[i]), 'clickbaitScore': y_pred[i]})
      fp.write(os.linesep)