import osmnx as ox

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


test_net = ox.graph_from_bbox(north, south, east, west, network_type = 'drive', name = 'London_box')


nodes, edges = ox.graph_to_gdfs(test_net, nodes = True, edges = True, node)


# print(test_net.graph['crs'])

# test_file = ox.save_graphml(test_net, filename = 'test.graphml', gephi = True)

# new_net = ox.load_graphml('test.graphml')
# print(new_net.graph['crs'])