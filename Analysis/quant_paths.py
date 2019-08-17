# calculate missing values for quant


# import
import networkx 
import sqlalchemy
import pickle
import pandas as pd 
from datetime import datetime



# engine
engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')


# net
file = 'pickles/quant.file'
net = pickle.load(open(file, 'rb'))

# pairs

sql = 'select origin, destination dest from quant_missing_1;'
# sql = 'select origin, destination dest from quant_missing_2;'

pairs = pd.read_sql(sql,engine)

# 200,041


# for each pair, calc shortest path. 

start = datetime.now()
print('start: ', start)

for index, row in pairs.iterrows():

	origin = row['origin']
	dest = row['dest']

	if networkx.has_path(net, origin, dest):
		dist = networkx.shortest_path_length(net, origin, dest, weight = 'time')

		data_row = pd.DataFrame([{'origin':origin, 'dest':dest,'distance':dist}])
		data_row.to_sql('missing_quant_times_1', con=engine, if_exists='append')
		# data_row.to_sql('missing_quant_times_2', con=engine, if_exists='append')

	if index > 100:
		break

end = datetime.now()

print('end ', end)

print('elapsed: ', end - start)