# import

import pandas as pd 
import sqlalchemy



file = "Data/TFL-road-casualty-data-since-2005.csv"

data = pd.read_csv(file)

engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')


# data.to_sql('casualties', con = engine, if_exists= 'fail')