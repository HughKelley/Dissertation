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

print(engine.table_names())

# print(Base.metadata)
# or 
# print(metadata.reflect(engine))

metadata = sqlalchemy.MetaData()


# declare mappings?

class inner_london_boundary(Base):
    """
    eg. fields: id, title
    """

    __table__ = sqlalchemy.Table('inner_london_boundary', metadata, autoload=True, autoload_with=engine)
    # boundary = sqlalchemy.Table('inner_london_boundary', metadata, autoload=True, autoload_with=engine)



def loadSession():
	""""""
	Session = sessionmaker(bind=engine)
	session = Session()
	return session

# https://stackoverflow.com/questions/419163/what-does-if-name-main-do#419185
if __name__ == "__main__":
	session = loadSession()
	res = session.query(inner_london_boundary).all()
	


boundary_data = session.query(inner_london_boundary).all()


boundary_geom = boundary_data[0].geom 

# then convert to shapely

shapely_geom = to_shape(boundary_geom)

# check crs

crs = boundary_geom.srid

# not clear how to check the shapely object


project = partial(pyproj.transform, pyproj.Proj(init='epsg:27700'), pyproj.Proj(init='epsg:4326')) 

lat_lon_boundary = transform(project, shapely_geom)  # apply projection




# Base.metadata.create_all(engine)


# Session = sessionmaker(bind=engine)

# session = Session()

# query inner borough table for polygon



# make polygon a shapely object

# check crs


# pass polygon to osmnx graph maker


# call for various network types

# save to graphml file