import osmnx as ox
import pandas as pd  
from sqlalchemy import *
import geopandas as gpd
from geoalchemy2 import Geometry, WKTElement



# load graphml file as multidigraph object
# file = "C:/Users/Hugh/Documents/UCL_CASA_1819/Dissertation/Analysis/Data/bike.graphml"
file = "bike.graphml"

# Function to generate WKB hex
def wkb_hexer(line):
    return line.wkb_hex


# convert geometry to usable type
def geom_column_to_wkb(gdf, srid_val):
	pass

	gdf['geom'] = gdf['geometry'].apply(wkb_hexer)
	gdf.drop('geometry', 1, inplace=True)

	return gdf

def change_geom(net_type, engine, crs):
	""""""

	node_table_name = net_type + '_nodes'
	edge_table_name = net_type + 'edges'

	tables = [ node_table_name, edge_table_name]

	for table in tables:

		with engine.connect() as conn, conn.begin():
			sql = 'ALTER TABLE ' + table + ' ALTER COLUMN geom TYPE Geometry(Polygon, ' + str(crs) + ') USING ST_SetSRID(geom::Geometry, ' + str(crs) + ')'
			conn.execute(sql)

	return 0


def gml_to_db(net_type, net_file, engine):
	""""""

	# technically should check types but whatev

	# load that file
	graph = ox.load_graphml(net_file)

	# multidigraph to geodataframes
	nodes, edges  = ox.graph_to_gdfs(graph, nodes = True, edges = True, node_geometry = True, fill_edge_geometry = True)

	# geodataframes to sql tables

	# table names
	node_table_name = net_type + '_nodes'
	edge_table_name = net_type + 'edges'

	# convert geometry column to WKT and drop redundant column

	nodes = geom_column_to_wkb(nodes)
	edges = geom_column_to_wkb(edges)

	# gdf to sql

	# nodes.to_sql
	# edges.to_sql

	# execute alter table command to change geometry column

	alter = change_geom(net_type, engine = engine, crs = 4326)

	return 0











# do it as a loop through a list of files



if __name__ == '__main__' :

	# define connection
	engine = create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')

	# list of network types to be uploaded
	file_list = ['all', 'bike', 'drive', 'walk']

	# call function on each item of list
	for item in file_list:
		file_name = item + '.graphml'
		print(file_name)

	test = gml_to_db('drive', 'data/drive.graphml', engine = engine)



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