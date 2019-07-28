# import
import pandas as pd 
import sqlalchemy
import osmnx as ox 
from shapely.wkt import loads
from geopandas import GeoDataFrame



# connect to DB

engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')

# Base = declarative_base(engine)
# metadata = sqlalchemy.MetaData()


# pull tables into gdf's

query = 'SELECT * FROM london_drive_nodes'

nodes = pd.read_sql(query, con = engine, )

# convert to geodataframe
# http://geopandas.org/reference.html?highlight=wkb#geopandas.GeoDataFrame.from_postgis

df = geopandas.GeoDataFrame.from_postgis(sql = query, con = engine, geom_col = geom, crs= 27700,  )


# ox.graph_to_gdfs() returns gdf with structure:
#            highway       osmid         x          y                       geometry
# 3398008838     NaN  3398008838 -0.139214  51.491624  POINT (-0.1392139 51.4916235)


# convert WKB into geoalchemy geometry column

# turn gdf's into network


# 