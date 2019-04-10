from sklearn.feature_selection import mutual_info_classif

import pandas as pd

from utils.data_preprocess import generate_final_training_dataset
from logger import Logger

if __name__ == '__main__':

  logger = Logger(show = True, html_output = True, config_file = "config.txt")

  final_df = generate_final_training_dataset("large", logger)
  final_df.drop(['EMB_' + str(i) for i in range(1, 101)], axis = 1, inplace = True)

  X = final_df.iloc[:, :-2].values
  y = final_df.iloc[:, -2].values

  y = (y > 0.5) * 1

  mutual_info = mutual_info_classif(X, y)
  mutual_info /= mutual_info.max()

  mutual_info_pair = zip(final_df.columns.values[:-2], mutual_info)
  mutual_info_pair = sorted(mutual_info_pair, key=lambda tup: tup[1], reverse = True)

  feats_names, mutual_info = zip(*mutual_info_pair)

  results = pd.DataFrame([mutual_info], columns = feats_names)
  results.to_csv(logger.get_output_file("large_mutual_info.csv"), index = False)