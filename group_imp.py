from sklearn.ensemble import AdaBoostClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier

from features.pos_tags_features import POSTagFeatures
from features.sentence_struct_features import SentenceStructureFeatures
from features.sentence_sentm_features import SentenceSentimentFeatures
from features.original_features import OriginalFeatures
from features.sentence_word_emb import GloVeFeatures


from data_preprocess import generate_final_training_dataset, get_train_test_scores
from logger import Logger

from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.metrics import roc_auc_score, mean_squared_error

import numpy as np
import json

logger = Logger(show = True, html_output = True, config_file = "config.txt")
comm_cols = ['Click_Bait', 'ID']
pos_cols     = POSTagFeatures(logger).end_computing_features()
sent_cols    = SentenceSentimentFeatures(logger).end_computing_features()
struct_cols  = SentenceStructureFeatures(logger).end_computing_features()
sw_cph_cols  = struct_cols[2:4]
struct_cols  = struct_cols[:2] + struct_cols[4:]
emb_cols     = GloVeFeatures(logger).end_computing_features()
orig_cols    = OriginalFeatures(logger).end_computing_features()


def get_only_original(df):
  return df[orig_cols + comm_cols]


def get_only_emb(df):
  return df[emb_cols + comm_cols]


def get_only_struct(df):
  return df[struct_cols + comm_cols]


def get_only_sent(df):
  return df[sent_cols + comm_cols]


def get_only_sw_cph(df):
  return df[sw_cph_cols + comm_cols]


def get_only_pos(df):
  return df[pos_cols + comm_cols]


def get_without_orig(df):
  return df.drop(orig_cols, axis=1)


def get_without_emb(df):
  return df.drop(emb_cols, axis=1)
  

def get_without_sent(df):
  return df.drop(sent_cols, axis=1)


def get_without_struct(df):
  return df.drop(struct_cols, axis=1)


def get_without_sw_cph(df):
  return df.drop(sw_cph_cols, axis=1)


def get_without_pos(df):
  return df.drop(pos_cols, axis=1)


def evaluate_model(model, X_test, y_true, y_score):

  y_pred = model.predict(X_test)
  y_prob = model.predict_proba(X_test)
  y_prob = np.array([elem[1] for elem in y_prob])
  logger.log("Scores snippet {}".format(y_prob[:10]))

  logger.log("Accuracy {}".format(accuracy_score(y_true, y_pred)))
  logger.log("Precision {}".format(precision_score(y_true, y_pred)))
  logger.log("Recall {}".format(recall_score(y_true, y_pred)))
  logger.log("F1 {}".format(f1_score(y_true, y_pred)))
  logger.log("MSE {}".format(mean_squared_error(y_score, y_prob)))
  logger.log("AUC {}".format(roc_auc_score(y_true, y_prob, max_fpr = 0.3)))


def load_architecture():

  ada_params_filename = logger.config_dict['BEST_ADA_L']
  logger.log("Loading params for ADA from {} ...".format(ada_params_filename))
  with open(logger.get_model_file(ada_params_filename, "large")) as fp:
    ada_best_params = json.load(fp)

  ada_model = AdaBoostClassifier(DecisionTreeClassifier())
  ada_model.set_params(**ada_best_params)

  xgb_params_filename = logger.config_dict['BEST_XGB_L']
  logger.log("Loading params for XGB from {} ...".format(xgb_params_filename))
  with open(logger.get_model_file(xgb_params_filename, "large")) as fp:
    xgb_best_params = json.load(fp)

  xgb_model = XGBClassifier()
  xgb_model.set_params(**xgb_best_params)

  ensemble_weights = [0.5, 0.5]

  comb_model = VotingClassifier(estimators = [('ADA', ada_model), ('XGB', xgb_model)],
    voting='soft', weights = ensemble_weights, n_jobs = -1)

  logger.log("Finish loading best architecture {}".format(comb_model))

  return comb_model



CBAIT_SAMP_W = 3.0
if __name__ == '__main__':

  all_df  = generate_final_training_dataset("large", logger)

  crt_model = load_architecture()
  crt_df = all_df
  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(crt_df, 
    test_size = 0.2)
  sample_weight = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]
  logger.log("Training on all features ... {}".format(crt_df.columns.values.tolist()))
  crt_model.fit(X_train, y_train, sample_weight = sample_weight)
  evaluate_model(crt_model, X_test, y_test, y_score)

  logger.log("")

  crt_model = load_architecture()
  crt_df = get_only_original(all_df)
  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(crt_df, 
    test_size = 0.2)
  sample_weight = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]
  logger.log("Training on only original features ... {}".format(crt_df.columns.values.tolist()))
  crt_model.fit(X_train, y_train, sample_weight = sample_weight)
  evaluate_model(crt_model, X_test, y_test, y_score)

  logger.log("")

  crt_model = load_architecture()
  crt_df = get_only_sent(all_df)
  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(crt_df, 
    test_size = 0.2)
  sample_weight = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]
  logger.log("Training on only sentiment features ... {}".format(crt_df.columns.values.tolist()))
  crt_model.fit(X_train, y_train, sample_weight = sample_weight)
  evaluate_model(crt_model, X_test, y_test, y_score)

  logger.log("")


  crt_model = load_architecture()
  crt_df = get_only_struct(all_df)
  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(crt_df, 
    test_size = 0.2)
  sample_weight = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]
  logger.log("Training on only structure features ... {}".format(crt_df.columns.values.tolist()))
  crt_model.fit(X_train, y_train, sample_weight = sample_weight)
  evaluate_model(crt_model, X_test, y_test, y_score)

  logger.log("")

  crt_model = load_architecture()
  crt_df = get_only_emb(all_df)
  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(crt_df, 
    test_size = 0.2)
  sample_weight = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]
  logger.log("Training on only embedding features ... {}".format(crt_df.columns.values.tolist()))
  crt_model.fit(X_train, y_train, sample_weight = sample_weight)
  evaluate_model(crt_model, X_test, y_test, y_score)

  logger.log("")

  crt_model = load_architecture()
  crt_df = get_only_sw_cph(all_df)
  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(crt_df, 
    test_size = 0.2)
  sample_weight = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]
  logger.log("Training on only stopW + cBaitPhr features ... {}".format(crt_df.columns.values.tolist()))
  crt_model.fit(X_train, y_train, sample_weight = sample_weight)
  evaluate_model(crt_model, X_test, y_test, y_score)

  logger.log("")

  crt_model = load_architecture()
  crt_df = get_only_pos(all_df)
  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(crt_df, 
    test_size = 0.2)
  sample_weight = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]
  logger.log("Training on only pos features ... {}".format(crt_df.columns.values.tolist()))
  crt_model.fit(X_train, y_train, sample_weight = sample_weight)
  evaluate_model(crt_model, X_test, y_test, y_score)

  logger.log("")


  crt_model = load_architecture()
  crt_df = get_without_orig(all_df)
  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(crt_df, 
    test_size = 0.2)
  sample_weight = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]
  logger.log("Training without original features ... {}".format(crt_df.columns.values.tolist()))
  crt_model.fit(X_train, y_train, sample_weight = sample_weight)
  evaluate_model(crt_model, X_test, y_test, y_score)

  logger.log("")

  crt_model = load_architecture()
  crt_df = get_without_struct(all_df)
  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(crt_df, 
    test_size = 0.2)
  sample_weight = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]
  logger.log("Training without structure features ... {}".format(crt_df.columns.values.tolist()))
  crt_model.fit(X_train, y_train, sample_weight = sample_weight)
  evaluate_model(crt_model, X_test, y_test, y_score)

  logger.log("")

  crt_model = load_architecture()
  crt_df = get_without_sent(all_df)
  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(crt_df, 
    test_size = 0.2)
  sample_weight = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]
  logger.log("Training without sentiment features ... {}".format(crt_df.columns.values.tolist()))
  crt_model.fit(X_train, y_train, sample_weight = sample_weight)
  evaluate_model(crt_model, X_test, y_test, y_score)

  logger.log("")

  crt_model = load_architecture()
  crt_df = get_without_emb(all_df)
  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(crt_df, 
    test_size = 0.2)
  sample_weight = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]
  logger.log("Training without embedding features ... {}".format(crt_df.columns.values.tolist()))
  crt_model.fit(X_train, y_train, sample_weight = sample_weight)
  evaluate_model(crt_model, X_test, y_test, y_score)

  logger.log("")


  crt_model = load_architecture()
  crt_df = get_without_pos(all_df)
  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(crt_df, 
    test_size = 0.2)
  sample_weight = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]
  logger.log("Training without pos features ... {}".format(crt_df.columns.values.tolist()))
  crt_model.fit(X_train, y_train, sample_weight = sample_weight)
  evaluate_model(crt_model, X_test, y_test, y_score)

  logger.log("")


  crt_model = load_architecture()
  crt_df = get_without_sw_cph(all_df)
  X_train, y_train, X_test, y_test, y_score = get_train_test_scores(crt_df, 
    test_size = 0.2)
  sample_weight = [CBAIT_SAMP_W if int(sample) == 1 else 1 for sample in y_train]
  logger.log("Training without stopW + cBaitPhr features ... {}".format(crt_df.columns.values.tolist()))
  crt_model.fit(X_train, y_train, sample_weight = sample_weight)
  evaluate_model(crt_model, X_test, y_test, y_score)