# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:58:01 2019

@author: Hugh
"""


import osmnx as ox
ox.config(use_cache=True, log_console=True)




# explicitly uses the second result
london = ox.graph_from_place('London, United Kingdom', network_type='walk', which_result=2)

#https://nominatim.openstreetmap.org/search?format=json&limit=10&dedupe=0&polygon_geojson=1&q=Baltimore%2C+Maryland%2C+USA
#https://nominatim.openstreetmap.org/search?format=json&limit=10&dedupe=0&polygon_geojson=1&q=Camden%2C+United%20Kingdom


# then save locally
#ox.save_graph_shapefile(london, filename = 'london_network')
# ox.save_graphml(camden, filename='camden_network.graphml')


# then plot network
# fig, ax = ox.plot_graph(london)
# looks correct. big win