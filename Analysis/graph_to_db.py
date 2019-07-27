import osmnx as ox
import pandas as pd  
from sqlalchemy import *
import geopandas as gpd
from geoalchemy2 import Geometry, WKTElement

# load graphml file as multidigraph object
file = "C:/Users/Hugh/Documents/UCL_CASA_1819/Dissertation/Analysis/Data/bike.graphml"
file = "bike.graphml"

graph = ox.load_graphml(file)

# multidigraph to geodataframe

nodes, edges  = ox.gaph_to_gdf(graph, nodes = True, edges = True, node_geometry = True, fill_edge_geometry = True)

# geodataframe to sql table 

# define connection

engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')

# convert geometry column to WKT and drop redundant column

# gdf to sql


# close



# CRS notes: 
	# UTM is universal transverse mercator
	# a projected crs
	# WSG84 is World Geodetic System from 1984
	# Geographic coordinate system in lat and lon


# projection module offers: 
	# project_gdf
	# project_geometry
	# project_graph
	# https://osmnx.readthedocs.io/en/stable/osmnx.html?highlight=coordinate%20reference%20system#osmnx.projection.project_geometry