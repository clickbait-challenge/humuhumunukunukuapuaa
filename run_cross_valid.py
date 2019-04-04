from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from xgboost import XGBClassifier

from data_preprocess import generate_final_training_dataset
from logger import Logger

from sklearn.model_selection import train_test_split

from cross_valid import CrossValidation

import json

from sklearn.utils import shuffle

from xgboost import XGBRegressor

import pickle as pkl

MODE = "randf"


if __name__ == '__main__':

  logger = Logger(show = True, html_output = True, config_file = "config.txt")

  final_df = generate_final_training_dataset("large", logger)
  final_df = shuffle(final_df)

  X = final_df.iloc[:, :-2].values
  y = final_df.iloc[:, -2].values

  print(X.shape)

  with open(logger.get_model_file(logger.config_dict['BEST_XGB_L'], "large"), "r") as fp:
    best_params = json.load(fp)
  best_params['max_depth'] = 8

  model =  XGBRegressor(n_jobs = -1, verbose = 1, **best_params)
  model.fit(X, y)

  with open("best_model.pkl", "wb") as fp:
    pkl.dump(model, fp)


  '''
  X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 13, 
    test_size = 0.1)
  '''



  ''''

  data = {'X': X_train, 'y': y_train}
  cross_valider = CrossValidation(data, 10, logger)

  if MODE == "ada":
    with open(logger.get_model_file(logger.config_dict['BEST_ADA_L'], "large"), "r") as fp:
      best_params = json.load(fp)

    model = AdaBoostClassifier(base_estimator = DecisionTreeClassifier())
    model.set_params(**best_params)
    print(model)
    cross_valider.evaluate_model(model)
  elif MODE == "randf":
    with open(logger.get_model_file(logger.config_dict['BEST_RANDF_L'], "large"), "r") as fp:
      best_params = json.load(fp)
      
    model = RandomForestClassifier()
    model.set_params(**best_params)
    print(model)
    cross_valider.evaluate_model(model)
  elif MODE == "dectree":
    with open(logger.get_model_file(logger.config_dict['BEST_DECT_L'], "large"), "r") as fp:
      best_params = json.load(fp)
      
    model = DecisionTreeClassifier()
    model.set_params(**best_params)
    print(model)
    cross_valider.evaluate_model(model)
  elif MODE == "xgb":
    with open(logger.get_model_file(logger.config_dict['BEST_XGB_L'], "large"), "r") as fp:
      best_params = json.load(fp)
      
    model = XGBClassifier()
    #model.set_params(**best_params)
    #print(model)
    cross_valider.evaluate_model(model)
  '''