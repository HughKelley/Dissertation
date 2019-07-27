# import
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# get the data types
from sqlalchemy import Column, Integer, String, Float, BigInteger
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape 

# my version of osmnx
import osmnx as ox 

# for transforming crs
from functools import partial
import pyproj
from shapely.ops import transform



# load session

# set up engine
engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')

Base = declarative_base(engine)

# metadata = sqlalchemy.MetaData()

# print(engine.table_names())

# print(Base.metadata)
# or 
# print(metadata.reflect(engine))

metadata = sqlalchemy.MetaData()


# declare mappings?

class geo_crs_lbound(Base):
    """
    eg. fields: id, title
    """

    __table__ = sqlalchemy.Table('geo_crs_lbound', metadata, autoload=True, autoload_with=engine)
    # boundary = sqlalchemy.Table('inner_london_boundary', metadata, autoload=True, autoload_with=engine)



def loadSession():
	""""""
	Session = sessionmaker(bind=engine)
	session = Session()
	return session



# def get_network(polygon, filter, name, filename):
# 	""""""
# 	try:
# 		graph = ox.graph_from_polygon(polygon=polygon, network_type = filter, name = name)
	
# 	except: 'error getting graph'

# 	try: 
# 		ox.save_graphml(g=graph, filename=filename, )
# 	except: graph

# 	return 0





# https://stackoverflow.com/questions/419163/what-does-if-name-main-do#419185
if __name__ == "__main__":
	session = loadSession()
	boundary_data = session.query(geo_crs_lbound).all()
	
	boundary_geom = boundary_data[0].geom 

	# check crs

	crs = boundary_geom.srid
	
	# then convert to shapely

	shapely_geom = to_shape(boundary_geom)

	# buffer to get valid outer ring polygon instead of invalid multipolygon. 

	valid_poly = shapely_geom.buffer(0)



	# success = get_network(shapely_geom, filter = 'all_private', name = 'london_all', filename = "all_priv_inner_london.graphml")

	# call function for getting and saving network from OSMnx



	# lines for getting and saving graph to graphml
	graph = ox.graph_from_polygon(valid_poly, name = 'london_all')

	# file = ox.save_graphml(graph, filename = 'all.graphml', gephi = True)


	# multidigraph to geodataframes
	nodes, edges  = ox.graph_to_gdfs(graph, nodes = True, edges = True, node_geometry = True, fill_edge_geometry = True)




# not clear how to check the shapely object



# query inner borough table for polygon



# make polygon a shapely object

# check crs


# pass polygon to osmnx graph maker


# call for various network types

# save to graphml file