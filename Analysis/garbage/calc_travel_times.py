# Data:
# 	LSOA centerpoints
# 	networks
# 	quant table


# import

import slqalchemy
import networkx
import osmnx as ox
import geoalchemy
import pandas


# connect to db

engine = 

Base = 

metadata = Metadata()

# define necessary classes

	# class for pulling pairs out of quant table

class quant(Base):
	def method_a(self):
		pass

	# class for loading results into results table
class results(Base):
	def method_a(self)		
		pass



# load network

network = ox.load_graphml()

# osmnx.save_load.load_graphml(filename, folder=None, node_type=<class 'int'>)


# pull an O/D pair from Quant Table

current_pair = quant.query()

# not clear how to iterate through pairs 
# could just iterate through integer primary key I guess

# match O and D to a node on the network

	# this might be way easier if the network data was in sql

# call networkx function for calculating distance

	path = networkx.shortest_path()

	# or can use specific algo

# pass distance to results table with necessary data. 

	# Should I save the actual route? 


# 	pull O/D pair out of quant database

# 	query lsoa-centrepoints database for locations

# 	match locations to nodes on network

# 	calculate shortest path for that O/D pair

# 	record to output table

# 	next