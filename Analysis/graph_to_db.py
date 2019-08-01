import osmnx as ox
import pandas as pd  

import geopandas as gpd
from geoalchemy2 import Geometry, WKTElement

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# get the data types
from sqlalchemy import Column, Integer, String, Float, BigInteger
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape 

# set up sql connection
engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')

Base = declarative_base(engine)
metadata = sqlalchemy.MetaData()

class wsg_boundaries(Base):

	__table__ = sqlalchemy.Table('wsg_boundaries', metadata, autoload=True, autoload_with=engine)

# Function to generate WKB hex
def wkb_hexer(line):
    return line.wkb_hex


# convert geometry to usable type
def geom_column_to_wkb(gdf):

	gdf['geom'] = gdf['geometry'].apply(wkb_hexer)
	gdf.drop('geometry', 1, inplace=True)

	return gdf

def change_geom(net_type, engine, crs):
	""""""

	node_table_name = net_type + '_nodes'
	edge_table_name = net_type + '_edges'

	tables = [ node_table_name, edge_table_name]

	for table in tables:

		with engine.connect() as conn, conn.begin():
			sql = 'ALTER TABLE ' + table + ' ALTER COLUMN geom TYPE Geometry(Polygon, ' + str(crs) + ') USING ST_SetSRID(geom::Geometry, ' + str(crs) + ')'
			conn.execute(sql)

	return 0


def get_poly(session, table):

	boundary_data = session.query(table).all()

	boundary_geom = boundary_data[0].geom 

	shapely_geom = to_shape(boundary_geom)

	# buffer to get valid outer ring polygon instead of invalid multipolygon. 

	valid_poly = shapely_geom.buffer(0)

	return valid_poly



def loadSession():
	""""""
	Session = sessionmaker(bind=engine)
	session = Session()
	return session


if __name__ == "__main__":


	# get boundary data

	session = loadSession()

	polygon = get_poly(session, wsg_boundary)



	# define list of network types
	# file_list = ['all', 'bike', 'walk']
	# file_list = ['drive']
	# file_list = ['all', 'bike', 'walk', 'drive']
	file_list = ['all']
	# custom filters



	for item in file_list:

		print(item)

		# get the network from osm

		filter = ''

		name = 'london_' + item + '_projected'
		geo_graph = ox.graph_from_polygon(polygon, network_type = item, name = name)
		graph = ox.project_graph(geo_graph)

		# project graph using osmnx function instead of doing it in postgis

		# convert the network to 2 gdf's

		nodes, edges = ox.graph_to_gdfs(graph, nodes = True, edges = True, node_geometry = True, fill_edge_geometry = True)

		print(item, ' network retrieved and converted to gdfs')

		# convert the geometry of each gdf to WKB

		nodes = geom_column_to_wkb(nodes)
		edges = geom_column_to_wkb(edges)

		# put the gdf into the DB

		nodes.to_sql((name + '_nodes') , engine, if_exists='fail', index=False)
		edges.to_sql((name + '_edges') , engine, if_exists='fail', index=False)

		print('to sql successfully')

		# alter the geometry of the column

		# crs = str(4326)

		# with engine.connect() as conn, conn.begin():
		# 	sql = 'ALTER TABLE ' + name + '_nodes' + ' ALTER COLUMN geom TYPE Geometry(Point, ' + crs + ') USING ST_SetSRID(geom::Geometry, ' + crs + ')'
		# 	conn.execute(sql)

		# with engine.connect() as conn, conn.begin():
		# 	sql = 'ALTER TABLE ' + name + '_edges' + ' ALTER COLUMN geom TYPE Geometry(LineString, ' + crs + ') USING ST_SetSRID(geom::Geometry, ' + crs + ')'
		# 	conn.execute(sql)



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