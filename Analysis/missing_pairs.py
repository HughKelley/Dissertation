# import

import pandas as pd 
import pickle
import osmnx as ox 
import networkx
import csv
import sqlalchemy



engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')


# load network from pickle
file = 'pickles/undirected_london_bike_2_projected_pickle.file'
net = pickle.load(open(file, 'rb'))

print('net type: ', type(net))

# load missing pairs from sql

sql = 'select * from missing_u_2'

pairs = pd.read_sql(sql, con=engine)

print('column names: ', list(pairs))

print('shape: ', pairs.shape)

print('head: ', pairs.head(5))


for index, row in pairs.iterrows():

	# print('row: ', row)
	origin = row['origin_node_id']	
	dest = row['dest_node_id']
	# print('origin: ', origin)
	# print('dest: ', dest)
	# print(index)

	if networkx.has_path(net, origin, dest):
		dist = networkx.shortest_path_length(net, origin, dest, weight='length')
		
		data_row = pd.DataFrame([{'origin':origin, 'dest':dest, 'distance':dist}])

		data_row.to_sql('missing_calc_u_2', con = engine, if_exists='append')

		# data_row = [origin, dest, dist]
		# csv_file.write(origin, dest, dist)


