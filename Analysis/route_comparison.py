# make plots of routes through network where distance changes a lot betweeen nets d1 and d2

import pickle
import networkx as nx 
import osmnx as ox

file_d1 = 'pickles/london_bike_1_projected_pickle.file'
file_d2 = 'pickles/london_bike_2_projected_pickle.file'

net_d1 = pickle.load(open(file_d1, 'rb'))
net_d2 = pickle.load(open(file_d2, 'rb'))

origin = 362575231		
dest = 248948337


d1_route = nx.shortest_path(net_d1, origin, dest, weight='length')
d2_route = nx.shortest_path(net_d2, origin, dest, weight='length')

fig_1, ax_1 = ox.plot_graph_route(net_d1, d1_route, node_size=0)

fig_2, ax_2 = ox.plot_graph_route(net_d2, d2_route, node_size=0)

# load pickles

# calc routes

# plot routes




# # ex 5 
# origin = 2846921223
# dest = 1459025865


# ex 6
# origin 254761321
# dest 108666

# ex 7 
# origin 5279414475	
# dest 353890133
# 30% increase

# ex 8 
# origin 34104246	
# dest 1973712483

# ex 9

 # origin 362575231	
 # dest 248948337
 # 10% increase