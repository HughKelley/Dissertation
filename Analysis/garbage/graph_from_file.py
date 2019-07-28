# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:58:01 2019

@author: Hugh
"""

import osmnx as ox
ox.config(use_cache=True, log_console=True)




# explicitly uses the second result
london = ox.graph_from_place('London, United Kingdom', network_type='drive', which_result=2)


#london_gdf = ox.gdf_from_place('London, United Kingdom', gdf_name = 'London')

#def gdf_from_place(query, gdf_name=None, which_result=1, buffer_dist=None):
#    """
#    Create a GeoDataFrame from a single place name query.
#
#    Parameters
#    ----------
#    query : string or dict
#        query string or structured query dict to geocode/download
#    gdf_name : string
#        name attribute metadata for GeoDataFrame (this is used to save shapefile
#        later)
#    which_result : int
#        max number of results to return and which to process upon receipt
#    buffer_dist : float
#        distance to buffer around the place geometry, in meters
#
#    Returns
#    -------
#    GeoDataFrame
#    
#    """




#gdf_from_place query:  London, United Kingdom

#osm polygon download params:  OrderedDict([('format', 'json'), ('limit', 2), ('dedupe', 0), ('polygon_geojson', 1), ('q', 'London, United Kingdom')])



# then save locally
#ox.save_graph_shapefile(london, filename = 'london_network')
ox.save_graphml(london, filename='london_network.graphml')


# then plot network
#fig, ax = ox.plot_graph(london)
# looks correct. big win