# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 11:57:04 2019

@author: Hugh
"""

# imports

import json
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, BigInteger
from sqlalchemy.orm import sessionmaker

from datetime import datetime
startTime = datetime.now()

import pickle

# open json file into memory

file = 'Data/sample_overpass_output.json'

with open(file, mode="r", encoding='utf-8') as read_file:
	data = json.load(read_file)

# strip meta data
data = data['elements']

# open sql connection

engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')

Base = declarative_base()

# define classes

class node(Base):
     __tablename__ = 'osm_nodes'

     id = Column(BigInteger, primary_key=True)
     kind = Column(String)
     lat = Column(Float)
     lon = Column(Float)

     def __repr__(self):
        return "<element(kind='%s', lat='%s', lon='%s')>" % (self.kind, self.lat, self.lon)


class tag(Base):
	__tablename__= 'osm_tags'

	prim_key = Column(Integer, primary_key=True)
	id = Column(BigInteger)
	key = Column(String)
	value = Column(String)

	def __repr__(self):
		return "<tag(prim_key='%s', id='%s', key='%s', value='%s'>" % (self.prim_key, self.id, self.key, self.value)



class way(Base):
	__tablename__ = 'osm_ways'

	prim_key = Column(Integer, primary_key=True)
	id = Column(BigInteger)
	node = Column(BigInteger)

class way_tag(Base):
	__tablename__ = 'osm_way_tags'

	prim_key = Column(Integer, primary_key=True)
	id = Column(BigInteger)
	key = Column(String)
	value = Column(String)

# create in DB
# should really handle case where it already exists
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

# subset json data to actual data, without metadata

# {
#   "type": "node",
#   "id": 78112,
#   "lat": 51.5269760,
#   "lon": -0.1457924,
#   "example": "an_example"
# },

# {'type': 'node', 
# 	'id': 99939, 
# 	'lat': 51.5224429, 
# 	'lon': -0.1554618, 
# 	'tags': 
# 		{'highway': 'traffic_signals', 
# 		'traffic_signals:direction': 'forward'}}

# or if it's a way

# {'type': 'way', 
# 	'id': 667548455, 
# 	'nodes': [6250303376, 3069487527], 
# 	'tags': {'access': 'no', 
# 		'highway': 'footway', 
# 		'lit': 'yes'}}, 

# should really check for key in table already....

# loop through nodes
count = 0
node_key_int = 0
way_key = 0
way_tag_key = 0
missing_type = []

for item in data: 

	# print("json item number: ", count)
	count = count + 1

	# if count > 100000: break
	# if (count % 100000) == 0:
	# 	print(count)

	if item['type'] == 'way':
		# it's a way
		if 'id' in item and 'nodes' in item:

			for node in item['nodes']:
				new_way = way(prim_key = way_key, id = item['id'], node=node)
				session.add(new_way)
				way_key = way_key + 1


			tags = item['tags']
			for pair in tags:
				new_way_tag = way_tag(prim_key = way_tag_key, id = item['id'], key=pair , value=tags[pair] )
				session.add(new_way_tag)
				way_tag_key = way_tag_key + 1

	elif item['type'] == 'node':
		# it's a node

		if 'id' in item and 'type' in item and 'lat' in item and 'lon' in item: 
			new_node = node(id = item['id'], kind = item['type'], lat = item['lat'], lon = item['lon'])
			session.add(new_node)

			##################################################################
		
		if 'tags' in item:
			tags = item['tags']
			# print(tags)

			for pair in tags:
				# print(pair)

				node_key_int = node_key_int + 1
				new_tag = tag(prim_key = node_key_int, id = item['id'], key=pair, value=tags[pair])

				# send to sql
				session.add(new_tag)

			####################################################33

	else :

		missing_type.append(item)

	session.commit()


with open("saver.file", "wb") as f:
    pickle.dump(missing_type, f, pickle.HIGHEST_PROTOCOL)

print("missing type: ", len(missing_type))

print('total items: ', count)

print('total node tags: ', node_key_int)

print('total way tags: ', way_tag_key)
	# next

print(datetime.now() - startTime)


# most recent results
# total items:  137397
# total node tags:  31031
# total way tags:  159993
# 0:03:23.724521

# close connection
	# automatic at end of script?
# close json file: happens at end of "with"



