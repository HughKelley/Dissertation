# read geojson file to DB


import geopandas

import sqlalchemy

file = 'Data/london_bike_relation.geojson'

engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')

data = geopandas.read_file(file)

# error: can't adapt type multi line string

# gotta convert the geometry column I guess

data.to_sql(name = 'relation', con = engine)