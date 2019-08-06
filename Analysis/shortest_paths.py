# script for generating shortest paths and path lengths

# import

# connect to database

# initialize ORM object/table relationship class

# get origin and destination lists

# load network from pickle

# for each item in origin list

	# for each item in destination list

		# try

			# shortest path

			# shortest path length

			# push object to database

		# except

				# O and D are not connected

				# push Null to DB 





# test

import osmnx as osmnx
import networkx
import pickle

file = 'pickles/london_bike_1_projected_pickle.file'

net = pickle.load(open(file, "rb" ))

origin = 652813798
destination = 1236955052


# could use dijkstra or Bellman-ford algo for finding path


check = networkx.has_path(net, origin, destination)
# https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.has_path.html#networkx.algorithms.shortest_paths.generic.has_path

# https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.shortest_paths.weighted.dijkstra_path.html#networkx.algorithms.shortest_paths.weighted.dijkstra_path

# shortest_path_length = networkx.dijkstra_path_length(net, origin, destination, weight = ??)

# https://networkx.github.io/documentation/stable/reference/algorithms/shortest_paths.html


# shortest_path_nodes = networkx.dijkstra_path(net, origin, destination, weight = ?????)


# NetworkX algorithms designed for weighted graphs cannot use multigraphs directly because it is not 
# clear how to handle multiedge weights. Convert to Graph using edge attribute ‘weight’ to enable 
# weighted graph algorithms.