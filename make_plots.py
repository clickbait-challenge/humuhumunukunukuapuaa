import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from logger import Logger
from data_preprocess import generate_data

from collections import Counter

def plot_scores_distribution(plt_filename, dataset, logger):

  click_bait_scores = [elem['clickBaitScore'] for elem in dataset]
  occurences = dict(Counter(click_bait_scores)).items()
  occurences = sorted(occurences, key=lambda tup: tup[1], reverse = True)

  sns.set()

  x = np.array(range(len(occurences)))
  y = [item[1] for item in occurences]

  fig = plt.figure(figsize=(10, 8))
  plt.bar(x, y, color = 'blue')

  my_xticks = ["{:.2f}".format(item[0]) for item in occurences]
  plt.xticks(x, my_xticks, rotation = 90, fontsize = 11)
  plt.yticks(fontsize = 11)
  plt.xlabel("Click-bait scores", fontsize = 13)
  plt.ylabel("Count", fontsize = 13)

  for pos_x, pos_y in zip(x, y):
    plt.text(pos_x - 0.5, pos_y + 0.8, str(pos_y), fontsize = 9)

  plt.savefig(logger.get_output_file(plt_filename), dpi = 120, bbox_inches='tight')
  plt.close()


if __name__ == '__main__':

  logger = Logger(show = True, html_output = True, config_file = "config.txt")
  dataset = generate_data("large", logger)
  
  plot_scores_distribution("large_scores_distribution.jpg", dataset, logger)