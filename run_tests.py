from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from xgboost import XGBClassifier

from data_preprocess import generate_final_training_dataset
from logger import Logger


from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.metrics import roc_auc_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

import pickle as pkl
import numpy as np

from hyperparams.params import *


def get_train_test_scores(df, test_size):

  X = final_df.iloc[:, :-2].values
  y = final_df.iloc[:, -2].values

  X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 13, 
    test_size = test_size)

  y_score = np.copy(y_test)
  y_train = (y_train > 0.5) * 1
  y_test  = (y_test > 0.5) * 1

  return X_train, y_train, X_test, y_test, y_score


def run_model(model, params, sample_weight, logger):

  model.set_params(**params)
  logger.log("Start training {} with {}".format(type(model).__name__, params))
  model.fit(X_train, y_train, sample_weight = sample_weight)
  logger.log("Finish training", show_time = True)

  return model


def evaluate_model(model, y_true, y_score, logger):

  y_pred = model.predict(X_test)
  y_prob = model.predict_proba(X_test)
  y_prob = np.array([elem[1] for elem in y_prob])

  logger.log("Accuracy {}".format(accuracy_score(y_test, y_pred)))
  logger.log("Precision {}".format(precision_score(y_test, y_pred)))
  logger.log("Recall {}".format(recall_score(y_test, y_pred)))
  logger.log("F1 {}".format(f1_score(y_test, y_pred)))
  logger.log("MSE {}".format(mean_squared_error(y_score, y_prob)))
  logger.log("AUC {}".format(roc_auc_score(y_test, y_prob)))


# "small", "large", "custom"
DATA_TYPE = "large"
CBAIT_SAMP_W = 3.5

if __name__ == '__main__':

  logger = Logger(show = True, html_output = True, config_file = "config.txt")

  if DATA_TYPE == "custom":
    final_df  = generate_final_training_dataset("large", logger)
    custom_df = generate_final_training_dataset("custom", logger)
  else:
    final_df = generate_final_training_dataset(DATA_TYPE, logger)

  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(final_df, 
    test_size = 0.1 if DATA_TYPE == "small" else 0.2)
  logger.log("Splitting data in {} train / {} test".format(y_train.shape[0], y_test.shape[0]))

  logger.log("Assign {} weight to clickBaits".format(CBAIT_SAMP_W))
  samples_weights = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]

  if DATA_TYPE == "custom":
    X_custom = custom_df.iloc[:, :-2].values
    y_custom = custom_df.iloc[:, -2].values

    logger.log("Add {} entries from custom data to training".format(y_custom.shape[0]))
    X_train = np.concatenate([X_train, X_custom], axis = 0)
    y_train = np.concatenate([y_train, y_custom], axis = 0)

    logger.log("Assign {} weight to custom data".format(0.5))
    samples_weights += [0.5 for _ in y_custom]


  model = DecisionTreeClassifier()
  best_params = small_dect_params if DATA_TYPE == "small" else large_dect_params
  if DATA_TYPE == "custom":
    samples_weights[:-y_custom.shape[0]] = [large_dect_w if int(
      sample) == 1 else 1 for sample in y_train[:-y_custom.shape[0]]]
  else:
    dtype_dect_w = small_dect_w if DATA_TYPE == "small" else large_dect_w
    samples_weights = [dtype_dect_w if int(sample) == 1 else 1 for sample in y_train]

  model = run_model(model, best_params, samples_weights, logger)
  evaluate_model(model, y_test, y_score, logger)


  model = AdaBoostClassifier(DecisionTreeClassifier())
  best_params = small_ada_params if DATA_TYPE == "small" else large_ada_params
  if DATA_TYPE == "custom":
    samples_weights[:-y_custom.shape[0]] = [large_ada_w if int(
      sample) == 1 else 1 for sample in y_train[:-y_custom.shape[0]]]
  else:
    dtype_ada_w = small_ada_w if DATA_TYPE == "small" else large_ada_w
    samples_weights = [dtype_ada_w if int(sample) == 1 else 1 for sample in y_train]

  model = run_model(model, best_params, samples_weights, logger)
  evaluate_model(model, y_test, y_score, logger)


  model = RandomForestClassifier()
  best_params = small_randf_params if DATA_TYPE == "small" else large_randf_params
  best_params['n_jobs'] = -1
  if DATA_TYPE == "custom":
    samples_weights[:-y_custom.shape[0]] = [large_randf_w if int(
      sample) == 1 else 1 for sample in y_train[:-y_custom.shape[0]]]
  else:
    dtype_randf_w = small_randf_w if DATA_TYPE == "small" else large_randf_w
    samples_weights = [dtype_randf_w if int(sample) == 1 else 1 for sample in y_train]

  model = run_model(model, best_params, samples_weights, logger)
  evaluate_model(model, y_test, y_score, logger)


  model = XGBClassifier()
  best_params = small_xgb_params if DATA_TYPE == "small" else large_xgb_params
  best_params['n_jobs'] = -1
  if DATA_TYPE == "custom":
    samples_weights[:-y_custom.shape[0]] = [large_xgb_w if int(
      sample) == 1 else 1 for sample in y_train[:-y_custom.shape[0]]]
  else:
    dtype_xgb_w = small_xgb_w if DATA_TYPE == "small" else large_xgb_w
    samples_weights = [dtype_xgb_w if int(sample) == 1 else 1 for sample in y_train]

  model = run_model(model, best_params, samples_weights, logger)
  evaluate_model(model, y_test, y_score, logger)