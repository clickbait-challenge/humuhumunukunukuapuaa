from sklearn.manifold import TSNE

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from logger import Logger
from utils.data_preprocess import generate_data

def compute_tsne(original_array, logger):

	logger.log("Start TSNE for {} vectors of {}d ...".format(
		len(original_array), len(original_array[0])))
	tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, 
		random_state=13, verbose = 2)
	new_array = tsne_model.fit_transform(original_array)
	logger.log("Finish TSNE", show_time = True)

	filename = "TSNE_" + logger.get_time_prefix() + ".npy"
	logger.log("Saving 2D arrays to {}".format(filename))
	np.save(logger.get_output_file(filename), new_array)

	return new_array


def plot_tsne(reduced_2d_array, scores, logger):

	x = [elem[0] for elem in reduced_2d_array]
	y = [elem[1] for elem in reduced_2d_array]

	sns.set()
	fig = plt.figure(figsize=(25, 25))

	cmap = sns.cubehelix_palette(12, as_cmap=True)
	plt.scatter(x, y, c=scores, s=50, cmap='jet')
	plt.colorbar()
	plt.savefig(logger.get_output_file("tsne.jpg"), dpi = 120, bbox_inches='tight')
	plt.close()


if __name__ == '__main__':

	logger = Logger(show = True, html_output = True, config_file = "config.txt")
	dataset = generate_data("small", logger)

	scores = [elem['clickBaitScore'] for elem in dataset]
	emb_colnames = ["EMB_" + str(i) for i in range(1, 101)]

	df = pd.read_csv(logger.get_data_file("small_train.csv"))
	original_array = df[emb_colnames].values.tolist()

	new_array = compute_tsne(original_array, logger)
	'''
	new_array = np.load(logger.get_output_file("TSNE_2019-04-04_03_16_50.npy"))
	new_array = new_array.tolist()
	'''
	plot_tsne(new_array, scores, logger)