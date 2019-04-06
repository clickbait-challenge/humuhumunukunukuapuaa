from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from xgboost import XGBClassifier

from hyperparam_tunning import HyperparamGridSearcher
from hyperparams import *

from data_preprocess import generate_final_training_dataset
from logger import Logger

from sklearn.model_selection import train_test_split


DATA_TYPE = "small"

if __name__ == '__main__':

	logger = Logger(show = True, html_output = True, config_file = "config.txt")

	final_df = generate_final_training_dataset(DATA_TYPE, logger)

	X = final_df.iloc[:, :-2].values
	y = final_df.iloc[:, -2].values

	y = (y > 0.5) * 1

	X_train, _, y_train, _ = train_test_split(X, y, random_state = 13, 
		test_size = 0.1 if DATA_TYPE == "small" else 0.2)
	_, X_valid, _, y_valid = train_test_split(X_train, y_train, random_state = 13,
		test_size = 0.2) 

	valid_data = {'X': X_valid, 'y': y_valid}
	grid_searcher = HyperparamGridSearcher(valid_data, logger)

	classifier = AdaBoostClassifier(base_estimator = DecisionTreeClassifier())
	grid_searcher.rand_grid_search(classifier, ada_hyperparams_grid, 200, DATA_TYPE)

	classifier = RandomForestClassifier(n_jobs = -1)
	grid_searcher.rand_grid_search(classifier, randf_hyperparams_grid, 200, DATA_TYPE)

	classifier = DecisionTreeClassifier()
	grid_searcher.rand_grid_search(classifier, randf_hyperparams_grid, 200, DATA_TYPE)

	classifier = XGBClassifier(n_jobs = -1)
	grid_searcher.rand_grid_search(classifier, xgb_hyperparams_grid, 200)