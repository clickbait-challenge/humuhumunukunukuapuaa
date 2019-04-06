from data_preprocess import generate_final_training_dataset
from logger import Logger

import pickle as pkl
import numpy as np
import pandas as pd


def calculate_feats_importance(model, ensemble_names, feats_names, data_type, logger):

  logger.log("Calculate feature importance for {} data on {}".format(data_type, ensemble_names))
  if len(ensemble_names) > 1:
    clf1_scores = model.estimators_[0].feature_importances_
    clf2_scores = model.estimators_[1].feature_importances_

    clf1_scores = clf1_scores[: - int(logger.config_dict['EMB_SIZE'])]
    clf2_scores = clf2_scores[: - int(logger.config_dict['EMB_SIZE'])]
    clf1_scores /= clf1_scores.max()
    clf2_scores /= clf2_scores.max()
    scores = np.stack([clf1_scores, clf2_scores])
  else:
    clf_scores = model.feature_importances_
    clf_scores = clf_scores[: - int(logger.config_dict['EMB_SIZE'])]
    clf_scores /= clf_scores.max()
    scores = np.stack([clf_scores])

  results_df = pd.DataFrame(scores, columns = feats_names, index = ensemble_names)
  results_df.index.name = "Estimator"
  feats_imp_path = logger.get_output_file(data_type + "_feats_imp.csv")
  logger.log("Save feature importance scores in {}".format(feats_imp_path))
  results_df.to_csv(feats_imp_path)


if __name__ == '__main__':

  logger = Logger(show = True, html_output = True, config_file = "config.txt")

  df = generate_final_training_dataset("small", logger)

  feats_names = df.columns.values
  feats_names = feats_names[:-2]
  feats_names = feats_names[: - int(logger.config_dict['EMB_SIZE'])]

  logger.log("Loading best small model RandF...")
  small_model_path = logger.get_model_file(logger.config_dict['SMALL_BEST'], "small")
  with open(small_model_path, "rb") as fp:
    small_best_model = pkl.load(fp)

  logger.log("Loading best large model Ada + XGB...")
  large_model_path = logger.get_model_file(logger.config_dict['LARGE_BEST'], "large")
  with open(large_model_path, "rb") as fp:
    large_best_model = pkl.load(fp)

  calculate_feats_importance(small_best_model, ["RandF"], feats_names, "small", logger)
  calculate_feats_importance(large_best_model, ["Ada", "XGB"], feats_names, "large", logger)