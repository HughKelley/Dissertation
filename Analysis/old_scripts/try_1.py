# -*- coding: utf-8 -*-
"""
Created on Fri May 31 14:44:39 2019

@author: Hugh
"""

import requests
import geopandas as gpd



r = requests.get('https://nominatim.openstreetmap.org/search?format=json&limit=10&dedupe=0&polygon_geojson=1&q=London%2C+United%20Kingdom')

r.status_code

# kind of "decode" the json into a python structure of lists of dicts and dicts of lists
london_options = r.json()

# then grab just the dict that we want from the top list
london_boundary = london_options[1]

# see all the keys in the dict

for key, value in london_boundary.items() :
    print(key)
    
london_polygon = london_boundary['geojson']

# then get this stuff into geopandas somehow

# internet examples use shapely

# then plot to check that it's correct

# import geopandas to work with API data




import networkx as nx
import osmnx as ox
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
ox.config(use_cache=True, log_console=True)

# defaults to taking first result in the json object returned
G = ox.graph_from_place('Baltimore, Maryland, USA', network_type='drive')

# explicitly uses the second result
london = ox.graph_from_place('London, United Kingdom', network_type='drive', which_result=2)

# then save locally
#ox.save_graph_shapefile(london, filename = 'london_network')
ox.save_graphml(london, filename='london_network.graphml')


# then plot network

fig, ax = ox.plot_graph(london)
# looks correct. big win

#network size
# this takes > 30 minutes to run
#london_proj = ox.project_graph(london)
#nodes_proj = ox.graph_to_gdfs(london_proj, edges = False)
#graph_area_m = nodes_proj.unary_union.convex_hull.area
#graph_area_m
#1839504069.4823053 sq meters


# basic network stats
ox.basic_stats(london_proj, area=graph_area_m, clean_intersects=True, circuity_dist='euclidean')
#
#{'n': 125316,
# 'm': 295994,
# 'k_avg': 4.7239618245076445,
# 'intersection_count': 93764,
# 'streets_per_node_avg': 2.5574228350729356,
# 'streets_per_node_counts': {0: 0,
#  1: 31552,
#  2: 1380,
#  3: 83606,
#  4: 8554,
#  5: 206,
#  6: 16,
#  7: 2},
# 'streets_per_node_proportion': {0: 0.0,
#  1: 0.2517795014204092,
#  2: 0.011012161256343963,
#  3: 0.6671614159405024,
#  4: 0.06825944013533787,
#  5: 0.0016438443614542437,
#  6: 0.00012767723195761116,
#  7: 1.5959653994701395e-05},
# 'edge_length_total': 29017095.54799952,
# 'edge_length_avg': 98.0327153523366,
# 'street_length_total': 15733068.697000204,
# 'street_length_avg': 97.83212407270503,
# 'street_segments_count': 160817,
# 'node_density_km': 68.12488326555749,
# 'intersection_density_km': 50.972434122631846,
# 'edge_density_km': 15774.41226110788,
# 'street_density_km': 8552.886051199652,
# 'circuity_avg': 1.0599049219728784,
# 'self_loop_proportion': 0.005155509908984642,
# 'clean_intersection_count': 73152,
# 'clean_intersection_density_km': 39.76724010215823}

# see more stats (mostly topological stuff) with extended_stats
#This takes a while too
more_stats = ox.extended_stats(london, ecc=True, bc=True, cc=True) #use arguments to turn other toplogical analyses on/off

#
#more_stats = ox.extended_stats(london, ecc=True, bc=True, cc=True) #use arguments to turn other toplogical analyses on/off
#Traceback (most recent call last):
#
#  File "<ipython-input-11-a01a026d6a5f>", line 1, in <module>
#    more_stats = ox.extended_stats(london, ecc=True, bc=True, cc=True) #use arguments to turn other toplogical analyses on/off
#
#  File "C:\Users\Hugh\Anaconda3\lib\site-packages\osmnx\stats.py", line 382, in extended_stats
#    sp = {source:dict(nx.single_source_dijkstra_path_length(G_strong, source, weight='length')) for source in G_strong.nodes()}
#
#  File "C:\Users\Hugh\Anaconda3\lib\site-packages\osmnx\stats.py", line 382, in <dictcomp>
#    sp = {source:dict(nx.single_source_dijkstra_path_length(G_strong, source, weight='length')) for source in G_strong.nodes()}
#
#  File "C:\Users\Hugh\Anaconda3\lib\site-packages\networkx\algorithms\shortest_paths\weighted.py", line 373, in single_source_dijkstra_path_length
#    weight=weight)
#
#  File "C:\Users\Hugh\Anaconda3\lib\site-packages\networkx\algorithms\shortest_paths\weighted.py", line 623, in multi_source_dijkstra_path_length
#    return _dijkstra_multisource(G, sources, weight, cutoff=cutoff)
#
#  File "C:\Users\Hugh\Anaconda3\lib\site-packages\networkx\algorithms\shortest_paths\weighted.py", line 824, in _dijkstra_multisource
#    dist[v] = d
#
#MemoryError



# edge closeness centrality: convert graph to line graph so edges become nodes and vice versa
edge_centrality = nx.closeness_centrality(nx.line_graph(london))




# list of edge values for the orginal graph
ev = [edge_centrality[edge + (0,)] for edge in london.edges()]

# color scale converted to list of colors for graph edges
norm = colors.Normalize(vmin=min(ev)*0.8, vmax=max(ev))
cmap = cm.ScalarMappable(norm=norm, cmap=cm.inferno)
ec = [cmap.to_rgba(cl) for cl in ev]

# color the edges in the original graph with closeness centralities in the line graph
fig, ax = ox.plot_graph(london, bgcolor='k', axis_off=True, node_size=0,
                        edge_color=ec, edge_linewidth=1.5, edge_alpha=1)








#Instead could just use a point and radius rather than the Name London. 

# and can use a place query dict to be max specific
# but not clear how this should work outside US. 




place_query = {'city':'San Francisco', 'state':'California', 'country':'USA'}
G = ox.graph_from_place(place_query, network_type='drive')


#G = ox.graph_from_place('Manhattan Island, New York City, New York, USA', network_type='drive')
#ox.plot_graph(G)