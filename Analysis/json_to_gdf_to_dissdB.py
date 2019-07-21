# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 11:57:04 2019

@author: Hugh
"""

# imports

import json
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

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

class element(Base):
     __tablename__ = 'osm_elements'

     id = Column(Integer, primary_key=True)
     kind = Column(String)
     lat = Column(Float)
     lon = Column(Float)

     def __repr__(self):
        return "<element(kind='%s', lat='%s', lon='%s')>" % (self.kind, self.lat, self.lon)


class tag(Base):
	__tablename__= 'osm_tags'

	prim_key = Column(String, primary_key=True)
	id = Column(Integer)
	key = Column(String)
	value = Column(String)

	def __repr__(self):
		return "<tag(prim_key='%s', id='%s', key='%s', value='%s'>" % (self.prim_key, self.id, self.key, self.value)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


# subset json data to actual data, without metadata

# {
#   "type": "node",
#   "id": 78112,
#   "lat": 51.5269760,
#   "lon": -0.1457924,
#   "example": "an_example"
# },


# loop through nodes
count = 0
key_int = 0


for item in data: 

	print("json item number: ", count)
	count = count + 1

	if count > 100: break

	# ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
	new_element = element(id = x['id'], kind = x['type'], lat = x['lat'], lon = x['lon'])
	session.add(new_element)

	if len(x) > 4:
		for pair in x:
			if pair == 'id':
				continue
			if pair == 'type':
				continue
			if pair == 'lat':
				continue
			if pair == 'lon':
				continue

			key_int = key_int + 1
			new_tag = tag(prim_key = key_int, id = x['id'], key=pair, value=x[pair])

			# send to sql
			session.add(new_tag)

	session.commit()

	# next



# close connection

# close json file: happens at end of "with"



