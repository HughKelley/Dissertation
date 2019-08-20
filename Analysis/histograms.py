# making histograms from distances data

import matplotlib.pyplot as plt
#import numpy as np
import pandas as pd
import sqlalchemy
import seaborn as sns


engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')

sql = 'select * from all_agg_directness;'
sql = 'select * from node_centroid_dist_diffs'

data = pd.read_sql(sql, con=engine)






#df = pd.read_csv('https://raw.githubusercontent.com/selva86/datasets/master/diamonds.csv')
print(data.head())

print(list(data))

sns.distplot(data['differences'], bins=100, axlabel='Differences in distance')



d_1 = data.loc[:,'d_1_direct']


max_u_1 = data['d_1_direct'].max()

sns.distplot(u_1, bins = 60, axlabel='directness')

d_1=u_1

range_d_1 = data[(data['d_1_direct'] < 3)]

range_d_1.head(5)

sns.distplot(range_d_1['d_2_direct'], bins=50, axlabel='d_1')


range_d_2 = data[(data['d_2_direct'] < 3)]

sns.distplot(range_d_2['d_2_direct'], bins=50, axlabel='d_2')







#############################################################################

# travel times distributions

sql = 'select * from agg_times_no_nulls'

times = pd.read_sql(sql, con=engine)

times.head(5)

list(times)

sns.distplot(times['quant_time'], bins=50, axlabel='quant travel times (mins)')


sns.distplot(times['d_1_time'], bins=60,axlabel='d_1 travel times (mins)')

sns.distplot(times['d_2_time'], bins=60, axlabel='d_2 travel times (mins)')

sns.distplot(times['u_2_time'], bins=60, axlabel='u_2 travel times (mins)')




#############################################################################

sql = 'select * from quant_node_dist_diff;'

q_n_diffs = pd.read_sql(sql, con=engine)

q_n_diffs.head(5)

q_n_diffs['difference'].mean()
#-1.722
q_n_diffs['difference'].std()
#48.407
# on average nodes are 1.7 meters further from each other than the associated 
# quant origins and destinations. 
# not significantly different from 0. 



sns.distplot(q_n_diffs['difference'], bins = 60, axlabel='difference in distances')

############################################################################





print(max_d_1)

#range_u_1 = data[['u_1_direct']].query('0 <= u_1_direct <= 3')

range_u_1 = data[(data['u_1_direct'] < 3)]

print(range_u_1.head(10))

ax = range_u_1['u_1_direct'].hist(bins=60)

n, bins, patches = plt.hist(range_u_1, bins=60, range=(0,3) )

plt.xlabel('test')
plt.title('test')


data['u_1_direct'].max()
#plt.hist(range_u_1, bins=10)


sns.distplot(range_u_1['u_1_direct'], bins=60, axlabel='test')

#
#x1 = df.loc[df.cut=='Ideal', 'depth']
#x2 = df.loc[df.cut=='Fair', 'depth']
#x3 = df.loc[df.cut=='Good', 'depth']

#kwargs = dict(alpha=0.5, bins=100)
#
#plt.hist(x1, **kwargs, color='g', label='Ideal')
#plt.hist(x2, **kwargs, color='b', label='Fair')
#plt.hist(x3, **kwargs, color='r', label='Good')
#plt.gca().set(title='Frequency Histogram of Diamond Depths', ylabel='Frequency')
#plt.xlim(50,75)
#plt.legend();

