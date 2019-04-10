from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from utils.data_preprocess import generate_final_training_dataset, get_train_test_scores
from logger import Logger

from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.metrics import roc_auc_score, mean_squared_error
from sklearn.model_selection import train_test_split

import pickle as pkl
import numpy as np
import sklearn
import json


def run_model(model, params, X_train, y_train, sample_weight, logger):

  model.set_params(**params)
  logger.log("Start training {} with {} ...".format(type(model).__name__, params))
  model.fit(X_train, y_train, sample_weight = sample_weight)
  logger.log("Finish training", show_time = True)

  return model


def evaluate_model(model, X_test, y_true, y_score, logger, data_type):

  y_pred = model.predict(X_test)
  y_prob = model.predict_proba(X_test)
  y_prob = np.array([elem[1] for elem in y_prob])

  logger.log("Scores snippet {}".format(y_prob[:15]))
  logger.log("Accuracy {}".format(accuracy_score(y_true, y_pred)))
  logger.log("Precision {}".format(precision_score(y_true, y_pred)))
  logger.log("Recall {}".format(recall_score(y_true, y_pred)))
  logger.log("F1 {}".format(f1_score(y_true, y_pred)))
  logger.log("MSE {}".format(mean_squared_error(y_score, y_prob)))
  logger.log("AUC {}".format(roc_auc_score(y_true, y_prob, max_fpr = 0.3)))

  model_filename  = type(model).__name__ + "_" + str(CBAIT_SAMP_W)
  model_filename += "_" + "{:.4f}".format(mean_squared_error(y_score, y_prob))
  model_filename += "_" + logger.get_time_prefix()
  model_filename += ".pkl"

  logger.log("Saving model to {} ...".format(model_filename))
  with open(logger.get_model_file(model_filename, data_type), "wb") as fp:
    pkl.dump(model, fp)


def load_params(model_prefix, data_type, logger):

  params_filename = logger.config_dict[model_prefix + ("_S" if data_type == "small" else "_L")]
  logger.log("Loading params for {} from {} ...".format(model_prefix, params_filename))
  with open(logger.get_model_file(params_filename, data_type)) as fp:
    best_params = json.load(fp)

  return best_params


# "small", "large", "custom"
DATA_TYPE = "large"
CBAIT_SAMP_W = 4

if __name__ == '__main__':

  logger = Logger(show = True, html_output = True, config_file = "config.txt")

  if DATA_TYPE == "custom":
    final_df  = generate_final_training_dataset("large", logger)
    custom_df = generate_final_training_dataset("custom", logger)
  else:
    final_df = generate_final_training_dataset(DATA_TYPE, logger)

  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(final_df, 
    test_size = 0.1 if DATA_TYPE == "small" else 0.1)
  logger.log("Splitting data in {} train / {} test".format(y_train.shape[0], y_test.shape[0]))

  logger.log("Assign {} weight to clickBaits".format(CBAIT_SAMP_W))
  samples_weights = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]

  if DATA_TYPE == "custom":
    X_custom = custom_df.iloc[:, :-2].values
    y_custom = custom_df.iloc[:, -2].values

    logger.log("Add {} entries from custom data to training".format(y_custom.shape[0]))
    X_train = np.concatenate([X_train, X_custom], axis = 0)
    y_train = np.concatenate([y_train, y_custom], axis = 0)

    logger.log("Assign {} weight to custom data".format(2.0))
    samples_weights += [2.0 for _ in y_custom]

  dect_model = DecisionTreeClassifier()
  best_params = load_params("BEST_DECT", DATA_TYPE if DATA_TYPE == "small" else "large", logger)
  dect_model = run_model(dect_model, best_params, X_train, y_train, samples_weights, logger)
  evaluate_model(dect_model, X_test, y_test, y_score, logger, DATA_TYPE)


  ada_model = AdaBoostClassifier(DecisionTreeClassifier())
  best_params = load_params("BEST_ADA", DATA_TYPE if DATA_TYPE == "small" else "large", logger)
  ada_model = run_model(ada_model, best_params, X_train, y_train, samples_weights, logger)
  evaluate_model(ada_model, X_test, y_test, y_score, logger, DATA_TYPE)

  randf_model = RandomForestClassifier()
  best_params = load_params("BEST_RANDF",DATA_TYPE if DATA_TYPE == "small" else "large", logger)
  best_params['n_jobs'] = -1
  randf_model = run_model(randf_model, best_params, X_train, y_train, samples_weights, logger)
  evaluate_model(randf_model, X_test, y_test, y_score, logger, DATA_TYPE)


  xgb_model = XGBClassifier()
  best_params = load_params("BEST_XGB", DATA_TYPE if DATA_TYPE == "small" else "large", logger)
  best_params['n_jobs'] = -1
  xgb_model = run_model(xgb_model, best_params, X_train, y_train, samples_weights, logger)
  evaluate_model(xgb_model, X_test, y_test, y_score, logger, DATA_TYPE)

  dect_model  = sklearn.base.clone(dect_model)
  ada_model   = sklearn.base.clone(ada_model)
  randf_model = sklearn.base.clone(randf_model)
  xgb_model   = sklearn.base.clone(xgb_model)

  if DATA_TYPE == "small":
    ensemble_names = ["ADA", "RANDF"]
    ensemble_weights = [0.5, 0.5]
    comb_model = VotingClassifier(estimators = [('ADA', ada_model), ('RANDF', randf_model)],
      voting='soft', weights = ensemble_weights, n_jobs = -1)
  else:
    ensemble_names = ["ADA", "XGB"]
    ensemble_weights = [0.5, 0.5]
    comb_model = VotingClassifier(estimators = [('ADA', ada_model), ('XGB', xgb_model)],
      voting='soft', weights = ensemble_weights, n_jobs = -1)
  

  logger.log("Start training average ensemble {} with {} ...".format(
    ensemble_names, ensemble_weights))
  comb_model.fit(X_train, y_train, samples_weights)
  logger.log("Finish training average ensemble", show_time = True)

  evaluate_model(comb_model, X_test, y_test, y_score, logger, DATA_TYPE)