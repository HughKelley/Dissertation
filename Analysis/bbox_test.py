import osmnx as ox

ox.config(use_cache=True, log_console=True)

# ox.configure(use_cache=True, log_console=True)


# big bbox
north = 51.55975924
south = 51.45975924
east = -0.010389357
west = -0.2106266

# small bbox 
# half size
north = north - (north - south) / 4
south = south + (north - south) / 4
east = east + (west - east) / 4
west = west - (west - east) / 4


# extent of north inner london boundary

# east = -0.255164782343012 
# west = 0.00934658957231362 
# south = 51.4647441507093
# north = 51.5778742530578



# filter_dict = 


# cycle_filter = '["area"!~"yes"]["highway"="cycleway"]'





# cycle_plus_filter = '["area"!~"yes"]["highway"="cycleway"]'

# basic_bike
# moderate_bike

test_net = ox.graph_from_bbox(north, south, east, west, network_type = 'moderate_bike', retain_all=True, name = 'London_box', )


# fig, ax = ox.plot_graph(test_net)



# osm_filter for osm_net_download:  

# ["area"!~"yes"]
# ["highway"!~"cycleway|footway|path|pedestrian|steps|track|corridor|elevator|escalator|proposed|construction|bridleway|abandoned|platform|raceway|service"]["motor_vehicle"!~"no"]["motorcar"!~"no"]["access"!~"private"]["service"!~"parking|parking_aisle|driveway|private|emergency_access"]



 # Overpass:  
 # [out:json][timeout:180];(way["highway"]["area"!~"yes"]["highway"!~"cycleway|footway|path|pedestrian|steps|track|corridor|elevator|escalator|proposed|construction|bridleway|abandoned|platform|raceway|service"]["motor_vehicle"!~"no"]["motorcar"!~"no"]["access"!~"private"]["service"!~"parking|parking_aisle|driveway|private|emergency_access"]
 # 	(51.474015,-0.180287,51.539253,-0.053244);>;);out;

# nodes, edges = ox.graph_to_gdfs(test_net, nodes = True, edges = True, node_geometry = True, fill_edge_geometry = True)



# print(test_net.graph['crs'])

# test_file = ox.save_graphml(test_net, filename = 'test.graphml', gephi = True)

# new_net = ox.load_graphml('test.graphml')
# print(new_net.graph['crs'])