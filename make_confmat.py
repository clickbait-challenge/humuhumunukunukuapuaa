from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pickle as pkl
import numpy as np


from utils.data_preprocess import generate_final_training_dataset
from logger import Logger


def plot_confusion_matrix(cm,
                          target_names,
                          plt_filename,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=True):
  """
    Citiation - adapted from:
    ---------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

  """
  import matplotlib.pyplot as plt
  import itertools

  if cmat.shape[0] == 2:
    tp = cm[0][0]
    fn = cm[0][1]
    fp = cm[1][0]
    tn = cm[1][1]
  
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

  accuracy = np.trace(cm) / float(np.sum(cm))
  misclass = 1 - accuracy

  if cmap is None:
    cmap = plt.get_cmap('Blues')

  plt.figure(figsize=(8, 6))
  plt.imshow(cm, interpolation='nearest', cmap=cmap)
  plt.title(title)
  plt.colorbar()

  if target_names is not None:
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)

  if normalize:
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


  thresh = cm.max() / 1.5 if normalize else cm.max() / 2
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    if normalize:
      plt.text(j, i, "{:0.2f}".format(cm[i, j]),
              horizontalalignment="center",
              color="white" if cm[i, j] > thresh else "black")
    else:
      plt.text(j, i, "{:,}".format(cm[i, j]),
              horizontalalignment="center",
              color="white" if cm[i, j] > thresh else "black")

  plt.ylabel('True label')
  plt.xlabel('Predicted label\nPrecision={:0.4f}; Recall={:0.4f}'.format(precision, recall))
    
  plt.savefig(plt_filename, dpi = 120, bbox_inches='tight')
  plt.close()


if __name__ == "__main__":

  logger = Logger(show = True, html_output = True, config_file = "config.txt")

  df = generate_final_training_dataset("small", logger)
  X = df.iloc[:, :-2].values
  y = df.iloc[:, -2].values
  _, X_test, _, y_test = train_test_split(X, y, random_state = 13, 
    test_size = 0.1)
  y_test = (y_test > 0.5) * 1
  logger.log("Loading best small model RandF...")
  small_model_path = logger.get_model_file(logger.config_dict['SMALL_BEST'], "small")
  with open(small_model_path, "rb") as fp:
    small_best_model = pkl.load(fp)
  logger.log("Done loading", show_time = True)

  y_pred = small_best_model.predict(X_test)
  cmat = confusion_matrix(y_test, y_pred, labels = [1, 0])
  plot_confusion_matrix(cmat, ["ClickBait", "Not ClickBait"], 
    logger.get_output_file("small_cmat.jpg"), normalize = False, 
    title = "")

  df = generate_final_training_dataset("large", logger)
  X = df.iloc[:, :-2].values
  y = df.iloc[:, -2].values
  _, X_test, _, y_test = train_test_split(X, y, random_state = 13, 
    test_size = 0.2)
  y_test = (y_test > 0.5) * 1
  logger.log("Loading best large model Ada + XGB...")
  large_model_path = logger.get_model_file(logger.config_dict['LARGE_BEST'], "large")
  large_model_path = logger.get_model_file('VotingClassifier_4.0_0.0957_2019-04-08_21_05_51.pkl', "large")
  with open(large_model_path, "rb") as fp:
    large_best_model = pkl.load(fp)

  y_pred = large_best_model.predict(X_test)
  cmat = confusion_matrix(y_test, y_pred, labels = [1, 0])
  plot_confusion_matrix(cmat, ["ClickBait", "Not ClickBait"], 
    logger.get_output_file("large_cmat.jpg"), normalize = False, 
    title = "")