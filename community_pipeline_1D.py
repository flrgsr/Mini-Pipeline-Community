import numpy as np
import pandas as pd
import networkx as nx
import os
import sys
sys.path.append("..")
import louvain

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
	        if filenames.index(file) == 0:
	            analyse_community(graph)
	    print 'done'


def analyse_community(graph):
	dendrogram = louvain.generate_dendrogram(graph)
	print 'number of levels ' + str(len(dendrogram))
	print len(set(louvain.partition_at_level(dendrogram, 1)))
	print len(set(louvain.partition_at_level(dendrogram, len(dendrogram) - 1 )))

if __name__ == '__main__':
	run_mini_pipeline()