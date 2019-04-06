import json

from sklearn.model_selection import RandomizedSearchCV

class HyperparamGridSearcher():

  def __init__(self, valid_data, logger):
    self.valid_data = valid_data
    self.logger = logger


  def rand_grid_search(self, classifier, hyperparams_grid, num_iterations):

    self.logger.log("Start hyperparameter random grid-search for {}".format(
      type(classifier).__name__))

    random_grid_search = RandomizedSearchCV(estimator = classifier, 
      param_distributions = hyperparams_grid, n_iter = num_iterations, 
      cv = 3, verbose=2, random_state=13, n_jobs = -1)

    random_grid_search.fit(self.valid_data['X'], self.valid_data['y'])
    best_params = random_grid_search.best_params_

    self.logger.log("Hyperparameter random grid-search done", show_time = True)
    self.logger.log("Best params are {}".format(best_params))

    params_filename = type(classifier).__name__ + "_params_" + self.logger.get_time_prefix()
    params_filename += ".json"

    with open(self.logger.get_model_file(params_filename), 'w') as fp:
      json.dump(best_params, fp)