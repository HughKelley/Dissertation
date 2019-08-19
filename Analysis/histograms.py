# making histograms from distances data

import matplotlib.pyplot as plt
#import numpy as np
import pandas as pd
import sqlalchemy
import seaborn as sns


engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')

sql = 'select * from all_agg_directness;'

data = pd.read_sql(sql, con=engine)






#df = pd.read_csv('https://raw.githubusercontent.com/selva86/datasets/master/diamonds.csv')
print(data.head())

print(list(data))

u_1 = data.loc[:,'u_1_direct']


max_u_1 = data['u_1_direct'].max()

print(max_u_1)

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

