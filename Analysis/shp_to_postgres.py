# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:02:56 2019

@author: Hugh
"""

# modules 
import pandas as pd
import geopandas as gpd
import psycopg2
from geoalchemy2 import Geometry, WKTElement
import sqlalchemy

# get data file
file = "Data/statistical-gis-boundaries-london/ESRI\LSOA_2011_London_gen_MHW.shp"
LSOA_shp = gpd.read_file(file)
#print(LSOA_shp)

column_names = list(LSOA_shp.columns.values)
column_types = list(LSOA_shp.dtypes)

# convert to geodataframe

geo_lsoa = gpd.GeoDataFrame(LSOA_shp)

# where dtype is 'O', python is indicating that the column is not a base type, it's a python Object

##############################################################################
# with sqlalchemy engine
###################################################################

engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')

## test operation
#data = [['Alex',10],['Bob',12],['Clarke',13]]
#df = pd.DataFrame(data,columns=['Name','Age'])
#df.to_sql('test4', engine)

LSOA_shp.to_sql('lsoa_data', engine)
# https://gis.stackexchange.com/questions/310912/importing-geojson-into-postgis-with-python

# about to be so easy with SQLalpchemy GEO extension
# https://gis.stackexchange.com/questions/239198/adding-geopandas-dataframe-to-postgis-table/239231

##############################################################################
# with psycopg2
###################################################################

# start connection to DB
conn = psycopg2.connect(database="Dissertation", user="postgres", password="tuesday789")
cur = conn.cursor()

#cur.execute("CREATE TABLE lsoa (id serial PRIMARY KEY, LSOA11CD varchar(32), LSOA11NM varchar(32), geom geometry);")
# looks in pgAdmin like this was fine and postgis is installed correctly because geometry dat type was accepted? 

# put the data from the shapefile as a geodataframe into the table




# does this need to iterate through the rows of the GDF?
#cur.execute("INSERT INTO lsoa VALUES " from GDF)


# put upload code here


#
#cur.execute("CREATE TABLE test3 (id serial PRIMARY KEY, num integer, data varchar);")
#cur.execute("INSERT INTO test3 (num, data) VALUES (%s, %s)",(100, "abc'def"))
#cur.execute("SELECT * FROM test3;")
#cur.fetchone()


conn.commit()

cur.close()

conn.close()
