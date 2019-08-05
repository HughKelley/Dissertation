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

net_1 = ox.graph_from_bbox(north, south, east, west, network_type = 'bike_1', retain_all=True, name = 'London_box', )

net_2 = ox.graph_from_bbox(north, south, east, west, network_type = 'bike_2', retain_all=True, name = 'London_box', )

net_3 = ox.graph_from_bbox(north, south, east, west, network_type = 'bike_3', retain_all=True, name = 'London_box', )

net_4 = ox.graph_from_bbox(north, south, east, west, network_type = 'bike_4', retain_all=True, name = 'London_box', )

net_5 = ox.graph_from_bbox(north, south, east, west, network_type = 'bike_5', retain_all=True, name = 'London_box', )

fig2, ax2 = ox.plot_graph(net_2, node_alpha=0)
fig2.savefig('box_bike_2.png')

fig3, ax3 = ox.plot_graph(net_3, node_alpha=0)
fig3.savefig('box_bike_3.png')

fig4, ax4 = ox.plot_graph(net_4, node_alpha=0)
fig4.savefig('box_bike_4.png')

fig5, ax5 = ox.plot_graph(net_5, node_alpha=0)
fig5.savefig('box_bike_5.png')



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