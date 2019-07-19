# -*- coding: utf-8 -*-

""" 
19-7-2019
"""

import json

file = 'Data/sample_overpass_output.json'

with open(file, mode="r", encoding='utf-8') as read_file:
	data = json.load(read_file)

print(type(data))

# print("top of file", data[1])

dict_length = len(data)

print("length is: ", dict_length)


if dict_length < 100:
	for x in data: 
		print(x)
		print(type(data[x]))
		# print("length of entry: ", len(data[x]))

		# for y in x:
		# 	print(x, ": ", y)
		# 	print("length: ", len(y))


print("osm3s key length: ", len(data['osm3s']))

print("elements key length: ", len(data['elements']))

for y in data['osm3s']:
	print(y)
	print(type(y))


# so the actual data is in data['elements']

# loop through list adding each item to a gdf or something

actual_data = data['elements']

print(next(iter(actual_data)))

# {'type': 'node', 'id': 78112, 'lat': 51.526976, 'lon': -0.1457924}
# every list item should have these attributes
# some items will have other attributes
