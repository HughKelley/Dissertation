# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 15:09:03 2019

@author: Hugh
"""

import osmnx as ox
ox.config(use_cache=True, log_console=True)
import pandas as pd

london = ox.load_graphml('london_network.graphml')

fig, ax = ox.plot_graph(london)

#great this works don't have to worry about OSM anymore...


#Now need to associate other data with the graph object somehow

casualty_data = pd.read_csv('TFL-road-casualty-data-since-2005.csv')

# 200k road incidents with locations. 
# Need to associate with an edge in the network


