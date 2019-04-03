from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from xgboost import XGBClassifier

from hyperparam_tunning import HyperparamGridSearcher
from hyperparams import *

from data_preprocess import generate_final_training_dataset
from logger import Logger

from sklearn.model_selection import train_test_split


MODE = "ada"

if __name__ == '__main__':

	logger = Logger(show = True, html_output = True, config_file = "config.txt")

	final_df = generate_final_training_dataset("small", logger)

	X = final_df.iloc[:, :-2].values
	y = final_df.iloc[:, -2].values

	X_train, X_valid, y_valid, y_valid = train_test_split(X, y, random_state = 13, 
		test_size = 0.1)

	valid_data = {'X': X_valid, 'y': y_valid}
	grid_searcher = HyperparamGridSearcher(valid_data, logger)

	if MODE == "ada":
		classifier = AdaBoostClassifier(base_estimator = DecisionTreeClassifier())
		grid_searcher.rand_grid_search(classifier, ada_hyperparams_grid, 200)
	elif MODE == "randf":
		classifier = RandomForestClassifier()
		grid_searcher.rand_grid_search(classifier, randf_hyperparams_grid, 200)
	elif MODE == "dectree":
		classifier = DecisionTreeClassifier()
		grid_searcher.rand_grid_search(classifier, dectree_hyperparams_grid, 200)
	elif MODE == "xgb":
		classifier = XGBClassifier()
		grid_searcher.rand_grid_search(classifier, xgb_hyperparams_grid, 200)