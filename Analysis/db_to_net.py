# import
import pandas as pd 
import sqlalchemy
import osmnx as ox 
from shapely.wkt import loads
import geopandas as gpd 



# connect to DB

engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')

# Base = declarative_base(engine)
# metadata = sqlalchemy.MetaData()


# pull tables into gdf's

node_query = 'SELECT * FROM london_drive_nodes'
edge_query = 'SELECT * FROM london_drive_edges'

# convert to geodataframe
# http://geopandas.org/reference.html?highlight=wkb#geopandas.GeoDataFrame.from_postgis

nodes = gpd.GeoDataFrame.from_postgis(sql = node_query, con = engine, geom_col = 'geom', crs= 27700)
edges = gpd.GeoDataFrame.from_postgis(sql = edge_query, con = engine, geom_col = 'geom', crs= 27700)

nodes.gdf_name = 'nodes'

edges.gdf_name = 'edges'

# ox.graph_to_gdfs() returns gdf with structure:
#            highway       osmid         x          y                       geometry
# 3398008838     NaN  3398008838 -0.139214  51.491624  POINT (-0.1392139 51.4916235)


# convert WKB into geoalchemy geometry column
# postgis handles this 

# turn gdf's into network
net = ox.gdfs_to_graph(gdf_nodes = nodes, gdf_edges = edges)



# 