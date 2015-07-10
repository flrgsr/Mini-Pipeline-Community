import numpy as np
import pandas as pd
import networkx as nx
import os
import sys
sys.path.append("..")
import louvain

import matplotlib.pyplot as plt
import matplotlib.colors as colors

def run_mini_pipeline():
	datadir = 'data'
	for root, dirs, filenames in os.walk(datadir):
		for file in filenames:
			print 'computing subject ' + str(filenames.index(file))
			file_handle = os.path.join(root, file)
			df = pd.read_csv(file_handle, sep='\t')
			np_ts_matrix=df.as_matrix()
			correlation_matrix = np.corrcoef(np_ts_matrix.T)
			threshold = 0.6
			correlation_matrix[correlation_matrix<threshold] = 0
			correlation_matrix[correlation_matrix != 0] = 1
			graph = nx.from_numpy_matrix(correlation_matrix)
			if filenames.index(file) != float('inf'):
				save_name = 'subject ' + str(filenames.index(file))
				analyse_community(graph, save_name)
		print 'done'


def analyse_community(graph, save_name):
	partition = louvain.best_partition(graph)    
	nx.set_node_attributes(graph, 'community', partition)
	drawNetwork(graph, save_name)



def drawNetwork(G, save_name):
	# position map
	pos = nx.spring_layout(G)
	# community ids
	communities = [v for k,v in nx.get_node_attributes(G, 'community').items()]
	numCommunities = max(communities) + 1
	# color map from http://colorbrewer2.org/
	cmapLight = colors.ListedColormap(['#a6cee3', '#b2df8a', '#fb9a99', '#fdbf6f', '#cab2d6'], 'indexed', numCommunities)
	cmapDark = colors.ListedColormap(['#1f78b4', '#33a02c', '#e31a1c', '#ff7f00', '#6a3d9a'], 'indexed', numCommunities)

	# edges
	nx.draw_networkx_edges(G, pos)

	# nodes
	nodeCollection = nx.draw_networkx_nodes(G,
		pos = pos,
		node_color = communities,
		cmap = cmapLight
	)
	# set node border color to the darker shade
	darkColors = [cmapDark(v) for v in communities]
	nodeCollection.set_edgecolor(darkColors)

	# Print node labels separately instead
	for n in G.nodes_iter():
		plt.annotate(n,
			xy = pos[n],
			textcoords = 'offset points',
			horizontalalignment = 'center',
			verticalalignment = 'center',
			xytext = [0, 2],
			color = cmapDark(communities[n])
		)

	plt.axis('off')
	plt.savefig('figures/' + save_name)
	# plt.show()
	plt.clf()

if __name__ == '__main__':
	run_mini_pipeline()