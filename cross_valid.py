from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, make_scorer
from sklearn.model_selection import cross_validate

import numpy as np

class CrossValidation():

  def __init__(self, data, k_folds, logger):
    self.logger = logger
    self.data = data
    self.k_folds = k_folds
    self.scoring = {'accuracy': 'accuracy', 
                    'precision': 'precision',
                    'recall':  'recall',
                    'f1': 'f1'
                   }


  def evaluate_model(self, model):

    self.logger.log("Start {}-fold cross validation on {} entries".format(
      self.k_folds, self.data['y'].shape[0]))
    scores = cross_validate(model, self.data['X'], self.data['y'],
      scoring = self.scoring, cv = self.k_folds, return_train_score = True,
      verbose = 2, n_jobs = -1)
    self.logger.log("Finished cross validation", show_time = True)

    print(scores.keys())

    self.logger.log("Mean accuracy {}".format(np.average(scores['test_accuracy'])))
    self.logger.log("Mean precision {}".format(np.average(scores['test_precision'])))
    self.logger.log("Mean recall {}".format(np.average(scores['test_recall'])))
    self.logger.log("Mean f1 {}".format(np.average(scores['test_f1'])))