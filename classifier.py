#! /home/humuhumunukunukuapuaa/anaconda3/envs/nlp/bin/python3

from features.pos_tags_features import POSTagFeatures
from features.sentence_struct_features import SentenceStructureFeatures
from features.sentence_sentm_features import SentenceSentimentFeatures
from features.sentence_word_emb import GloVeFeatures

from features.originalFeatures import meld_with_original_features
from features.originalFeatures import column_names as originalfeatures_name
from features.text_image_extract import extract_info

import argparse, sys
import pandas as pd
import pickle as pkl

from logger import Logger

import json
import os

from time import sleep


def start_server():
    os.popen(
        'java -mx1524m -cp "stanford-corenlp-full-2018-10-05/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,parse,depparse -status_port 9000 -port 9000 -timeout 300000 &')


def generate_data(path_to_file, logger):
    data = []

    logger.log("Start reading data file from {} ...".format(path_to_file))
    data_file = open(path_to_file, mode="r", encoding="utf8")
    for line in data_file:
        data.append(json.loads(line))
    data_file.close()
    logger.log("Finish reading", show_time=True)

    return data


def generate_test_data(data, logger, media_path):
    pos_extractor = POSTagFeatures(logger)
    sentiment_extractor = SentenceSentimentFeatures(logger)
    structure_extractor = SentenceStructureFeatures(logger)
    glove_extractor = GloVeFeatures(logger)

    features_list = []
    logger.log("Start calculating features ...")
    for row in data:
        crt_feats = []
        crt_sentence = row['postText'][-1]

        crt_feats = [row['id']]
        crt_feats += pos_extractor.compute_features_per_sentence(crt_sentence)
        crt_feats += sentiment_extractor.compute_features_per_sentence(crt_sentence)
        crt_feats += structure_extractor.compute_features_per_sentence(crt_sentence)
        crt_feats += glove_extractor.compute_features_per_sentence(crt_sentence)

        features_list.append(crt_feats)

    image_meta = extract_info(media_path)
    meld_with_original_features(data, image_meta, features_list)

    logger.log("Finish calculating {} features for {} entries".format(
        len(features_list[-1]) - 1, len(features_list)), show_time=True)

    colnames = ["ID"]
    colnames += pos_extractor.end_computing_features()
    colnames += sentiment_extractor.end_computing_features()
    colnames += structure_extractor.end_computing_features()
    colnames += glove_extractor.end_computing_features()

    colnames.extend(originalfeatures_name)

    df = pd.DataFrame(features_list, columns=colnames)

    return df


def load_model(logger):
    model_filename = logger.config_dict['BEST_MODEL']
    with open(logger.get_model_file(model_filename), "rb") as fp:
        model = pkl.load(fp)

        return model


if __name__ == '__main__':

    logger = Logger(show=True, html_output=True, config_file="config.txt")

    start_server()
    sleep(70)

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str)
    parser.add_argument('--output', '-o', type=str)

    args = parser.parse_args()

    data = generate_data(os.path.join(args.input, "instances.jsonl"), logger)

    test_df = generate_test_data(data, logger, os.path.join(args.input, "media"))
    del data

    X_test = test_df.iloc[:, 1:].values
    model = load_model(logger)
    logger.log("Load best model {}".format(model))

    logger.log("Start predicting on test data ...")
    y_pred = model.predict_proba(X_test)
    y_pred = [elem[1] for elem in y_pred]
    logger.log("Finish predicting, snippet of scores: {}".format(
        y_pred[:10]), show_time=True)

    ids = test_df.ID.values

    logger.log("Save results...")
    with open(os.path.join(args.output, "results.jsonl"), "w") as fp:
        for i in range(len(y_pred)):
            json.dump({'id': str(ids[i]), 'clickbaitScore': float(y_pred[i])}, fp)
            fp.write(os.linesep)
    logger.log("Done saving", show_time=True)
    logger.close()
