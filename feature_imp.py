from utils.data_preprocess import generate_final_training_dataset
from logger import Logger

import pickle as pkl
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


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


def make_feats_importance_barplot(feats_imp_filename, plot_filename, 
  num_feats_to_plot, logger):

  fig = plt.figure(figsize=(8, 10))
  sns.set()

  df = pd.read_csv(logger.get_output_file(feats_imp_filename))

  model1_feats_imp_scores = df.iloc[0, 1:]
  if len(df) > 1:
    model2_feats_imp_scores = df.iloc[1, 1:]

  model1_name_score_pairs = list(zip(df.columns[1:], model1_feats_imp_scores))
  if len(df) > 1:
    model2_name_score_pairs = list(zip(df.columns[1:], model2_feats_imp_scores))

  model1_name_score_pairs = sorted(model1_name_score_pairs, key=lambda tup: tup[1], reverse = True)
  if len(df) > 1:
    model2_name_score_pairs = sorted(model2_name_score_pairs, key=lambda tup: tup[1], reverse = True)

  model1_names, model1_scores = zip(*model1_name_score_pairs)
  if len(df) > 1:
    model2_names, model2_scores = zip(*model2_name_score_pairs)
    model1_scores = [dict(model1_name_score_pairs)[name] for name in model2_names]

  model1_names = model1_names[:num_feats_to_plot]
  if len(df) > 1:
    model2_names = model2_names[:num_feats_to_plot]

  model1_scores = model1_scores[:num_feats_to_plot]
  if len(df) > 1:
    model2_scores = model2_scores[:num_feats_to_plot]

  x_range = np.array(range(len(model1_names)))

  plt.yticks(fontsize = 15)
  plt.ylabel("Relative importance score", fontsize = 18)

  if len(df) > 1:
    plt.bar(x_range, model2_scores, width = 0.4, color = 'red')
    plt.xticks(x_range, model2_names, rotation = 90, fontsize = 16)
    plt.bar(x_range + 0.4, model1_scores, width = 0.4, color = 'blue')
    plt.legend(["XGBoost", "AdaBoost"], fontsize = 16)
  else:
    plt.bar(x_range, model1_scores, width = 0.6, color = 'red')
    plt.xticks(x_range, model1_names, rotation = 90, fontsize = 16)
    plt.legend(["Randon Forest"], fontsize = 16)

  plt.savefig(logger.get_output_file(plot_filename), dpi = 120, fontsize = 16, bbox_inches='tight')
  plt.close()


# "compute", "plot"
MODE = "plot"

if __name__ == '__main__':

  logger = Logger(show = True, html_output = True, config_file = "config.txt")

  if MODE == "compute":
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

  elif MODE == "plot":

    make_feats_importance_barplot("small_feats_imp.csv", "small_feats_imp_plot.jpg", 10, logger)
    make_feats_importance_barplot("large_feats_imp.csv", "large_feats_imp_plot.jpg", 6, logger)