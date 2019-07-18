# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:02:56 2019

@author: Hugh
"""

# Imports
from geoalchemy2 import Geometry, WKTElement
import sqlalchemy
import pandas as pd
import geopandas as gpd

# make SQLAlchemy engine
engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')

# get geodataframe

# get data file
file = "Data/statistical-gis-boundaries-london/ESRI\LSOA_2011_London_gen_MHW.shp"
lsoa_shp = gpd.read_file(file)
#print(LSOA_shp)

column_names = list(lsoa_shp.columns.values)
column_types = list(lsoa_shp.dtypes)

crs = lsoa_shp.crs
print(crs)
crs_val = crs['init']
print(crs_val)
crs = 27700

# seems like a really bad way to store the crs...

# crs = {'init':'epsg:27700'}
# British National Grid
# https://epsg.io/27700

# convert to geodataframe
# geo_lsoa = gpd.GeoDataFrame(LSOA_shp)

lsoa_shp['geom'] = lsoa_shp['geometry'].apply(lambda x: WKTElement(x.wkt, srid = crs))

lsoa_shp.drop('geometry', 1, inplace=True)

table_name = 'lsoa_table'

lsoa_shp.to_sql(table_name, engine, if_exists='fail', index=False, dtype={'geom' : Geometry('Point', srid = crs)})



# Well Known Text for BNG

# PROJCS["OSGB 1936 / British National Grid",
#     GEOGCS["OSGB 1936",
#         DATUM["OSGB_1936",
#             SPHEROID["Airy 1830",6377563.396,299.3249646,
#                 AUTHORITY["EPSG","7001"]],
#             TOWGS84[446.448,-125.157,542.06,0.15,0.247,0.842,-20.489],
#             AUTHORITY["EPSG","6277"]],
#         PRIMEM["Greenwich",0,
#             AUTHORITY["EPSG","8901"]],
#         UNIT["degree",0.0174532925199433,
#             AUTHORITY["EPSG","9122"]],
#         AUTHORITY["EPSG","4277"]],
#     PROJECTION["Transverse_Mercator"],
#     PARAMETER["latitude_of_origin",49],
#     PARAMETER["central_meridian",-2],
#     PARAMETER["scale_factor",0.9996012717],
#     PARAMETER["false_easting",400000],
#     PARAMETER["false_northing",-100000],
#     UNIT["metre",1,
#         AUTHORITY["EPSG","9001"]],
#     AXIS["Easting",EAST],
#     AXIS["Northing",NORTH],
#     AUTHORITY["EPSG","27700"]]

