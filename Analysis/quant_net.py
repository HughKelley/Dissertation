import networkx as nx
import pandas as pd
import pickle
import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')


sql = 'select * from clean_quant_subset_times'

df = pd.read_sql(sql, con=engine)

print(type(df))
print(df.shape)

print(df.head(10))

# need to separate columns and stack into full repetitive edge list. 

df_transit = df[['origin','destination', 'travel_time_mins']].copy()
df_walking = df[['origin','destination', 'walking_time_mins']].copy()

df_transit.rename(columns={'origin':'origin', 'destination':'destination', 'travel_time_mins':'time'}, inplace=True)
print('transit shape: ', df_transit.shape)

df_walking.rename(columns={'origin':'origin', 'destination':'destination', 'walking_time_mins':'time'}, inplace=True)
print('walking shape: ', df_walking.shape)

df_edges = df_transit.append(df_walking)
print('edges shape: ', df_edges.shape)

# drop NaN's
df_edges = df_edges.dropna()

print('edges shape after drop: ', df_edges.shape)




# G = nx.MultiDiGraph()

# # nx.to_networkx_graph()

# >>> G.add_edge(1, 2)
# >>> e = (2, 3)
# >>> G.add_edge(*e)  # unpack edge tuple*

graph = nx.from_pandas_edgelist(df_edges, source='origin', target='destination',edge_attr='time', create_using=nx.MultiDiGraph)

pickle_name = 'pickles/quant.file'

with open(pickle_name, 'wb') as output:
	# overwrites any existing file of that name
	pickle.dump(graph, output, pickle.HIGHEST_PROTOCOL)

	with open(pickle_name, 'wb') as output: pickle.dump(graph, output, pickle.HIGHEST_PROTOCOL)