# script for generating shortest paths and path lengths

# import

import osmnx as ox
import networkx
import pickle
import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, Float, Sequence, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
import pandas as pd
from datetime import datetime 



########################################################################################################
# connect to database

engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')

# initialize ORM object/table relationship class

Base = declarative_base(engine)
metadata = sqlalchemy.MetaData()

class undirected_travel_time_2(Base):

	__tablename__ = 'undirected_travel_times_2'

	pidddd = Column(Integer, Sequence('pidddd'), primary_key=True)
	net_filter = Column(Integer)
	origin = Column(BigInteger)
	destination = Column(BigInteger)
	has_path = Column(Boolean)
	distance = Column(Float)

class nearest_nodes(Base):

	__table__ = sqlalchemy.Table('nearest_node', metadata, autoload=True, autoload_with=engine)


Base.metadata.create_all(engine)

# test_travel_time = travel_time(net_filter = 'bike_1', origin = 652813798, destination = 1236955052, has_path = True, distance = 101.101)

Session = sessionmaker(bind=engine)

session = Session()

# after this line, the data in test_travel_time is "pending"
# still separate from the DB
# session.add(travel_time)

# now commit the outstanding data/session status
# session.commit()

####################################################################################################

def net_dict():
	file_dict = {}
	for i in range(2,3):
		# print(i)
		file_dict[i] = 'pickles/undirected_london_bike_' + str(i) + '_projected_pickle.file'
		# print(file_dict[i])
	return file_dict


def trip_calc(net, origin, dest):

	# check_path = networkx.has_path(net, origin, destination)

	if networkx.has_path(net, origin, destination):

		# path = networkx.shortest_path(net, origin, destination, weight='length')
		path_length = networkx.shortest_path_length(net, origin, destination, weight='length')
		calced_data = undirected_travel_time_2(origin = origin, destination = destination, has_path = True, distance = path_length)

	else: 
	
		calced_data = undirected_travel_time_2(origin = origin, destination = destination, has_path = False)


	return calced_data



# net_dict = net_dict()
# print(net_dict)


# file_dict['1'] = 'pickles/london_bike_1_projected_pickle.file'
# file_dict['2'] = 'pickles/london_bike_2_projected_pickle.file'
# file_dict['3'] = 'pickles/london_bike_3_projected_pickle.file'
# file_dict['4'] = 'pickles/london_bike_4_projected_pickle.file'
# file_dict['5'] = 'pickles/london_bike_5_projected_pickle.file'

####################################################################################################

# get origin and destination lists
sql = 'select lsoa11cd, nearest_common_node from nearest_node'
nodes_df = pd.read_sql(sql, con = engine) 
print(nodes_df.head(2))

# load network from pickle

# file = 'pickles/london_bike_1_projected_pickle.file'

# net = pickle.load(open(file, "rb" ))

node_id_list = list(nodes_df['nearest_common_node'])
p_id = 0
# debug_limit = 10
net_dict = net_dict()

start = datetime.now()

print('start time was: ', start)

for key, value in net_dict.items():

	print('key: ', key)
	print('type of key: ', type(key))
	print('value: ', value)
	# debug_limit = p_id + 10

	net = pickle.load(open(value, "rb" ))
	print(type(net))

# for each item in origin list

	for origin_count, origin in enumerate(node_id_list):
		
		results_list = []

		# if p_id > debug_limit:
			# break

		for dest_count, destination in enumerate(node_id_list):

			if origin == destination:
				# print('matchy matchy')
				continue

			# print('id: ', p_id)
			# print('origin: ', origin)
			# print('destination: ', destination)

			# if p_id > debug_limit:
				# break

			###############################################################
			# calc data for O/D pair

			results_list.append(trip_calc(net, origin, destination))
			# results_list[dest_count] = trip_calc(net, origin, destination)


			# print('list len: ', len(results_list))
			# print('counter: ', dest_count)
			results_list[dest_count-1].net_filter = key
			# print("trip object filter value: ", trip.net_filter)
			# print('distance: ', trip.distance)

			# p_id = p_id + 1

			#####################
			# send to sql DB

			session.add(results_list[dest_count-1])

		# commit everything in the results list.
		print('adding origin ', origin_count, 'to the db') 	
		session.commit()


end = datetime.now()

print('start: ', start)
print('end: ', end)

print('elapse: ', (end - start))

	# for each item in destination list


		# try

			# shortest path

			# shortest path length

			# push object to database

		# except

				# O and D are not connected

				# push Null to DB 





# test

######################################################################################################

# file = 'pickles/london_bike_1_projected_pickle.file'

# net = pickle.load(open(file, "rb" ))

# origin = 652813798
# destination = 1236955052


# # could use dijkstra or Bellman-ford algo for finding path


# check = networkx.has_path(net, origin, destination)

# test_path = networkx.shortest_path(net, origin, destination, weight='length')

# test_path_length = networkx.shortest_path_length(net, origin, destination, weight='length')

# fig, ax = ox.plot_graph_route(net, test_path, node_size=0)

######################################################################################################



# route_map = ox.plot_route_folium(net, test_path)


# https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.has_path.html#networkx.algorithms.shortest_paths.generic.has_path

# https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.shortest_paths.weighted.dijkstra_path.html#networkx.algorithms.shortest_paths.weighted.dijkstra_path

# shortest_path_length = networkx.dijkstra_path_length(net, origin, destination, weight = ??)

# https://networkx.github.io/documentation/stable/reference/algorithms/shortest_paths.html


# shortest_path_nodes = networkx.dijkstra_path(net, origin, destination, weight = ?????)


# NetworkX algorithms designed for weighted graphs cannot use multigraphs directly because it is not 
# clear how to handle multiedge weights. Convert to Graph using edge attribute ‘weight’ to enable 
# weighted graph algorithms.

# code for converting a multigraph into a graph with weights
# https://stackoverflow.com/questions/15590812/networkx-convert-multigraph-into-simple-graph-with-weighted-edges#15598279



# osmnx example seems to think nx.shortest_path can handle whatever OSMNX builds from OSM. 
# classes

# multidigraph 
# 
